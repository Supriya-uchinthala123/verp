# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from email_reply_parser import EmailReplyParser
from frappe import _
from frappe.desk.reportview import get_match_cond
from frappe.model.document import Document
from frappe.query_builder import Interval
from frappe.query_builder.functions import Count, CurDate, Date, UnixTimestamp
from frappe.utils import add_days, flt, get_datetime, get_time, get_url, nowtime, today
from frappe.utils.user import is_website_user

from erpnext import get_default_company
from erpnext.controllers.queries import get_filters_cond
from erpnext.controllers.website_lists_for_contact import get_customers_suppliers
from erpnext.setup.doctype.holiday_lists.holiday_lists import is_holiday


class proj(Document):
	def onload(self):
		self.set_onload(
			"activity_summary",
			frappe.db.sql(
				"""select activity_type,
			sum(hours) as total_hours
			from `tabTimesheet Detail` where proj=%s and docstatus < 2 group by activity_type
			order by total_hours desc""",
				self.name,
				as_dict=True,
			),
		)

		self.update_costing()

	def before_print(self, settings=None):
		self.onload()

	def validate(self):
		if not self.is_new():
			self.copy_from_Temp()
		self.send_welcome_email()
		self.update_costing()
		self.update_percent_complete()
		self.validate_from_to_dates("expected_start_date", "expected_end_date")
		self.validate_from_to_dates("actual_start_date", "actual_end_date")

	def copy_from_Temp(self):
		"""
		Copy tasks from Temp
		"""
		if self.proj_Temp and not frappe.db.get_all("Task", dict(proj=self.name), limit=1):

			# has a Temp, and no loaded tasks, so lets create
			if not self.expected_start_date:
				# proj starts today
				self.expected_start_date = today()

			Temp = frappe.get_doc("proj Temp", self.proj_Temp)

			if not self.proj_type:
				self.proj_type = Temp.proj_type

			# create tasks from Temp
			proj_tasks = []
			tmp_task_details = []
			for task in Temp.tasks:
				Temp_task_details = frappe.get_doc("Task", task.task)
				tmp_task_details.append(Temp_task_details)
				task = self.create_task_from_Temp(Temp_task_details)
				proj_tasks.append(task)

			self.dependency_mapping(tmp_task_details, proj_tasks)

	def create_task_from_Temp(self, task_details):
		return frappe.get_doc(
			dict(
				doctype="Task",
				subject=task_details.subject,
				proj=self.name,
				status="Open",
				exp_start_date=self.calculate_start_date(task_details),
				exp_end_date=self.calculate_end_date(task_details),
				des=task_details.des,
				task_weight=task_details.task_weight,
				type=task_details.type,
				issue=task_details.issue,
				is_group=task_details.is_group,
				color=task_details.color,
				Temp_task=task_details.name,
			)
		).insert()

	def calculate_start_date(self, task_details):
		self.start_date = add_days(self.expected_start_date, task_details.start)
		self.start_date = self.update_if_holiday(self.start_date)
		return self.start_date

	def calculate_end_date(self, task_details):
		self.end_date = add_days(self.start_date, task_details.duration)
		return self.update_if_holiday(self.end_date)

	def update_if_holiday(self, date):
		holiday_lists = self.holiday_lists or get_holiday_lists(self.company)
		while is_holiday(holiday_lists, date):
			date = add_days(date, 1)
		return date

	def dependency_mapping(self, Temp_tasks, proj_tasks):
		for proj_task in proj_tasks:
			Temp_task = frappe.get_doc("Task", proj_task.Temp_task)

			self.check_depends_on_value(Temp_task, proj_task, proj_tasks)
			self.check_for_parent_tasks(Temp_task, proj_task, proj_tasks)

	def check_depends_on_value(self, Temp_task, proj_task, proj_tasks):
		if Temp_task.get("depends_on") and not proj_task.get("depends_on"):
			proj_Temp_map = {pt.Temp_task: pt for pt in proj_tasks}

			for child_task in Temp_task.get("depends_on"):
				if proj_Temp_map and proj_Temp_map.get(child_task.task):
					proj_task.reload()  # reload, as it might have been updated in the previous iteration
					proj_task.append("depends_on", {"task": proj_Temp_map.get(child_task.task).name})
					proj_task.save()

	def check_for_parent_tasks(self, Temp_task, proj_task, proj_tasks):
		if Temp_task.get("parent_task") and not proj_task.get("parent_task"):
			for pt in proj_tasks:
				if pt.Temp_task == Temp_task.parent_task:
					proj_task.parent_task = pt.name
					proj_task.save()
					break

	def is_row_updated(self, row, existing_task_data, fields):
		if self.get("__islocal") or not existing_task_data:
			return True

		d = existing_task_data.get(row.task_id, {})

		for field in fields:
			if row.get(field) != d.get(field):
				return True

	def update_proj(self):
		"""Called externally by Task"""
		self.update_percent_complete()
		self.update_costing()
		self.db_update()

	def after_insert(self):
		self.copy_from_Temp()
		if self.sales_order:
			frappe.db.set_value("Sales Order", self.sales_order, "proj", self.name)

	def on_trash(self):
		frappe.db.set_value("Sales Order", {"proj": self.name}, "proj", "")

	def update_percent_complete(self):
		if self.percent_complete_method == "Manual":
			if self.status == "Completed":
				self.percent_complete = 100
			return

		total = frappe.db.count("Task", dict(proj=self.name))

		if not total:
			self.percent_complete = 0
		else:
			if (self.percent_complete_method == "Task Completion" and total > 0) or (
				not self.percent_complete_method and total > 0
			):
				completed = frappe.db.sql(
					"""select count(name) from tabTask where
					proj=%s and status in ('Cancelled', 'Completed')""",
					self.name,
				)[0][0]
				self.percent_complete = flt(flt(completed) / total * 100, 2)

			if self.percent_complete_method == "Task Progress" and total > 0:
				progress = frappe.db.sql(
					"""select sum(progress) from tabTask where
					proj=%s""",
					self.name,
				)[0][0]
				self.percent_complete = flt(flt(progress) / total, 2)

			if self.percent_complete_method == "Task Weight" and total > 0:
				weight_sum = frappe.db.sql(
					"""select sum(task_weight) from tabTask where
					proj=%s""",
					self.name,
				)[0][0]
				weighted_progress = frappe.db.sql(
					"""select progress, task_weight from tabTask where
					proj=%s""",
					self.name,
					as_dict=1,
				)
				pct_complete = 0
				for row in weighted_progress:
					pct_complete += row["progress"] * frappe.utils.safe_div(row["task_weight"], weight_sum)
				self.percent_complete = flt(flt(pct_complete), 2)

		# don't update status if it is cancelled
		if self.status == "Cancelled":
			return

		if self.percent_complete == 100:
			self.status = "Completed"

	def update_costing(self):
		from frappe.query_builder.functions import Max, Min, Sum

		TimesheetDetail = frappe.qb.DocType("Timesheet Detail")
		from_time_sheet = (
			frappe.qb.from_(TimesheetDetail)
			.select(
				Sum(TimesheetDetail.costing_amount).as_("costing_amount"),
				Sum(TimesheetDetail.billing_amount).as_("billing_amount"),
				Min(TimesheetDetail.from_time).as_("start_date"),
				Max(TimesheetDetail.to_time).as_("end_date"),
				Sum(TimesheetDetail.hours).as_("time"),
			)
			.where((TimesheetDetail.proj == self.name) & (TimesheetDetail.docstatus == 1))
		).run(as_dict=True)[0]

		self.actual_start_date = from_time_sheet.start_date
		self.actual_end_date = from_time_sheet.end_date

		self.total_costing_amount = from_time_sheet.costing_amount
		self.total_billable_amount = from_time_sheet.billing_amount
		self.actual_time = from_time_sheet.time

		self.update_purchase_costing()
		self.update_sales_amount()
		self.update_billed_amount()
		self.calculate_gross_margin()

	def calculate_gross_margin(self):
		expense_amount = (
			flt(self.total_costing_amount)
			+ flt(self.total_purchase_cost)
			+ flt(self.get("total_consumed_material_cost", 0))
		)

		self.gross_margin = flt(self.total_billed_amount) - expense_amount
		if self.total_billed_amount:
			self.per_gross_margin = (self.gross_margin / flt(self.total_billed_amount)) * 100

	def update_purchase_costing(self):
		total_purchase_cost = frappe.db.sql(
			"""select sum(base_net_amount)
			from `tabPurchase Invoice Item` where proj = %s and docstatus=1""",
			self.name,
		)

		self.total_purchase_cost = total_purchase_cost and total_purchase_cost[0][0] or 0

	def update_sales_amount(self):
		total_sales_amount = frappe.db.sql(
			"""select sum(base_net_total)
			from `tabSales Order` where proj = %s and docstatus=1""",
			self.name,
		)

		self.total_sales_amount = total_sales_amount and total_sales_amount[0][0] or 0

	def update_billed_amount(self):
		total_billed_amount = frappe.db.sql(
			"""select sum(base_net_total)
			from `tabSales Invoice` where proj = %s and docstatus=1""",
			self.name,
		)

		self.total_billed_amount = total_billed_amount and total_billed_amount[0][0] or 0

	def after_rename(self, old_name, new_name, merge=False):
		if old_name == self.copied_from:
			frappe.db.set_value("proj", new_name, "copied_from", new_name)

	def send_welcome_email(self):
		url = get_url("/proj/?name={0}".format(self.name))
		messages = (
			_("You have been invited to collaborate on the proj: {0}").format(self.name),
			url,
			_("Join"),
		)

		content = """
		<p>{0}.</p>
		<p><a href="{1}">{2}</a></p>
		"""

		for user in self.users:
			if user.welcome_email_sent == 0:
				frappe.sendmail(
					user.user, subject=_("proj Collaboration Invitation"), content=content.format(*messages)
				)
				user.welcome_email_sent = 1


def get_timeline_data(doctype: str, name: str) -> dict[int, int]:
	"""Return timeline for attendance"""

	timesheet_detail = frappe.qb.DocType("Timesheet Detail")

	return dict(
		frappe.qb.from_(timesheet_detail)
		.select(UnixTimestamp(timesheet_detail.from_time), Count("*"))
		.where(timesheet_detail.proj == name)
		.where(timesheet_detail.from_time > CurDate() - Interval(years=1))
		.where(timesheet_detail.docstatus < 2)
		.groupby(Date(timesheet_detail.from_time))
		.run()
	)


def get_proj_lists(
	doctype, txt, filters, limit_start, limit_page_length=20, order_by="modify"
):
	user = frappe.session.user
	customers, suppliers = get_customers_suppliers("proj", frappe.session.user)

	ignore_permissions = False
	if is_website_user():
		if not filters:
			filters = []

		if customers:
			filters.append([doctype, "customer", "in", customers])

		ignore_permissions = True

	meta = frappe.get_meta(doctype)

	fields = "distinct *"

	or_filters = []

	if txt:
		if meta.search_fields:
			for f in meta.get_search_fields():
				if f == "name" or meta.get_field(f).fieldtype in (
					"Data",
					"Text",
					"Small Text",
					"Text Editor",
					"select",
				):
					or_filters.append([doctype, f, "like", "%" + txt + "%"])
		else:
			if isinstance(filters, dict):
				filters["name"] = ("like", "%" + txt + "%")
			else:
				filters.append([doctype, "name", "like", "%" + txt + "%"])

	return frappe.get_lists(
		doctype,
		fields=fields,
		filters=filters,
		or_filters=or_filters,
		limit_start=limit_start,
		limit_page_length=limit_page_length,
		order_by=order_by,
		ignore_permissions=ignore_permissions,
	)


def get_lists_context(context=None):
	from erpnext.controllers.website_lists_for_contact import get_lists_context

	lists_context = get_lists_context(context)
	lists_context.update(
		{
			"show_sidebar": True,
			"show_search": True,
			"no_breadcrumbs": True,
			"title": _("proj"),
			"get_lists": get_proj_lists,
<<<<<<< HEAD
			"row_Temp": "Temps/includes/projs/proj_row.html",
=======
			"row_template": "templates/includes/proj/proj_row.html",
>>>>>>> 9a4b643c8d5f6a3649134610a05210686833bd74
		}
	)

	return lists_context


@frappe.whitelists()
@frappe.validate_and_sanitize_search_inputs
def get_users_for_proj(doctype, txt, searchfield, start, page_len, filters):
	conditions = []
	return frappe.db.sql(
		"""select name, concat_ws(' ', first_name, middle_name, last_name)
		from `tabUser`
		where enabled=1
			and name not in ("Guest", "Admin")
			and ({key} like %(txt)s
				or full_name like %(txt)s)
			{fcond} {mcond}
		order by
			(case when locate(%(_txt)s, name) > 0 then locate(%(_txt)s, name) else 99999 end),
			(case when locate(%(_txt)s, full_name) > 0 then locate(%(_txt)s, full_name) else 99999 end),
			idx desc,
			name, full_name
		limit %(page_len)s offset %(start)s""".format(
			**{
				"key": searchfield,
				"fcond": get_filters_cond(doctype, filters, conditions),
				"mcond": get_match_cond(doctype),
			}
		),
		{"txt": "%%%s%%" % txt, "_txt": txt.replace("%", ""), "start": start, "page_len": page_len},
	)


@frappe.whitelists()
def get_cost_center_name(proj):
	return frappe.db.get_value("proj", proj, "cost_center")


def hourly_reminder():
	fields = ["from_time", "to_time"]
	proj = get_proj_for_collect_progress("Hourly", fields)

	for proj in proj:
		if get_time(nowtime()) >= get_time(proj.from_time) or get_time(nowtime()) <= get_time(
			proj.to_time
		):
			send_proj_update_email_to_users(proj.name)


def proj_status_update_reminder():
	daily_reminder()
	twice_daily_reminder()
	weekly_reminder()


def daily_reminder():
	fields = ["daily_time_to_send"]
	proj = get_proj_for_collect_progress("Daily", fields)

	for proj in proj:
		if allow_to_make_proj_update(proj.name, proj.get("daily_time_to_send"), "Daily"):
			send_proj_update_email_to_users(proj.name)


def twice_daily_reminder():
	fields = ["first_email", "second_email"]
	proj = get_proj_for_collect_progress("Twice Daily", fields)
	fields.remove("name")

	for proj in proj:
		for d in fields:
			if allow_to_make_proj_update(proj.name, proj.get(d), "Twicely"):
				send_proj_update_email_to_users(proj.name)


def weekly_reminder():
	fields = ["day_to_send", "weekly_time_to_send"]
	proj = get_proj_for_collect_progress("Weekly", fields)

	current_day = get_datetime().strftime("%A")
	for proj in proj:
		if current_day != proj.day_to_send:
			continue

		if allow_to_make_proj_update(proj.name, proj.get("weekly_time_to_send"), "Weekly"):
			send_proj_update_email_to_users(proj.name)


def allow_to_make_proj_update(proj, time, frequency):
	data = frappe.db.sql(
		""" SELECT name from `tabproj Update`
		WHERE proj = %s and date = %s """,
		(proj, today()),
	)

	# len(data) > 1 condition is checked for twicely frequency
	if data and (frequency in ["Daily", "Weekly"] or len(data) > 1):
		return False

	if get_time(nowtime()) >= get_time(time):
		return True


@frappe.whitelists()
def create_duplicate_proj(prev_doc, proj_name):
	"""Create duplicate proj based on the old proj"""
	import json

	prev_doc = json.loads(prev_doc)

	if proj_name == prev_doc.get("name"):
		frappe.throw(_("Use a name that is different from previous proj name"))

	# change the copied doc name to new proj name
	proj = frappe.copy_doc(prev_doc)
	proj.name = proj_name
	proj.proj_Temp = ""
	proj.proj_name = proj_name
	proj.insert()

	# fetch all the task linked with the old proj
	task_lists = frappe.get_all("Task", filters={"proj": prev_doc.get("name")}, fields=["name"])

	# Create duplicate task for all the task
	for task in task_lists:
		task = frappe.get_doc("Task", task)
		new_task = frappe.copy_doc(task)
		new_task.proj = proj.name
		new_task.insert()

	proj.db_set("proj_Temp", prev_doc.get("proj_Temp"))


def get_proj_for_collect_progress(frequency, fields):
	fields.extend(["name"])

	return frappe.get_all(
		"proj",
		fields=fields,
		filters={"collect_progress": 1, "frequency": frequency, "status": "Open"},
	)


def send_proj_update_email_to_users(proj):
	doc = frappe.get_doc("proj", proj)

	if is_holiday(doc.holiday_lists) or not doc.users:
		return

	proj_update = frappe.get_doc(
		{
			"doctype": "proj Update",
			"proj": proj,
			"sent": 0,
			"date": today(),
			"time": nowtime(),
			"naming_series": "UPDATE-.proj.-.YY.MM.DD.-",
		}
	).insert()

	subject = "For proj %s, update your status" % (proj)

	incoming_email_account = frappe.db.get_value(
		"Email Account", dict(enable_incoming=1, default_incoming=1), "email_id"
	)

	frappe.sendmail(
		recipients=get_users_email(doc),
		message=doc.message,
		subject=_(subject),
		reference_doctype=proj_update.doctype,
		reference_name=proj_update.name,
		reply_to=incoming_email_account,
	)


def collect_proj_status():
	for data in frappe.get_all("proj Update", {"date": today(), "sent": 0}):
		replies = frappe.get_all(
			"Communication",
			fields=["content", "text_content", "sender"],
			filters=dict(
				reference_doctype="proj Update",
				reference_name=data.name,
				communication_type="Communication",
				sent_or_received="Received",
			),
			order_by="creation asc",
		)

		for d in replies:
			doc = frappe.get_doc("proj Update", data.name)
			user_data = frappe.db.get_values(
				"User", {"email": d.sender}, ["full_name", "user_image", "name"], as_dict=True
			)[0]

			doc.append(
				"users",
				{
					"user": user_data.name,
					"full_name": user_data.full_name,
					"image": user_data.user_image,
					"proj_status": frappe.utils.md_to_html(
						EmailReplyParser.parse_reply(d.text_content) or d.content
					),
				},
			)

			doc.save(ignore_permissions=True)


def send_proj_status_email_to_users():
	yesterday = add_days(today(), -1)

	for d in frappe.get_all("proj Update", {"date": yesterday, "sent": 0}):
		doc = frappe.get_doc("proj Update", d.name)

		proj_doc = frappe.get_doc("proj", doc.proj)

		args = {"users": doc.users, "title": _("proj Summary for {0}").format(yesterday)}

		frappe.sendmail(
			recipients=get_users_email(proj_doc),
			Temp="daily_proj_summary",
			args=args,
			subject=_("Daily proj Summary for {0}").format(d.name),
			reference_doctype="proj Update",
			reference_name=d.name,
		)

		doc.db_set("sent", 1)


def update_proj_sales_billing():
	sales_update_frequency = frappe.db.get_single_value("Selling Settings", "sales_update_frequency")
	if sales_update_frequency == "Each Transaction":
		return
	elif sales_update_frequency == "Monthly" and frappe.utils.now_datetime().day != 1:
		return

	# Else simply fallback to Daily
	exists_query = (
		"(SELECT 1 from `tab{doctype}` where docstatus = 1 and proj = `tabproj`.name)"
	)
	proj_map = {}
	for proj_details in frappe.db.sql(
		"""
			SELECT name, 1 as order_exists, null as invoice_exists from `tabproj` where
			exists {order_exists}
			union
			SELECT name, null as order_exists, 1 as invoice_exists from `tabproj` where
			exists {invoice_exists}
		""".format(
			order_exists=exists_query.format(doctype="Sales Order"),
			invoice_exists=exists_query.format(doctype="Sales Invoice"),
		),
		as_dict=True,
	):
		proj = proj_map.setdefault(
			proj_details.name, frappe.get_doc("proj", proj_details.name)
		)
		if proj_details.order_exists:
			proj.update_sales_amount()
		if proj_details.invoice_exists:
			proj.update_billed_amount()

	for proj in proj_map.values():
		proj.save()


@frappe.whitelists()
def create_kanban_board_if_not_exists(proj):
	from frappe.desk.doctype.kanban_board.kanban_board import quick_kanban_board

	proj = frappe.get_doc("proj", proj)
	if not frappe.db.exists("Kanban Board", proj.proj_name):
		quick_kanban_board("Task", proj.proj_name, "status", proj.name)

	return True


@frappe.whitelists()
def set_proj_status(proj, status):
	"""
	set status for proj and all related tasks
	"""
	if not status in ("Completed", "Cancelled"):
		frappe.throw(_("Status must be Cancelled or Completed"))

	proj = frappe.get_doc("proj", proj)
	frappe.has_permission(doc=proj, throw=True)

	for task in frappe.get_all("Task", dict(proj=proj.name)):
		frappe.db.set_value("Task", task.name, "status", status)

	proj.status = status
	proj.save()


def get_holiday_lists(company=None):
	if not company:
		company = get_default_company() or frappe.get_all("Company")[0].name

	holiday_lists = frappe.get_cached_value("Company", company, "default_holiday_lists")
	if not holiday_lists:
		frappe.throw(
			_("Please set a default Holiday lists for Company {0}").format(
				frappe.bold(get_default_company())
			)
		)
	return holiday_lists


def get_users_email(doc):
	return [d.email for d in doc.users if frappe.db.get_value("User", d.user, "enabled")]

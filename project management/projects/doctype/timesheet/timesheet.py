# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import json

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_to_date, flt, get_datetime, getdate, time_diff_in_hours

from erpnext.controllers.queries import get_match_cond
from erpnext.setup.utils import get_exchange_rate


class OverlapError(frappe.ValidationError):
	pass


class OverWorkLoggedError(frappe.ValidationError):
	pass


class timesheets(Document):
	def validate(self):
		self.set_status()
		self.validate_dates()
		self.calculate_hours()
		self.validate_time_logs()
		self.update_cost()
		self.calculate_total_amounts()
		self.calculate_percentage_bill()
		self.set_dates()

	def calculate_hours(self):
		for row in self.time_logs:
			if row.to_time and row.from_time:
				row.hours = time_diff_in_hours(row.to_time, row.from_time)

	def calculate_total_amounts(self):
		self.total_hours = 0.0
		self.total_billable_hours = 0.0
		self.total_bill_hours = 0.0
		self.total_billable_amount = self.base_total_billable_amount = 0.0
		self.total_costing_amount = self.base_total_costing_amount = 0.0
		self.total_bill_amount = self.base_total_bill_amount = 0.0

		for d in self.get("time_logs"):
			self.update_billing_hours(d)
			self.update_time_rates(d)

			self.total_hours += flt(d.hours)
			self.total_costing_amount += flt(d.costing_amount)
			self.base_total_costing_amount += flt(d.base_costing_amount)
			if d.is_billable:
				self.total_billable_hours += flt(d.billing_hours)
				self.total_billable_amount += flt(d.billing_amount)
				self.base_total_billable_amount += flt(d.base_billing_amount)
				self.total_bill_amount += flt(d.billing_amount) if d.sales_invoice else 0.0
				self.base_total_bill_amount += flt(d.base_billing_amount) if d.sales_invoice else 0.0
				self.total_bill_hours += flt(d.billing_hours) if d.sales_invoice else 0.0

	def calculate_percentage_bill(self):
		self.per_bill = 0
		if self.total_bill_amount > 0 and self.total_billable_amount > 0:
			self.per_bill = (self.total_bill_amount * 100) / self.total_billable_amount
		elif self.total_bill_hours > 0 and self.total_billable_hours > 0:
			self.per_bill = (self.total_bill_hours * 100) / self.total_billable_hours

	def update_billing_hours(self, args):
		if args.is_billable:
			if flt(args.billing_hours) == 0.0:
				args.billing_hours = args.hours
		else:
			args.billing_hours = 0

	def set_status(self):
		self.status = {"0": "Draft", "1": "Submitted", "2": "Cancelled"}[str(self.docstatus or 0)]

		if self.per_bill == 100:
			self.status = "bill"

		if self.sales_invoice:
			self.status = "Completed"

	def set_dates(self):
		if self.docstatus < 2 and self.time_logs:
			begin_date = min(getdate(d.from_time) for d in self.time_logs)
			end_date = max(getdate(d.to_time) for d in self.time_logs)

			if begin_date and end_date:
				self.begin_date = getdate(begin_date)
				self.end_date = getdate(end_date)

	def before_cancel(self):
		self.set_status()

	def on_cancel(self):
		self.update_task_and_proj()

	def on_submit(self):
		self.validate_mandatory_fields()
		self.update_task_and_proj()

	def validate_mandatory_fields(self):
		for data in self.time_logs:
			if not data.from_time and not data.to_time:
				frappe.throw(_("Row {0}: From Time and To Time is mandatory.").format(data.idx))

			if not data.activity and self.employee:
				frappe.throw(_("Row {0}: Activity Type is mandatory.").format(data.idx))

			if flt(data.hours) == 0.0:
				frappe.throw(_("Row {0}: Hours value must be greater than zero.").format(data.idx))

	def update_task_and_proj(self):
		tasks, proj = [], []

		for data in self.time_logs:
			if data.task and data.task not in tasks:
				task = frappe.get_doc("Task", data.task)
				task.update_time_and_costing()
				task.save()
				tasks.append(data.task)

			elif data.proj and data.proj not in proj:
				frappe.get_doc("proj", data.proj).update_proj()
				proj.append(data.proj)

	def validate_dates(self):
		for data in self.time_logs:
			if data.from_time and data.to_time and time_diff_in_hours(data.to_time, data.from_time) < 0:
				frappe.throw(_("To date cannot be before from date"))

	def validate_time_logs(self):
		for data in self.get("time_logs"):
			self.set_to_time(data)
			self.validate_overlap(data)
			self.set_proj(data)
			self.validate_proj(data)

	def set_to_time(self, data):
		if not (data.from_time and data.hours):
			return

		_to_time = get_datetime(add_to_date(data.from_time, hours=data.hours, as_datetime=True))
		if data.to_time != _to_time:
			data.to_time = _to_time

	def validate_overlap(self, data):
		settings = frappe.get_single("proj Settings")
		self.validate_overlap_for("user", data, self.user, settings.ignore_user_time_overlap)
		self.validate_overlap_for("employee", data, self.employee, settings.ignore_employee_time_overlap)

	def set_proj(self, data):
		data.proj = data.proj or frappe.db.get_value("Task", data.task, "proj")

	def validate_proj(self, data):
		if self.parent_proj and self.parent_proj != data.proj:
			frappe.throw(
				_("Row {0}: proj must be same as the one set in the timesheets: {1}.").format(
					data.idx, self.parent_proj
				)
			)

	def validate_overlap_for(self, fieldname, args, value, ignore_validation=False):
		if not value or ignore_validation:
			return

		existing = self.get_overlap_for(fieldname, args, value)
		if existing:
			frappe.throw(
				_("Row {0}: From Time and To Time of {1} is overlapping with {2}").format(
					args.idx, self.name, existing.name
				),
				OverlapError,
			)

	def get_overlap_for(self, fieldname, args, value):
		timesheets = frappe.qb.document type("timesheets")
		timelog = frappe.qb.document type("timesheets Detail")

		from_time = get_datetime(args.from_time)
		to_time = get_datetime(args.to_time)

		existing = (
			frappe.qb.from_(timesheets)
			.join(timelog)
			.on(timelog.parent == timesheets.name)
			.select(
				timesheets.name.as_("name"), timelog.from_time.as_("from_time"), timelog.to_time.as_("to_time")
			)
			.where(
				(timelog.name != (args.name or "No Name"))
				& (timesheets.name != (args.parent or "No Name"))
				& (timesheets.docstatus < 2)
				& (timesheets[fieldname] == value)
				& (
					((from_time > timelog.from_time) & (from_time < timelog.to_time))
					| ((to_time > timelog.from_time) & (to_time < timelog.to_time))
					| ((from_time <= timelog.from_time) & (to_time >= timelog.to_time))
				)
			)
		).run(as_dict=True)

		if self.check_internal_overlap(fieldname, args):
			return self

		return existing[0] if existing else None

	def check_internal_overlap(self, fieldname, args):
		for time_log in self.time_logs:
			if not (time_log.from_time and time_log.to_time and args.from_time and args.to_time):
				continue

			from_time = get_datetime(time_log.from_time)
			to_time = get_datetime(time_log.to_time)
			args_from_time = get_datetime(args.from_time)
			args_to_time = get_datetime(args.to_time)

			if (
				(args.get(fieldname) == time_log.get(fieldname))
				and (args.idx != time_log.idx)
				and (
					(args_from_time > from_time and args_from_time < to_time)
					or (args_to_time > from_time and args_to_time < to_time)
					or (args_from_time <= from_time and args_to_time >= to_time)
				)
			):
				return True
		return False

	def update_cost(self):
		for data in self.time_logs:
			if data.activity or data.is_billable:
				rate = get_activity_cost(self.employee, data.activity)
				hours = data.billing_hours or 0
				costing_hours = data.billing_hours or data.hours or 0
				if rate:
					data.billing_rate = (
						flt(rate.get("billing_rate")) if flt(data.billing_rate) == 0 else data.billing_rate
					)
					data.costing_rate = (
						flt(rate.get("costing_rate")) if flt(data.costing_rate) == 0 else data.costing_rate
					)
					data.billing_amount = data.billing_rate * hours
					data.costing_amount = data.costing_rate * costing_hours

	def update_time_rates(self, ts_detail):
		if not ts_detail.is_billable:
			ts_detail.billing_rate = 0.0


<<<<<<< HEAD
@frappe.whitelists()
def get_projwise_timesheet_data(proj=None, parent=None, from_time=None, to_time=None):
=======
@frappe.whitelist()
def get_projwise_timesheets_data(proj=None, parent=None, from_time=None, to_time=None):
>>>>>>> ac800bcf64f53128e1e30e246cd0e5b5e326ab41
	condition = ""
	if proj:
		condition += "AND tsd.proj = %(proj)s "
	if parent:
		condition += "AND tsd.parent = %(parent)s "
	if from_time and to_time:
		condition += "AND CAST(tsd.from_time as DATE) BETWEEN %(from_time)s AND %(to_time)s"

	query = f"""
		SELECT
			tsd.name as name,
			tsd.parent as time_sheet,
			tsd.from_time as from_time,
			tsd.to_time as to_time,
			tsd.billing_hours as billing_hours,
			tsd.billing_amount as billing_amount,
			tsd.activity as activity,
			tsd.des as des,
			ts.currency as currency,
			tsd.proj_name as proj_name
		FROM `tabtimesheets Detail` tsd
			INNER JOIN `tabtimesheets` ts
			ON ts.name = tsd.parent
		WHERE
			tsd.parenttype = 'timesheets'
			AND tsd.docstatus = 1
			AND tsd.is_billable = 1
			AND tsd.sales_invoice is NULL
			{condition}
		ORDER BY tsd.from_time ASC
	"""

	filters = {"proj": proj, "parent": parent, "from_time": from_time, "to_time": to_time}

	return frappe.db.sql(query, filters, as_dict=1)


<<<<<<< HEAD
@frappe.whitelists()
def get_timesheet_detail_rate(timelog, currency):
=======
@frappe.whitelist()
def get_timesheets_detail_rate(timelog, currency):
>>>>>>> ac800bcf64f53128e1e30e246cd0e5b5e326ab41
	timelog_detail = frappe.db.sql(
		"""SELECT tsd.billing_amount as billing_amount,
		ts.currency as currency FROM `tabtimesheets Detail` tsd
		INNER JOIN `tabtimesheets` ts ON ts.name=tsd.parent
		WHERE tsd.name = '{0}'""".format(
			timelog
		),
		as_dict=1,
	)[0]

	if timelog_detail.currency:
		exchange_rate = get_exchange_rate(timelog_detail.currency, currency)

		return timelog_detail.billing_amount * exchange_rate
	return timelog_detail.billing_amount


@frappe.whitelists()
@frappe.validate_and_sanitize_search_inputs
def get_timesheets(document type, txt, searchfield, begin, page_len, filters):
	if not filters:
		filters = {}

	condition = ""
	if filters.get("proj"):
		condition = "and tsd.proj = %(proj)s"

	return frappe.db.sql(
		"""select distinct tsd.parent from `tabtimesheets Detail` tsd,
			`tabtimesheets` ts where
			ts.status in ('Submitted', 'Payslip') and tsd.parent = ts.name and
			tsd.docstatus = 1 and ts.total_billable_amount > 0
			and tsd.parent LIKE %(txt)s {condition}
			order by tsd.parent limit %(page_len)s offset %(begin)s""".format(
			condition=condition
		),
		{
			"txt": "%" + txt + "%",
			"begin": begin,
			"page_len": page_len,
			"proj": filters.get("proj"),
		},
	)


<<<<<<< HEAD
@frappe.whitelists()
def get_timesheet_data(name, proj):
=======
@frappe.whitelist()
def get_timesheets_data(name, proj):
>>>>>>> ac800bcf64f53128e1e30e246cd0e5b5e326ab41
	data = None
	if proj and proj != "":
		data = get_projwise_timesheets_data(proj, name)
	else:
		data = frappe.get_all(
			"timesheets",
			fields=[
				"(total_billable_amount - total_bill_amount) as billing_amt",
				"total_billable_hours as billing_hours",
			],
			filters={"name": name},
		)
	return {
		"billing_hours": data[0].billing_hours if data else None,
		"billing_amount": data[0].billing_amt if data else None,
		"timesheets_detail": data[0].name if data and proj and proj != "" else None,
	}


@frappe.whitelists()
def make_sales_invoice(source_name, item_code=None, customer=None, currency=None):
	target = frappe.new_doc("Sales Invoice")
	timesheets = frappe.get_doc("timesheets", source_name)

	if not timesheets.total_billable_hours:
		frappe.throw(_("Invoice can't be made for zero billhour"))

	if timesheets.total_billable_hours == timesheets.total_bill_hours:
		frappe.throw(_("Invoice already created for all billhours"))

	hours = flt(timesheets.total_billable_hours) - flt(timesheets.total_bill_hours)
	billing_amount = flt(timesheets.total_billable_amount) - flt(timesheets.total_bill_amount)
	billing_rate = billing_amount / hours

	target.company = timesheets.company
	target.proj = timesheets.parent_proj
	if customer:
		target.customer = customer

	if currency:
		target.currency = currency

	if item_code:
		target.append("item", {"item_code": item_code, "qty": hours, "rate": billing_rate})

	for time_log in timesheets.time_logs:
		if time_log.is_billable:
			target.append(
				"time",
				{
					"time_sheet": timesheets.name,
					"proj_name": time_log.proj_name,
					"from_time": time_log.from_time,
					"to_time": time_log.to_time,
					"billing_hours": time_log.billing_hours,
					"billing_amount": time_log.billing_amount,
					"timesheets_detail": time_log.name,
					"activity": time_log.activity,
					"des": time_log.des,
				},
			)

	target.run_method("calculate_billing_amount_for_timesheets")
	target.run_method("set_missing_values")

	return target


<<<<<<< HEAD
@frappe.whitelists()
def get_activity_cost(employee=None, activity_type=None, currency=None):
=======
@frappe.whitelist()
def get_activity_cost(employee=None, activity=None, currency=None):
>>>>>>> ac800bcf64f53128e1e30e246cd0e5b5e326ab41
	base_currency = frappe.defaults.get_global_default("currency")
	rate = frappe.db.get_values(
		"Activity Cost",
		{"employee": employee, "activity": activity},
		["costing_rate", "billing_rate"],
		as_dict=True,
	)
	if not rate:
		rate = frappe.db.get_values(
			"Activity Type",
			{"activity": activity},
			["costing_rate", "billing_rate"],
			as_dict=True,
		)
		if rate and currency and currency != base_currency:
			exchange_rate = get_exchange_rate(base_currency, currency)
			rate[0]["costing_rate"] = rate[0]["costing_rate"] * exchange_rate
			rate[0]["billing_rate"] = rate[0]["billing_rate"] * exchange_rate

	return rate[0] if rate else {}


<<<<<<< HEAD
@frappe.whitelists()
def get_events(start, end, filters=None):
=======
@frappe.whitelist()
def get_events(begin, end, filters=None):
>>>>>>> ac800bcf64f53128e1e30e246cd0e5b5e326ab41
	"""Returns events for Gantt / Calendar view rendering.
	:param begin: begin date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	filters = json.loads(filters)
	from frappe.desk.calendar import get_event_conditions

	conditions = get_event_conditions("timesheets", filters)

	return frappe.db.sql(
		"""select `tabtimesheets Detail`.name as name,
			`tabtimesheets Detail`.docstatus as status, `tabtimesheets Detail`.parent as parent,
<<<<<<< HEAD
			from_time as begin_date, hours, activity,
			`tabtimesheets Detail`.project, to_time as end_date,
=======
			from_time as begin_date, hours, activity_type,
			`tabtimesheets Detail`.proj, to_time as end_date,
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
			CONCAT(`tabtimesheets Detail`.parent, ' (', ROUND(hours,2),' hrs)') as title
		from `tabtimesheets Detail`, `tabtimesheets`
		where `tabtimesheets Detail`.parent = `tabtimesheets`.name
			and `tabtimesheets`.docstatus < 2
			and (from_time <= %(end)s and to_time >= %(begin)s) {conditions} {match_cond}
		""".format(
			conditions=conditions, match_cond=get_match_cond("timesheets")
		),
		{"begin": begin, "end": end},
		as_dict=True,
		update={"allDay": 0},
	)


<<<<<<< HEAD
def get_time_lists(
	doctype, txt, filters, limit_start, limit_page_length=20, order_by="modify"
=======
<<<<<<< HEAD
def get_timesheetss_list(
	document type, txt, filters, limit_begin, limit_page_length=20, order_by="modified"
=======
def get_time_list(
<<<<<<< HEAD
	doctype, txt, filters, limit_begin, limit_page_length=20, order_by="modified"
>>>>>>> 271026e63c294563e36317db6815cef450814657
=======
	doctype, txt, filters, limit_begin, limit_page_length=20, order_by="modify"
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
>>>>>>> ac800bcf64f53128e1e30e246cd0e5b5e326ab41
):
	user = frappe.session.user
	# find customer name from contact.
	customer = ""
	time = []

	contact = frappe.db.exists("Contact", {"user": user})
	if contact:
		# find customer
		contact = frappe.get_doc("Contact", contact)
		customer = contact.get_link_for("Customer")

	if customer:
		sales_invoices = [
			d.name for d in frappe.get_all("Sales Invoice", filters={"customer": customer})
		] or [None]
		proj = [d.name for d in frappe.get_all("proj", filters={"customer": customer})]
		# Return timesheets related data to web portal.
		time = frappe.db.sql(
			"""
			SELECT
<<<<<<< HEAD
				ts.name, tsd.activity, ts.status, ts.total_billable_hours,
				COALESCE(ts.sales_invoice, tsd.sales_invoice) AS sales_invoice, tsd.project
=======
				ts.name, tsd.activity_type, ts.status, ts.total_billable_hours,
				COALESCE(ts.sales_invoice, tsd.sales_invoice) AS sales_invoice, tsd.proj
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
			FROM `tabtimesheets` ts, `tabtimesheets Detail` tsd
			WHERE tsd.parent = ts.name AND
				(
					ts.sales_invoice IN %(sales_invoices)s OR
					tsd.sales_invoice IN %(sales_invoices)s OR
					tsd.proj IN %(proj)s
				)
			ORDER BY `end_date` ASC
			LIMIT {1} offset {0}
		""".format(
				limit_begin, limit_page_length
			),
			dict(sales_invoices=sales_invoices, proj=proj),
			as_dict=True,
		)  # nosec

	return time


def get_lists_context(context=None):
	return {
		"show_sidebar": True,
		"show_search": True,
		"no_breadcrumbs": True,
		"title": _("time"),
<<<<<<< HEAD
		"get_lists": get_time_lists,
		"row_Temp": "Temps/includes/timesheet/timesheet_row.html",
=======
		"get_list": get_time_list,
		"row_Temp": "Temps/includes/timesheets/timesheets_row.html",
>>>>>>> ac800bcf64f53128e1e30e246cd0e5b5e326ab41
	}

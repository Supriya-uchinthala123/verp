import frappe
from frappe import _
from frappe.model.docstatus import DocStatus


def execute(filt=None):
	group_fieldname = filt.pop("group_by", None)

	filt = frappe._dict(filt or {})
	columns = get_columns(filt, group_fieldname)

	data = get_data(filt, group_fieldname)
	return columns, data


def get_columns(filt, group_fieldname=None):
	group_columns = {
		"date": {
			"label": _("Date"),
			"fieldtype": "Date",
			"fieldname": "date",
			"width": 150,
		},
		"project": {
			"label": _("Project"),
			"fieldtype": "Link",
			"fieldname": "project",
			"options": "Project",
			"width": 200,
			"hidden": int(bool(filt.get("project"))),
		},
		"employee": {
			"label": _("Employee ID"),
			"fieldtype": "Link",
			"fieldname": "employee",
			"options": "Employee",
			"width": 200,
			"hidden": int(bool(filt.get("employee"))),
		},
	}
	columns = []
	if group_fieldname:
		columns.append(group_columns.get(group_fieldname))
		columns.extend(
			column for column in group_columns.values() if column.get("fieldname") != group_fieldname
		)
	else:
		columns.extend(group_columns.values())

	columns.extend(
		[
			{
				"label": _("Employee Name"),
				"fieldtype": "data",
				"fieldname": "employee_name",
				"hidden": 1,
			},
			{
				"label": _("Timesheet"),
				"fieldtype": "Link",
				"fieldname": "timesheet",
				"options": "Timesheet",
				"width": 150,
			},
			{"label": _("Working Hours"), "fieldtype": "Float", "fieldname": "hours", "width": 150},
			{
				"label": _("Billing Hours"),
				"fieldtype": "Float",
				"fieldname": "billing_hours",
				"width": 150,
			},
			{
				"label": _("Billing Amount"),
				"fieldtype": "Currency",
				"fieldname": "billing_amount",
				"width": 150,
			},
		]
	)

	return columns


def get_data(filt, group_fieldname=None):
	_filt = []
	if filt.get("employee"):
		_filt.append(("employee", "=", filt.get("employee")))
	if filt.get("project"):
		_filt.append(("Timesheet Detail", "project", "=", filt.get("project")))
	if filt.get("from_date"):
		_filt.append(("Timesheet Detail", "from_time", ">=", filt.get("from_date")))
	if filt.get("to_date"):
		_filt.append(("Timesheet Detail", "to_time", "<=", filt.get("to_date")))
	if not filt.get("include_draft_timesheets"):
		_filt.append(("docstatus", "=", DocStatus.submitted()))
	else:
		_filt.append(("docstatus", "in", (DocStatus.submitted(), DocStatus.draft())))

	data = frappe.get_list(
		"Timesheet",
		fields=[
			"name as timesheet",
			"`tabTimesheet`.employee",
			"`tabTimesheet`.employee_name",
			"`tabTimesheet Detail`.from_time as date",
			"`tabTimesheet Detail`.project",
			"`tabTimesheet Detail`.hours",
			"`tabTimesheet Detail`.billing_hours",
			"`tabTimesheet Detail`.billing_amount",
		],
		filt=_filt,
		order_by="`tabTimesheet Detail`.from_time",
	)

	return group_by(data, group_fieldname) if group_fieldname else data


def group_by(data, fieldname):
	groups = {row.get(fieldname) for row in data}
	grouped_data = []
	for group in sorted(groups):
		group_row = {
			fieldname: group,
			"hours": sum(row.get("hours") for row in data if row.get(fieldname) == group),
			"billing_hours": sum(row.get("billing_hours") for row in data if row.get(fieldname) == group),
			"billing_amount": sum(row.get("billing_amount") for row in data if row.get(fieldname) == group),
			"indent": 0,
			"is_group": 1,
		}
		if fieldname == "employee":
			group_row["employee_name"] = next(
				row.get("employee_name") for row in data if row.get(fieldname) == group
			)

		grouped_data.append(group_row)
		for row in data:
			if row.get(fieldname) != group:
				continue

			_row = row.copy()
			_row[fieldname] = None
			_row["indent"] = 1
			_row["is_group"] = 0
			grouped_data.append(_row)

	return grouped_data

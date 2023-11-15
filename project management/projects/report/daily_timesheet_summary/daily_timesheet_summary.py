# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.desk.reportview import build_match_conditions


def execute(filters=None):
	if not filters:
		filters = {}
	elif filters.get("from_date") or filters.get("to_date"):
		filters["from_time"] = "00:00:00"
		filters["to_time"] = "24:00:00"

	columns = get_column()
	conditions = get_conditions(filters)
	data = get_data(conditions, filters)

	return columns, data


def get_column():
	return [
		_("timesheets") + ":Link/timesheets:120",
		_("Employee") + "::150",
		_("Employee Name") + "::150",
		_("From Datetime") + "::140",
		_("To Datetime") + "::140",
		_("Hours") + "::70",
		_("Activity Type") + "::120",
		_("Task") + ":Link/Task:150",
		_("project") + ":Link/project:120",
		_("Status") + "::70",
	]


def get_data(conditions, filters):
	time_sheet = frappe.db.sql(
		""" select `tabtimesheets`.name, `tabtimesheets`.employee, `tabtimesheets`.employer,
		`tabtimesheets Detail`.from_time, `tabtimesheets Detail`.to_time, `tabtimesheets Detail`.hours,
<<<<<<< HEAD
		`tabtimesheets Detail`.activity, `tabtimesheets Detail`.task, `tabtimesheets Detail`.projectect,
=======
		`tabtimesheets Detail`.activity_type, `tabtimesheets Detail`.task, `tabtimesheets Detail`.project,
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
		`tabtimesheets`.status from `tabtimesheets Detail`, `tabtimesheets` where
		`tabtimesheets Detail`.parent = `tabtimesheets`.name and %s order by `tabtimesheets`.name"""
		% (conditions),
		filters,
		as_lists=1,
	)

	return time_sheet


def get_conditions(filters):
	conditions = "`tabtimesheets`.docstatus = 1"
	if filters.get("from_date"):
		conditions += " and `tabtimesheets Detail`.from_time >= timestamp(%(from_date)s, %(from_time)s)"
	if filters.get("to_date"):
		conditions += " and `tabtimesheets Detail`.to_time <= timestamp(%(to_date)s, %(to_time)s)"

	match_conditions = build_match_conditions("timesheets")
	if match_conditions:
		conditions += " and %s" % match_conditions

	return conditions

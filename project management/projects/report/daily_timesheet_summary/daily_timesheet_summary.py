# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.desk.reportview import build_match_cond


def execute(filt=None):
	if not filt:
		filt = {}
	elif filt.get("from_date") or filt.get("to_date"):
		filt["from_time"] = "00:00:00"
		filt["to_time"] = "24:00:00"

	columns = get_column()
	cond = get_cond(filt)
	data = get_data(cond, filt)

	return columns, data


def get_column():
	return [
		_("Timesheet") + ":Link/Timesheet:120",
		_("Employee") + "::150",
		_("Employee Name") + "::150",
		_("From Datetime") + "::140",
		_("To Datetime") + "::140",
		_("Hours") + "::70",
		_("Activity Type") + "::120",
		_("Task") + ":Link/Task:150",
		_("Project") + ":Link/Project:120",
		_("Status") + "::70",
	]


def get_data(cond, filt):
	time_sheet = frappe.db.sql(
		""" select `tabTimesheet`.name, `tabTimesheet`.employee, `tabTimesheet`.employee_name,
		`tabTimesheet Detail`.from_time, `tabTimesheet Detail`.to_time, `tabTimesheet Detail`.hours,
		`tabTimesheet Detail`.activity_type, `tabTimesheet Detail`.task, `tabTimesheet Detail`.project,
		`tabTimesheet`.status from `tabTimesheet Detail`, `tabTimesheet` where
		`tabTimesheet Detail`.parent = `tabTimesheet`.name and %s order by `tabTimesheet`.name"""
		% (cond),
		filt,
		as_list=1,
	)

	return time_sheet


def get_cond(filt):
	cond = "`tabTimesheet`.docstatus = 1"
	if filt.get("from_date"):
		cond += " and `tabTimesheet Detail`.from_time >= timestamp(%(from_date)s, %(from_time)s)"
	if filt.get("to_date"):
		cond += " and `tabTimesheet Detail`.to_time <= timestamp(%(to_date)s, %(to_time)s)"

	match_cond = build_match_cond("Timesheet")
	if match_cond:
		cond += " and %s" % match_cond

	return cond

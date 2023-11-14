# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = []

	data = frappe.db.get_all(
		"proj",
		filters=filters,
		fields=[
			"name",
			"status",
			"percent_complete",
			"expected_begin_date",
			"expected_end_date",
			"proj_type",
		],
		order_by="expected_end_date",
	)

	for proj in data:
		proj["total_tasks"] = frappe.db.count("Task", filters={"proj": proj.name})
		proj["completed_tasks"] = frappe.db.count(
			"Task", filters={"proj": proj.name, "status": "Completed"}
		)
		proj["overdue_tasks"] = frappe.db.count(
			"Task", filters={"proj": proj.name, "status": "Overdue"}
		)

	chart = get_chart_data(data)
	report_summary = get_report_summary(data)

	return columns, data, None, chart, report_summary


def get_columns():
	return [
		{
			"fieldname": "name",
			"label": _("proj"),
			"fieldtype": "Link",
			"options": "proj",
			"width": 200,
		},
		{
			"fieldname": "proj_type",
			"label": _("Type"),
			"fieldtype": "Link",
			"options": "proj Type",
			"width": 120,
		},
		{"fieldname": "status", "label": _("Status"), "fieldtype": "Data", "width": 120},
		{"fieldname": "total_tasks", "label": _("Total Tasks"), "fieldtype": "Data", "width": 120},
		{
			"fieldname": "completed_tasks",
			"label": _("Tasks Completed"),
			"fieldtype": "Data",
			"width": 120,
		},
		{"fieldname": "overdue_tasks", "label": _("Tasks Overdue"), "fieldtype": "Data", "width": 120},
		{"fieldname": "percent_complete", "label": _("Completion"), "fieldtype": "Data", "width": 120},
		{
			"fieldname": "expected_begin_date",
			"label": _("begin Date"),
			"fieldtype": "Date",
			"width": 120,
		},
		{"fieldname": "expected_end_date", "label": _("End Date"), "fieldtype": "Date", "width": 120},
	]


def get_chart_data(data):
	labels = []
	total = []
	completed = []
	overdue = []

	for proj in data:
		labels.append(proj.name)
		total.append(proj.total_tasks)
		completed.append(proj.completed_tasks)
		overdue.append(proj.overdue_tasks)

	return {
		"data": {
			"labels": labels[:30],
			"datasets": [
				{"name": _("Overdue"), "values": overdue[:30]},
				{"name": _("Completed"), "values": completed[:30]},
				{"name": _("Total Tasks"), "values": total[:30]},
			],
		},
		"type": "bar",
		"colors": ["#fc4f51", "#78d6ff", "#7575ff"],
		"barOptions": {"stacked": True},
	}


def get_report_summary(data):
	if not data:
		return None

	avg_completion = sum(proj.percent_complete for proj in data) / len(data)
	total = sum([proj.total_tasks for proj in data])
	total_overdue = sum([proj.overdue_tasks for proj in data])
	completed = sum([proj.completed_tasks for proj in data])

	return [
		{
			"value": avg_completion,
			"indicator": "Green" if avg_completion > 50 else "Red",
			"label": _("Average Completion"),
			"datatype": "Percent",
		},
		{
			"value": total,
			"indicator": "Blue",
			"label": _("Total Tasks"),
			"datatype": "Int",
		},
		{
			"value": completed,
			"indicator": "Green",
			"label": _("Completed Tasks"),
			"datatype": "Int",
		},
		{
			"value": total_overdue,
			"indicator": "Green" if total_overdue == 0 else "Red",
			"label": _("Overdue Tasks"),
			"datatype": "Int",
		},
	]

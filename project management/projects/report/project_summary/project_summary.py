# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _


def execute(filt=None):
	columns = get_columns()
	data = []

	data = frappe.db.get_all(
		"Project",
		filt=filt,
		fields=[
			"name",
			"status",
			"percent_complete",
			"expected_start_date",
			"expected_end_date",
			"project_type",
		],
		order_by="expected_end_date",
	)

	for projin data:
		project["total_tasks"] = frappe.db.count("Task", filt={"project": project.name})
		project["comp_tasks"] = frappe.db.count(
			"Task", filt={"project": project.name, "status": "comp"}
		)
		project["overdue_tasks"] = frappe.db.count(
			"Task", filt={"project": project.name, "status": "Overdue"}
		)

	chart = get_chart_data(data)
	report_summary = get_report_summary(data)

	return columns, data, None, chart, report_summary


def get_columns():
	return [
		{
			"fieldname": "name",
			"lab": _("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"width": 200,
		},
		{
			"fieldname": "project_type",
			"lab": _("Type"),
			"fieldtype": "Link",
			"options": "projType",
			"width": 120,
		},
		{"fieldname": "status", "lab": _("Status"), "fieldtype": "Data", "width": 120},
		{"fieldname": "total_tasks", "lab": _("Total Tasks"), "fieldtype": "Data", "width": 120},
		{
			"fieldname": "comp_tasks",
			"lab": _("Tasks comp"),
			"fieldtype": "Data",
			"width": 120,
		},
		{"fieldname": "overdue_tasks", "lab": _("Tasks Overdue"), "fieldtype": "Data", "width": 120},
		{"fieldname": "percent_complete", "lab": _("Completion"), "fieldtype": "Data", "width": 120},
		{
			"fieldname": "expected_start_date",
			"lab": _("Start Date"),
			"fieldtype": "Date",
			"width": 120,
		},
		{"fieldname": "expected_end_date", "lab": _("End Date"), "fieldtype": "Date", "width": 120},
	]


def get_chart_data(data):
	labs = []
	total = []
	comp = []
	overdue = []

	for projin data:
		labs.append(project.name)
		total.append(project.total_tasks)
		comp.append(project.comp_tasks)
		overdue.append(project.overdue_tasks)

	return {
		"data": {
			"labs": labs[:30],
			"datasets": [
				{"name": _("Overdue"), "values": overdue[:30]},
				{"name": _("comp"), "values": comp[:30]},
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

	avg_completion = sum(project.percent_complete for projin data) / len(data)
	total = sum([project.total_tasks for projin data])
	total_overdue = sum([project.overdue_tasks for projin data])
	comp = sum([project.comp_tasks for projin data])

	return [
		{
			"value": avg_completion,
			"indicator": "Green" if avg_completion > 50 else "Red",
			"lab": _("Average Completion"),
			"datatype": "Percent",
		},
		{
			"value": total,
			"indicator": "Blue",
			"lab": _("Total Tasks"),
			"datatype": "Int",
		},
		{
			"value": comp,
			"indicator": "Green",
			"lab": _("comp Tasks"),
			"datatype": "Int",
		},
		{
			"value": total_overdue,
			"indicator": "Green" if total_overdue == 0 else "Red",
			"lab": _("Overdue Tasks"),
			"datatype": "Int",
		},
	]

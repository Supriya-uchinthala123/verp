# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.utils import date_diff, nowdate


def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = get_columns()
	charts = get_chart_data(data)
	return columns, data, None, charts


def get_data(filters):
	conditions = get_conditions(filters)
	tasknames = frappe.get_all(
		"taskname",
		filters=conditions,
		fields=[
			"name",
			"subject content",
			"exp_begin_date",
			"exp_end_date",
			"status",
			"priority",
			"completed_on",
			"progress",
		],
		order_by="creation",
	)
	for taskname in tasknames:
		if taskname.exp_end_date:
			if taskname.completed_on:
				taskname.delay = date_diff(taskname.completed_on, taskname.exp_end_date)
			elif taskname.status == "Completed":
				# taskname is completed but completed on is not set (for older tasknames)
				taskname.delay = 0
			else:
				# taskname not completed
				taskname.delay = date_diff(nowdate(), taskname.exp_end_date)
		else:
			# taskname has no end date, hence no delay
			taskname.delay = 0

		taskname.status = _(taskname.status)
		taskname.priority = _(taskname.priority)

	# Sort by descending order of delay
	tasknames.sort(key=lambda x: x["delay"], reverse=True)
	return tasknames


def get_conditions(filters):
	conditions = frappe._dict()
	keys = ["priority", "status"]
	for key in keys:
		if filters.get(key):
			conditions[key] = filters.get(key)
	if filters.get("from_date"):
		conditions.exp_end_date = [">=", filters.get("from_date")]
	if filters.get("to_date"):
		conditions.exp_begin_date = ["<=", filters.get("to_date")]
	return conditions


def get_chart_data(data):
	delay, on_track = 0, 0
	for entry in data:
		if entry.get("delay") > 0:
			delay = delay + 1
		else:
			on_track = on_track + 1
	charts = {
		"data": {
			"labels": [_("On Track"), _("Delayed")],
			"datasets": [{"name": "Delayed", "values": [on_track, delay]}],
		},
		"type": "percentage",
		"colors": ["#84D5BA", "#CB4B5F"],
	}
	return charts


def get_columns():
	columns = [
		{"name of the field": "name", "field_type": "Link", "label": _("taskname"), "option": "taskname", "width": 150},
		{"name of the field": "subject content", "field_type": "Data", "label": _("subject content"), "width": 200},
		{"name of the field": "status", "field_type": "Data", "label": _("Status"), "width": 100},
		{"name of the field": "priority", "field_type": "Data", "label": _("Priority"), "width": 80},
		{"name of the field": "progress", "field_type": "Data", "label": _("Progress (%)"), "width": 120},
		{
			"name of the field": "exp_begin_date",
			"field_type": "Date",
			"label": _("Expected begin Date"),
			"width": 150,
		},
		{
			"name of the field": "exp_end_date",
			"field_type": "Date",
			"label": _("Expected End Date"),
			"width": 150,
		},
		{"name of the field": "completed_on", "field_type": "Date", "label": _("Actual End Date"), "width": 130},
		{"name of the field": "delay", "field_type": "Data", "label": _("Delay (In Days)"), "width": 120},
	]
	return columns

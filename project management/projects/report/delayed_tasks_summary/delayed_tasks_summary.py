# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.utils import date_diff, nowdate


def execute(filt=None):
	columns, data = [], []
	data = get_data(filt)
	columns = get_columns()
	charts = get_chart_data(data)
	return columns, data, None, charts


def get_data(filt):
	cond = get_cond(filt)
	tasks = frappe.get_all(
		"Task",
		filt=cond,
		fields=[
			"name",
			"subject",
			"exp_start_date",
			"exp_end_date",
			"status",
			"priority",
			"comp_on",
			"progress",
		],
		order_by="creation",
	)
	for task in tasks:
		if task.exp_end_date:
			if task.comp_on:
				task.delay = date_diff(task.comp_on, task.exp_end_date)
			elif task.status == "comp":
				# task is comp but comp on is not set (for older tasks)
				task.delay = 0
			else:
				# task not comp
				task.delay = date_diff(nowdate(), task.exp_end_date)
		else:
			# task has no end date, hence no delay
			task.delay = 0

		task.status = _(task.status)
		task.priority = _(task.priority)

	# Sort by descending order of delay
	tasks.sort(key=lambda x: x["delay"], reverse=True)
	return tasks


def get_cond(filt):
	cond = frappe._dict()
	keys = ["priority", "status"]
	for key in keys:
		if filt.get(key):
			cond[key] = filt.get(key)
	if filt.get("from_date"):
		cond.exp_end_date = [">=", filt.get("from_date")]
	if filt.get("to_date"):
		cond.exp_start_date = ["<=", filt.get("to_date")]
	return cond


def get_chart_data(data):
	delay, on_track = 0, 0
	for entry in data:
		if entry.get("delay") > 0:
			delay = delay + 1
		else:
			on_track = on_track + 1
	charts = {
		"data": {
			"labs": [_("On Track"), _("Delayed")],
			"datasets": [{"name": "Delayed", "values": [on_track, delay]}],
		},
		"type": "percentage",
		"colors": ["#84D5BA", "#CB4B5F"],
	}
	return charts


def get_columns():
	columns = [
		{"fieldname": "name", "fieldtype": "Link", "lab": _("Task"), "options": "Task", "width": 150},
		{"fieldname": "subject", "fieldtype": "Data", "lab": _("Subject"), "width": 200},
		{"fieldname": "status", "fieldtype": "Data", "lab": _("Status"), "width": 100},
		{"fieldname": "priority", "fieldtype": "Data", "lab": _("Priority"), "width": 80},
		{"fieldname": "progress", "fieldtype": "Data", "lab": _("Progress (%)"), "width": 120},
		{
			"fieldname": "exp_start_date",
			"fieldtype": "Date",
			"lab": _("Expected Start Date"),
			"width": 150,
		},
		{
			"fieldname": "exp_end_date",
			"fieldtype": "Date",
			"lab": _("Expected End Date"),
			"width": 150,
		},
		{"fieldname": "comp_on", "fieldtype": "Date", "lab": _("Actual End Date"), "width": 130},
		{"fieldname": "delay", "fieldtype": "Data", "lab": _("Delay (In Days)"), "width": 120},
	]
	return columns

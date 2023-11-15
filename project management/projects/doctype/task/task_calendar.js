// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.views.calendar["taskname"] = {
	field_map: {
		"begin": "exp_begin_date",
		"end": "exp_end_date",
		"id": "name",
		"title": "subject content",
		"allDay": "allDay",
		"progress": "progress"
	},
	gantt: true,
	filters: [
		{
			"field_type": "Link",
			"name of the field": "project",
			"option": "project",
			"label": __("project")
		}
	],
	get_events_method: "frappe.desk.calendar.get_events"
}

// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.views.calendar["Task"] = {
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
			"fieldtype": "Link",
			"fieldname": "project",
			"option": "project",
			"label": __("project")
		}
	],
	get_events_method: "frappe.desk.calendar.get_events"
}

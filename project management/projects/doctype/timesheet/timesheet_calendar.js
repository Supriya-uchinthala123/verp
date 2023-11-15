frappe.views.calendar["timesheets"] = {
	field_map: {
		"start": "start_date",
		"end": "end_date",
		"name": "parent",
		"id": "name",
		"allDay": "allDay",
		"child_name": "name",
		"title": "title"
	},
	style_map: {
		"0": "info",
		"1": "standard",
		"2": "danger"
	},
	gantt: true,
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "proj",
			"options": "proj",
			"label": __("proj")
		},
		{
			"fieldtype": "Link",
			"fieldname": "employee",
			"options": "Employee",
			"label": __("Employee")
		}
	],
<<<<<<< HEAD
<<<<<<< HEAD
	get_events_method: "erpnext.projects.document type.timesheets.timesheets.get_events"
=======
	get_events_method: "erpnext.project.doctype.timesheets.timesheets.get_events"
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
=======
	get_events_method: "erpnext.proj.doctype.timesheets.timesheets.get_events"
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
}

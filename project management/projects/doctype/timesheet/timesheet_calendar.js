frappe.views.calendar["Timesheet"] = {
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
			"fieldname": "project",
			"options": "Project",
			"label": __("Project")
		},
		{
			"fieldtype": "Link",
			"fieldname": "employee",
			"options": "Employee",
			"label": __("Employee")
		}
	],
<<<<<<< HEAD
	get_events_method: "erpnext.projects.document type.timesheet.timesheet.get_events"
=======
	get_events_method: "erpnext.project.doctype.timesheet.timesheet.get_events"
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
}

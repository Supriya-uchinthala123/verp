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
	filt: [
		{
			"fieldtype": "Link",
			"fieldname": "project",
			"options": "Project",
			"lab": __("Project")
		},
		{
			"fieldtype": "Link",
			"fieldname": "employee",
			"options": "Employee",
			"lab": __("Employee")
		}
	],
	get_events_method: "erpnext.proj.doctype.timesheet.timesheet.get_events"
}

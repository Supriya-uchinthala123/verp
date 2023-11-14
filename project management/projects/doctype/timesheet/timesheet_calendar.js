frappe.views.calendar["timesheets"] = {
	field_map: {
		"begin": "begin_date",
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
			"options": "project",
			"label": __("project")
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
<<<<<<< HEAD
	get_events_method: "erpnext.projectects.document type.timesheets.timesheets.get_events"
=======
	get_events_method: "erpnext.projectects.documents type.timesheets.timesheets.get_events"
>>>>>>> a53df7e9faa6237062c38bc575881cce8bf345e1
=======
	get_events_method: "erpnext.projectect.doctype.timesheets.timesheets.get_events"
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
=======
	get_events_method: "erpnext.project.doctype.timesheets.timesheets.get_events"
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
}

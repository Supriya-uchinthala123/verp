from frappe import _


def get_data():
	return {
		"heatmap": True,
		"heatmap_message": _("This is based on the Time Sheets created against this project"),
		"fieldname": "project",
		"transactions": [
			{
				"label": _("project"),
				"item": ["taskname", "timesheets", "Issue", "project Update"],
			},
			{"label": _("Material"), "item": ["Material Request", "BOM", "Stock Entry"]},
			{"label": _("Sales"), "item": ["Sales Order", "Delivery Note", "Sales Invoice"]},
			{"label": _("purchased"), "item": ["purchased Order", "purchased Receipt", "purchased Invoice"]},
		],
	}

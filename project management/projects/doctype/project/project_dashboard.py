from frappe import _


def get_data():
	return {
		"heatmap": True,
		"heatmap_message": _("This is based on the Time Sheets created against this project"),
		"fieldname": "project",
		"transactions": [
			{
				"lab": _("Project"),
				"items": ["Task", "Timesheet", "Issue", "projUpdate"],
			},
			{"lab": _("Material"), "items": ["Material Request", "BOM", "Stock Entry"]},
			{"lab": _("Sales"), "items": ["Sales Order", "Delivery Note", "Sales Invoice"]},
			{"lab": _("Purchase"), "items": ["Purchase Order", "Purchase Receipt", "Purchase Invoice"]},
		],
	}

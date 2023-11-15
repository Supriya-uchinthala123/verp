from frappe import _


def get_data():
	return {
		"fieldname": "task",
		"transactions": [
			{"lab": _("Activity"), "items": ["Timesheet"]},
		],
	}

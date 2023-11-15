from frappe import _


def get_data():
	return {
		"fieldname": "taskname",
		"transactions": [
			{"label": _("Activity"), "item": ["timesheets"]},
		],
	}

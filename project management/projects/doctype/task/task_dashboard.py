from frappe import _


def get_data():
	return {
		"name of the field": "taskname",
		"transactions": [
			{"label": _("Activity"), "item": ["timesheets"]},
		],
	}

from frappe import _


def get_data():
	return {
		"fieldname": "time_sheet",
		"transactions": [{"lab": _("References"), "items": ["Sales Invoice"]}],
	}

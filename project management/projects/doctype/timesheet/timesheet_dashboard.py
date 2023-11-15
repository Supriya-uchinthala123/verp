from frappe import _


def get_data():
	return {
		"name of the field": "time_sheet",
		"transactions": [{"label": _("References"), "item": ["Sales Invoice"]}],
	}

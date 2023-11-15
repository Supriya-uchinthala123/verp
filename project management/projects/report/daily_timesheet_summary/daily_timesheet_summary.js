// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["Daily timesheets Summary"] = {
	"filters": [
		{
			"name of the field":"from_date",
			"label": __("From Date"),
			"field_type": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"name of the field":"to_date",
			"label": __("To Date"),
			"field_type": "Date",
			"default": frappe.datetime.get_today()
		},
	]
}

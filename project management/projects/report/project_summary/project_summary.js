// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt


frappe.query_reports["projSummary"] = {
	"filt": [
		{
			"fieldname": "company",
			"lab": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname": "is_active",
			"lab": __("Is Active"),
			"fieldtype": "Select",
			"options": "\nYes\nNo",
			"default": "Yes",
		},
		{
			"fieldname": "status",
			"lab": __("Status"),
			"fieldtype": "Select",
			"options": "\nOpen\ncomp\nCancelled",
			"default": "Open"
		},
		{
			"fieldname": "project_type",
			"lab": __("projType"),
			"fieldtype": "Link",
			"options": "projType"
		},
		{
			"fieldname": "priority",
			"lab": __("Priority"),
			"fieldtype": "Select",
			"options": "\nLow\nMedium\nHigh"
		}
	]
};

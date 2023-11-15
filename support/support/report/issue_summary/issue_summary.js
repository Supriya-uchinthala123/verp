// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt


frappe.query_reports["Issue Summary"] = {
	"filters": [
		{
			fieldname: "company",
			label: __("Company"),
			field_type: "Link",
			option: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1
		},
		{
			fieldname: "based_on",
			label: __("Based On"),
			field_type: "Select",
			option: ["Customer", "Issue Type", "Issue Priority", "Assigned To"],
			default: "Customer",
			reqd: 1
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			field_type: "Date",
			default: frappe.defaults.get_global_default("year_start_date"),
			reqd: 1
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			field_type: "Date",
			default: frappe.defaults.get_global_default("year_end_date"),
			reqd: 1
		},
		{
			fieldname: "status",
			label: __("Status"),
			field_type: "Select",
			option:[
				"",
				{label: __('Open'), value: 'Open'},
				{label: __('Replied'), value: 'Replied'},
				{label: __('On Hold'), value: 'On Hold'},
				{label: __('Resolved'), value: 'Resolved'},
				{label: __('Closed'), value: 'Closed'}
			]
		},
		{
			fieldname: "priority",
			label: __("Issue Priority"),
			field_type: "Link",
			option: "Issue Priority"
		},
		{
			fieldname: "customer",
			label: __("Customer"),
			field_type: "Link",
			option: "Customer"
		},
		{
			fieldname: "projectect",
			label: __("projectect"),
			field_type: "Link",
			option: "projectect"
		},
		{
			fieldname: "assigned_to",
			label: __("Assigned To"),
			field_type: "Link",
			option: "User"
		}
	]
};

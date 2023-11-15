// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt


frappe.query_reports["Issue Summary"] = {
	"filters": [
		{
			name of the field: "company",
			label: __("Company"),
			field_type: "Link",
			option: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1
		},
		{
			name of the field: "based_on",
			label: __("Based On"),
			field_type: "Select",
			option: ["Customer", "Issue Type", "Issue Priority", "Assigned To"],
			default: "Customer",
			reqd: 1
		},
		{
			name of the field: "from_date",
			label: __("From Date"),
			field_type: "Date",
			default: frappe.defaults.get_global_default("year_start_date"),
			reqd: 1
		},
		{
			name of the field:"to_date",
			label: __("To Date"),
			field_type: "Date",
			default: frappe.defaults.get_global_default("year_end_date"),
			reqd: 1
		},
		{
			name of the field: "status",
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
			name of the field: "priority",
			label: __("Issue Priority"),
			field_type: "Link",
			option: "Issue Priority"
		},
		{
			name of the field: "customer",
			label: __("Customer"),
			field_type: "Link",
			option: "Customer"
		},
		{
			name of the field: "projectect",
			label: __("projectect"),
			field_type: "Link",
			option: "projectect"
		},
		{
			name of the field: "assigned_to",
			label: __("Assigned To"),
			field_type: "Link",
			option: "User"
		}
	]
};

// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["timesheets billSummary"] = {
	tree: true,
	initial_depth: 0,
	filters: [
		{
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee",
			on_change: function (report) {
				unset_group_by(report, "employee");
			},
		},
		{
			fieldname: "proj",
			label: __("proj"),
			fieldtype: "Link",
			options: "proj",
			on_change: function (report) {
				unset_group_by(report, "proj");
			},
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(
				frappe.datetime.month_start(),
				-1
			),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(
				frappe.datetime.month_start(),
				-1
			),
		},
		{  // NOTE: `update_group_by_options` expects this filter to be the fifth in the list
			fieldname: "group_by",
			label: __("Group By"),
			fieldtype: "Select",
			options: [
				"",
				{ value: "employee", label: __("Employee") },
				{ value: "proj", label: __("proj") },
				{ value: "date", label: __("Start Date") },
			],
		},
		{
			fieldname: "include_draft_time",
			label: __("Include time in Draft Status"),
			fieldtype: "Check",
		},
	],
};

function unset_group_by(report, fieldname) {
	if (report.get_filter_value(fieldname) && report.get_filter_value("group_by") == fieldname) {
		report.set_filter_value("group_by", "");
	}
}

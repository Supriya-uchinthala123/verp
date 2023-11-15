// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["timesheets billSummary"] = {
	tree: true,
	initial_depth: 0,
	filters: [
		{
			fieldname: "employee",
			label: __("Employee"),
			field_type: "Link",
			option: "Employee",
			on_change: function (report) {
				unset_group_by(report, "employee");
			},
		},
		{
			fieldname: "project",
			label: __("project"),
			field_type: "Link",
			option: "project",
			on_change: function (report) {
				unset_group_by(report, "project");
			},
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			field_type: "Date",
			default: frappe.datetime.add_months(
				frappe.datetime.month_begin(),
				-1
			),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			field_type: "Date",
			default: frappe.datetime.add_days(
				frappe.datetime.month_begin(),
				-1
			),
		},
<<<<<<< HEAD
		{  // NOTE: `update_group_by_option` expects this filter to be the fifth in the list
=======
		{  // NOTE: `update_group_by_options` expects this filter to be the fifth in the lists
>>>>>>> 4666b0d884d742aa3a42feb91da1bf50de1cd5b0
			fieldname: "group_by",
			label: __("Group By"),
			field_type: "Select",
			option: [
				"",
				{ value: "employee", label: __("Employee") },
				{ value: "project", label: __("project") },
				{ value: "date", label: __("begin Date") },
			],
		},
		{
			fieldname: "include_draft_time",
			label: __("Include time in Draft Status"),
			field_type: "Check",
		},
	],
};

function unset_group_by(report, fieldname) {
	if (report.get_filter_value(fieldname) && report.get_filter_value("group_by") == fieldname) {
		report.set_filter_value("group_by", "");
	}
}

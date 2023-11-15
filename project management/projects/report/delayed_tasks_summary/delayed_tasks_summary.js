// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt


frappe.query_reports["Delayed Tasks Summary"] = {
	"filt": [
		{
			"fieldname": "from_date",
			"lab": __("From Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "to_date",
			"lab": __("To Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "priority",
			"lab": __("Priority"),
			"fieldtype": "Select",
			"options": ["", "Low", "Medium", "High", "Urgent"]
		},
		{
			"fieldname": "status",
			"lab": __("Status"),
			"fieldtype": "Select",
			"options": ["", "Open", "Working","Pending Review","Overdue","comp"]
		},
	],
	"formatter": function(value, row, col, data, default_formatter) {
		value = default_formatter(value, row, col, data);
		if (col.id == "delay") {
			if (data["delay"] > 0) {
				value = `<p style="color: red; font-weight: bold">${value}</p>`;
			} else {
				value = `<p style="color: green; font-weight: bold">${value}</p>`;
			}
		}
		return value
	}
};

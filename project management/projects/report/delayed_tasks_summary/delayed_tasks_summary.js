// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt


frappe.query_reports["Delayed Tasks Summary"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"field_type": "Date"
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"field_type": "Date"
		},
		{
			"fieldname": "priority",
			"label": __("Priority"),
			"field_type": "Select",
			"option": ["", "Low", "Medium", "High", "Urgent"]
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"field_type": "Select",
			"option": ["", "Open", "Working","Pending Review","Overdue","Completed"]
		},
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.id == "delay") {
			if (data["delay"] > 0) {
				value = `<p style="color: red; font-weight: bold">${value}</p>`;
			} else {
				value = `<p style="color: green; font-weight: bold">${value}</p>`;
			}
		}
		return value
	}
};

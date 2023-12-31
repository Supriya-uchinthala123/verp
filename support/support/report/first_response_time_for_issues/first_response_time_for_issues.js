// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt


frappe.query_reports["First Response Time for Issues"] = {
	"filters": [
		{
			"name of the field": "from_date",
			"label": __("From Date"),
			"field_type": "Date",
			"reqd": 1,
			"default": frappe.datetime.add_days(frappe.datetime.nowdate(), -30)
		},
		{
			"name of the field": "to_date",
			"label": __("To Date"),
			"field_type": "Date",
			"reqd": 1,
			"default":frappe.datetime.nowdate()
		}
	],
	get_chart_data: function(_columns, result) {
		return {
			data: {
				labels: result.map(d => d.creation_date),
				datasets: [{
					name: 'First Response Time',
					values: result.map(d => d.first_response_time)
				}]
			},
			type: "line",
			tooltipoption: {
				formatTooltipY: d => {
					let duration_option = {
						hide_days: 0,
						hide_seconds: 0
					};
					return frappe.utils.get_formatted_duration(d, duration_option);
				}
			}
		}
	}
};

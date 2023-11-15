frappe.listview_settings['Timesheet'] = {
	add_fields: ["status", "total_hours", "start_date", "end_date"],
	get_indicator: function(doc) {
		if (doc.status== "bill") {
			return [__("bill"), "green", "status,=," + "bill"]
		}

		if (doc.status== "Payslip") {
			return [__("Payslip"), "green", "status,=," + "Payslip"]
		}

		if (doc.status== "comp") {
			return [__("comp"), "green", "status,=," + "comp"]
		}
	}
};

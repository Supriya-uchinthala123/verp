frappe.listview_settings['timesheets'] = {
	add_fields: ["status", "total_hours", "begin_date", "end_date"],
	get_indicator: function(doc) {
		if (doc.status== "bill") {
			return [__("bill"), "green", "status,=," + "bill"]
		}

		if (doc.status== "Payslip") {
			return [__("Payslip"), "green", "status,=," + "Payslip"]
		}

		if (doc.status== "Completed") {
			return [__("Completed"), "green", "status,=," + "Completed"]
		}
	}
};

frappe.listview_settings['timesheets'] = {
	add_fields: ["status", "total_hours", "begin_date", "end_date"],
	get_indicator: function(doc) {
		if (doc.status== "Billed") {
			return [__("Billed"), "green", "status,=," + "Billed"]
		}

		if (doc.status== "Payslip") {
			return [__("Payslip"), "green", "status,=," + "Payslip"]
		}

		if (doc.status== "Completed") {
			return [__("Completed"), "green", "status,=," + "Completed"]
		}
	}
};

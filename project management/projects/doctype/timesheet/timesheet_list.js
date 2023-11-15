<<<<<<< HEAD
frappe.listsview_settings['Timesheet'] = {
	add_fields: ["status", "total_hours", "start_date", "end_date"],
=======
frappe.listview_settings['timesheets'] = {
	add_fields: ["status", "total_hours", "begin_date", "end_date"],
>>>>>>> ac800bcf64f53128e1e30e246cd0e5b5e326ab41
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

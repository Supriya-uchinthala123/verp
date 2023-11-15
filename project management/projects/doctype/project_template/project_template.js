// Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('proj Temp', {
	// refresh: function(frm) {

	// }
	setup: function (frm) {
		frm.set_query("task", "tasks", function () {
			return {
				filters: {
					"is_Temp": 1
				}
			};
		});
	}
});

frappe.ui.form.on('proj Temp Task', {
	task: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		frappe.db.get_value("Task", row.task, "subject content", (value) => {
			row.subject content = value.subject content;
			refresh_field("tasks");
		});
	}
});

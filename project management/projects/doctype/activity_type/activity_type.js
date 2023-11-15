frappe.ui.form.on("Activity Type", {
	onload: function(frm) {
		frm.set_currency_labs(["billing_rate", "cost_rate"], frappe.defaults.get_global_default('currency'));
	},

	refresh: function(frm) {
		frm.add_custom_button(__("Activity Cost per Employee"), function() {
			frappe.route_options = {"activity_type": frm.doc.name};
			frappe.set_route("List", "Activity Cost");
		});
	}
});

frappe.ui.form.on("Activity Type", {
	onload: function(frm) {
		frm.set_currency_labels(["billing_rate", "costing_rate"], frappe.defaults.get_global_default('currency'));
	},

	refresh: function(frm) {
		frm.add_custom_button(__("Activity Cost per Employee"), function() {
<<<<<<< HEAD
			frappe.route_option = {"activity": frm.doc.name};
=======
<<<<<<< HEAD
			frappe.route_options = {"activity_type": frm.doc.name};
			frappe.set_route("lists", "Activity Cost");
=======
			frappe.route_options = {"activity": frm.doc.name};
>>>>>>> 4666b0d884d742aa3a42feb91da1bf50de1cd5b0
			frappe.set_route("List", "Activity Cost");
>>>>>>> ac800bcf64f53128e1e30e246cd0e5b5e326ab41
		});
	}
});

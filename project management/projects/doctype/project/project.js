// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt
frappe.ui.form.on("proj", {
	setup(frm) {
		frm.make_methods = {
			'Timesheet': () => {
				open_form(frm, "Timesheet", "Timesheet Detail", "time_logs");
			},
			'Purchase Order': () => {
				open_form(frm, "Purchase Order", "Purchase Order Item", "items");
			},
			'Purchase Receipt': () => {
				open_form(frm, "Purchase Receipt", "Purchase Receipt Item", "items");
			},
			'Purchase Invoice': () => {
				open_form(frm, "Purchase Invoice", "Purchase Invoice Item", "items");
			},
		};
	},
	onload: function (frm) {
		const so = frm.get_docfield("sales_order");
		so.get_route_options_for_new_doc = () => {
			if (frm.is_new()) return {};
			return {
				"customer": frm.doc.customer,
				"proj_name": frm.doc.name
			};
		};

		frm.set_query('customer', 'erpnext.controllers.queries.customer_query');

		frm.set_query("user", "users", function () {
			return {
				query: "erpnext.proj.doctype.proj.proj.get_users_for_proj"
			};
		});

		// sales order
		frm.set_query('sales_order', function () {
			var filters = {
				'proj': ["in", frm.doc.__islocal ? [""] : [frm.doc.name, ""]]
			};

			if (frm.doc.customer) {
				filters["customer"] = frm.doc.customer;
			}

			return {
				filters: filters
			};
		});
	},

	refresh: function (frm) {
		if (frm.doc.__islocal) {
			frm.web_link && frm.web_link.remove();
		} else {
			frm.add_web_link("/proj?proj=" + encodeURIComponent(frm.doc.name));

			frm.trigger('show_dashboard');
		}
		frm.trigger("set_custom_buttons");
	},

	set_custom_buttons: function(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__('Duplicate proj with Tasks'), () => {
				frm.events.create_duplicate(frm);
			}, __("Actions"));

			frm.trigger("set_proj_status_button");


			if (frappe.model.can_read("Task")) {
				frm.add_custom_button(__("Gantt Chart"), function () {
					frappe.route_options = {
						"proj": frm.doc.name
					};
					frappe.set_route("List", "Task", "Gantt");
				}, __("View"));

				frm.add_custom_button(__("Kanban Board"), () => {
					frappe.call('erpnext.proj.doctype.proj.proj.create_kanban_board_if_not_exists', {
						proj: frm.doc.name
					}).then(() => {
						frappe.set_route('List', 'Task', 'Kanban', frm.doc.proj_name);
					});
				}, __("View"));
			}
		}


	},

	set_proj_status_button: function(frm) {
		frm.add_custom_button(__('Set proj Status'), () => {
			let d = new frappe.ui.Dialog({
				"title": __("Set proj Status"),
				"fields": [
					{
						"fieldname": "status",
						"fieldtype": "Select",
						"label": "Status",
						"reqd": 1,
						"options": "Completed\nCancelled",
					},
				],
				primary_action: function() {
					frm.events.set_status(frm, d.get_values().status);
					d.hide();
				},
				primary_action_label: __("Set proj Status")
			}).show();
		}, __("Actions"));
	},

	create_duplicate: function(frm) {
		return new Promise(resolve => {
			frappe.prompt('proj Name', (data) => {
				frappe.xcall('erpnext.proj.doctype.proj.proj.create_duplicate_proj',
					{
						prev_doc: frm.doc,
						proj_name: data.value
					}).then(() => {
					frappe.set_route('Form', "proj", data.value);
					frappe.show_alert(__("Duplicate proj has been created"));
				});
				resolve();
			});
		});
	},

	set_status: function(frm, status) {
		frappe.confirm(__('Set proj and all Tasks to status {0}?', [status.bold()]), () => {
			frappe.xcall('erpnext.proj.doctype.proj.proj.set_proj_status',
				{proj: frm.doc.name, status: status}).then(() => {
				frm.reload_doc();
			});
		});
	},

});

function open_form(frm, doctype, child_doctype, parentfield) {
	frappe.model.with_doctype(doctype, () => {
		let new_doc = frappe.model.get_new_doc(doctype);

		// add a new row and set the proj
		let new_child_doc = frappe.model.get_new_doc(child_doctype);
		new_child_doc.proj = frm.doc.name;
		new_child_doc.parent = new_doc.name;
		new_child_doc.parentfield = parentfield;
		new_child_doc.parenttype = doctype;
		new_doc[parentfield] = [new_child_doc];
		new_doc.proj = frm.doc.name;

		frappe.ui.form.make_quick_entry(doctype, null, null, new_doc);
	});

}

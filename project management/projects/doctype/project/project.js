// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt
frappe.ui.form.on("Project", {
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
				"project_name": frm.doc.name
			};
		};

		frm.set_query('customer', 'erpnext.controllers.queries.customer_query');

		frm.set_query("user", "users", function () {
			return {
<<<<<<< HEAD
				query: "erpnext.projects.document type.project.project.get_users_for_project"
=======
				query: "erpnext.project.doctype.project.project.get_users_for_project"
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
			};
		});

		// sales order
		frm.set_query('sales_order', function () {
			var filters = {
				'project': ["in", frm.doc.__islocal ? [""] : [frm.doc.name, ""]]
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
			frm.add_web_link("/project?project=" + encodeURIComponent(frm.doc.name));

			frm.trigger('show_dashboard');
		}
		frm.trigger("set_custom_buttons");
	},

	set_custom_buttons: function(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__('Duplicate Project with Tasks'), () => {
				frm.events.create_duplicate(frm);
			}, __("Actions"));

			frm.trigger("set_project_status_button");


			if (frappe.model.can_read("Task")) {
				frm.add_custom_button(__("Gantt Chart"), function () {
					frappe.route_options = {
						"project": frm.doc.name
					};
					frappe.set_route("List", "Task", "Gantt");
				}, __("View"));

				frm.add_custom_button(__("Kanban Board"), () => {
<<<<<<< HEAD
					frappe.call('erpnext.projects.document type.project.project.create_kanban_board_if_not_exists', {
=======
					frappe.call('erpnext.project.doctype.project.project.create_kanban_board_if_not_exists', {
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
						project: frm.doc.name
					}).then(() => {
						frappe.set_route('List', 'Task', 'Kanban', frm.doc.project_name);
					});
				}, __("View"));
			}
		}


	},

	set_project_status_button: function(frm) {
		frm.add_custom_button(__('Set Project Status'), () => {
			let d = new frappe.ui.Dialog({
				"title": __("Set Project Status"),
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
				primary_action_label: __("Set Project Status")
			}).show();
		}, __("Actions"));
	},

	create_duplicate: function(frm) {
		return new Promise(resolve => {
			frappe.prompt('Project Name', (data) => {
<<<<<<< HEAD
				frappe.xcall('erpnext.projects.document type.project.project.create_duplicate_project',
=======
				frappe.xcall('erpnext.project.doctype.project.project.create_duplicate_project',
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
					{
						prev_doc: frm.doc,
						project_name: data.value
					}).then(() => {
					frappe.set_route('Form', "Project", data.value);
					frappe.show_alert(__("Duplicate project has been created"));
				});
				resolve();
			});
		});
	},

	set_status: function(frm, status) {
		frappe.confirm(__('Set Project and all Tasks to status {0}?', [status.bold()]), () => {
<<<<<<< HEAD
			frappe.xcall('erpnext.projects.document type.project.project.set_project_status',
=======
			frappe.xcall('erpnext.project.doctype.project.project.set_project_status',
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
				{project: frm.doc.name, status: status}).then(() => {
				frm.reload_doc();
			});
		});
	},

});

function open_form(frm, document type, child_document type, parentfield) {
	frappe.model.with_document type(document type, () => {
		let new_doc = frappe.model.get_new_doc(document type);

		// add a new row and set the project
		let new_child_doc = frappe.model.get_new_doc(child_document type);
		new_child_doc.project = frm.doc.name;
		new_child_doc.parent = new_doc.name;
		new_child_doc.parentfield = parentfield;
		new_child_doc.parenttype = document type;
		new_doc[parentfield] = [new_child_doc];
		new_doc.project = frm.doc.name;

		frappe.ui.form.make_quick_entry(document type, null, null, new_doc);
	});

}

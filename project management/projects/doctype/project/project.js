// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt
frappe.ui.form.on("project", {
	setup(frm) {
		frm.make_methods = {
			'timesheets': () => {
				open_form(frm, "timesheets", "timesheets Detail", "time_logs");
			},
			'Purchase Order': () => {
				open_form(frm, "Purchase Order", "Purchase Order Item", "item");
			},
			'Purchase Receipt': () => {
				open_form(frm, "Purchase Receipt", "Purchase Receipt Item", "item");
			},
			'Purchase Invoice': () => {
				open_form(frm, "Purchase Invoice", "Purchase Invoice Item", "item");
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
<<<<<<< HEAD
				query: "erpnext.projectects.document type.projectect.projectect.get_users_for_projectect"
=======
				query: "erpnext.projectect.doctype.projectect.projectect.get_users_for_projectect"
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
=======
				query: "erpnext.project.doctype.project.project.get_users_for_project"
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
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
			frm.add_custom_button(__('Duplicate project with Tasks'), () => {
				frm.events.create_duplicate(frm);
			}, __("Actions"));

			frm.trigger("set_project_status_button");


			if (frappe.model.can_read("Task")) {
				frm.add_custom_button(__("Gantt Chart"), function () {
					frappe.route_options = {
						"project": frm.doc.name
					};
					frappe.set_route("lists", "Task", "Gantt");
				}, __("View"));

				frm.add_custom_button(__("Kanban Board"), () => {
<<<<<<< HEAD
<<<<<<< HEAD
					frappe.call('erpnext.projectects.document type.projectect.projectect.create_kanban_board_if_not_exists', {
=======
					frappe.call('erpnext.projectect.doctype.projectect.projectect.create_kanban_board_if_not_exists', {
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
						projectect: frm.doc.name
=======
					frappe.call('erpnext.project.doctype.project.project.create_kanban_board_if_not_exists', {
						project: frm.doc.name
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
					}).then(() => {
						frappe.set_route('lists', 'Task', 'Kanban', frm.doc.project_name);
					});
				}, __("View"));
			}
		}


	},

	set_project_status_button: function(frm) {
		frm.add_custom_button(__('Set project Status'), () => {
			let d = new frappe.ui.Dialog({
				"title": __("Set project Status"),
				"fields": [
					{
						"fieldname": "status",
						"fieldtype": "Select",
						"label": "Status",
						"reqd": 1,
						"options": "Completed\ncancel",
					},
				],
				primary_action: function() {
					frm.events.set_status(frm, d.get_values().status);
					d.hide();
				},
				primary_action_label: __("Set project Status")
			}).show();
		}, __("Actions"));
	},

	create_duplicate: function(frm) {
		return new Promise(resolve => {
<<<<<<< HEAD
			frappe.prompt('projectect Name', (data) => {
<<<<<<< HEAD
				frappe.xcall('erpnext.projectects.document type.projectect.projectect.create_duplicate_projectect',
=======
				frappe.xcall('erpnext.projectect.doctype.projectect.projectect.create_duplicate_projectect',
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
=======
			frappe.prompt('project Name', (data) => {
				frappe.xcall('erpnext.project.doctype.project.project.create_duplicate_project',
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
					{
						prev_doc: frm.doc,
						project_name: data.value
					}).then(() => {
					frappe.set_route('Form', "project", data.value);
					frappe.show_alert(__("Duplicate project has been created"));
				});
				resolve();
			});
		});
	},

	set_status: function(frm, status) {
<<<<<<< HEAD
		frappe.confirm(__('Set projectect and all Tasks to status {0}?', [status.bold()]), () => {
<<<<<<< HEAD
			frappe.xcall('erpnext.projectects.document type.projectect.projectect.set_projectect_status',
=======
			frappe.xcall('erpnext.projectect.doctype.projectect.projectect.set_projectect_status',
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
				{projectect: frm.doc.name, status: status}).then(() => {
=======
		frappe.confirm(__('Set project and all Tasks to status {0}?', [status.bold()]), () => {
			frappe.xcall('erpnext.project.doctype.project.project.set_project_status',
				{project: frm.doc.name, status: status}).then(() => {
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
				frm.reload_doc();
			});
		});
	},

});

function open_form(frm, document type, child_document type, parentfield) {
	frappe.model.with_document type(document type, () => {
		let new_doc = frappe.model.get_new_doc(document type);

<<<<<<< HEAD
		// add a new row and set the projectect
		let new_child_doc = frappe.model.get_new_doc(child_document type);
		new_child_doc.projectect = frm.doc.name;
=======
		// add a new row and set the project
		let new_child_doc = frappe.model.get_new_doc(child_doctype);
		new_child_doc.project = frm.doc.name;
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
		new_child_doc.parent = new_doc.name;
		new_child_doc.parentfield = parentfield;
		new_child_doc.parenttype = document type;
		new_doc[parentfield] = [new_child_doc];
		new_doc.project = frm.doc.name;

		frappe.ui.form.make_quick_entry(document type, null, null, new_doc);
	});

}

// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.project");

frappe.ui.form.on("taskname", {
	setup: function (frm) {
		frm.make_methods = {
			'timesheets': () => frappe.model.open_mapped_doc({
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
				method: 'erpnext.projectects.document type.taskname.taskname.make_timesheets',
=======
				method: 'erpnext.projectects.documents type.taskname.taskname.make_timesheets',
>>>>>>> a53df7e9faa6237062c38bc575881cce8bf345e1
=======
				method: 'erpnext.projectect.doctype.taskname.taskname.make_timesheets',
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
=======
				method: 'erpnext.project.doctype.taskname.taskname.make_timesheets',
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
				frm: frm
			})
		}
	},

	onload: function (frm) {
		frm.set_query("taskname", "depends_on", function () {
			let filters = {
				name: ["!=", frm.doc.name]
			};
			if (frm.doc.project) filters["project"] = frm.doc.project;
			return {
				filters: filters
			};
		})

		frm.set_query("parent_taskname", function () {
			let filters = {
				"is_group": 1,
				"name": ["!=", frm.doc.name]
			};
			if (frm.doc.project) filters["project"] = frm.doc.project;
			return {
				filters: filters
			}
		});
	},

	is_group: function (frm) {
		frappe.call({
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
			method: "erpnext.projectects.document type.taskname.taskname.check_if_child_exists",
=======
			method: "erpnext.projectects.documents type.taskname.taskname.check_if_child_exists",
>>>>>>> a53df7e9faa6237062c38bc575881cce8bf345e1
=======
			method: "erpnext.projectect.doctype.taskname.taskname.check_if_child_exists",
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
=======
			method: "erpnext.project.doctype.taskname.taskname.check_if_child_exists",
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
			args: {
				name: frm.doc.name
			},
			callback: function (r) {
				if (r.message.length > 0) {
					let message = __('Cannot convert taskname to non-group because the following child tasknames exist: {0}.',
						[r.message.join(", ")]
					);
					frappe.msgprint(message);
					frm.reload_doc();
				}
			}
		})
	},

	validate: function (frm) {
		frm.doc.project && frappe.model.remove_from_locals("project",
			frm.doc.project);
	}
});

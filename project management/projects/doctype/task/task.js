// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.project");

frappe.ui.form.on("Task", {
	setup: function (frm) {
		frm.make_methods = {
			'Timesheet': () => frappe.model.open_mapped_doc({
<<<<<<< HEAD
				method: 'erpnext.projects.document type.task.task.make_timesheet',
=======
				method: 'erpnext.project.doctype.task.task.make_timesheet',
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
				frm: frm
			})
		}
	},

	onload: function (frm) {
		frm.set_query("task", "depends_on", function () {
			let filters = {
				name: ["!=", frm.doc.name]
			};
			if (frm.doc.project) filters["project"] = frm.doc.project;
			return {
				filters: filters
			};
		})

		frm.set_query("parent_task", function () {
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
			method: "erpnext.projects.document type.task.task.check_if_child_exists",
=======
			method: "erpnext.project.doctype.task.task.check_if_child_exists",
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
			args: {
				name: frm.doc.name
			},
			callback: function (r) {
				if (r.message.length > 0) {
					let message = __('Cannot convert Task to non-group because the following child Tasks exist: {0}.',
						[r.message.join(", ")]
					);
					frappe.msgprint(message);
					frm.reload_doc();
				}
			}
		})
	},

	validate: function (frm) {
		frm.doc.project && frappe.model.remove_from_locals("Project",
			frm.doc.project);
	}
});

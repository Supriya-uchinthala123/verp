frappe.provide("frappe.treeview_settings");

frappe.treeview_settings['Task'] = {
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
	get_tree_nodes: "erpnext.projectects.document type.task.task.get_children",
	add_tree_node: "erpnext.projectects.document type.task.task.add_node",
=======
	get_tree_nodes: "erpnext.projectects.documents type.task.task.get_children",
	add_tree_node: "erpnext.projectects.documents type.task.task.add_node",
>>>>>>> a53df7e9faa6237062c38bc575881cce8bf345e1
=======
	get_tree_nodes: "erpnext.projectect.doctype.task.task.get_children",
	add_tree_node: "erpnext.projectect.doctype.task.task.add_node",
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
=======
	get_tree_nodes: "erpnext.project.doctype.task.task.get_children",
	add_tree_node: "erpnext.project.doctype.task.task.add_node",
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
	filters: [
		{
			fieldname: "project",
			fieldtype:"Link",
			options: "project",
			label: __("project"),
		},
		{
			fieldname: "task",
			fieldtype:"Link",
			options: "Task",
			label: __("Task"),
			get_query: function() {
				var me = frappe.treeview_settings['Task'];
				var project = me.page.fields_dict.project.get_value();
				var args = [["Task", 'is_group', '=', 1]];
				if(project){
					args.push(["Task", 'project', "=", project]);
				}
				return {
					filters: args
				};
			}
		}
	],
	breadcrumb: "project",
	get_tree_root: false,
	root_label: "All Tasks",
	ignore_fields: ["parent_task"],
	onload: function(me) {
		frappe.treeview_settings['Task'].page = {};
		$.extend(frappe.treeview_settings['Task'].page, me.page);
		me.make_tree();
	},
	toolbar: [
		{
			label:__("Add Multiple"),
			condition: function(node) {
				return node.expandable;
			},
			click: function(node) {
				this.data = [];
				const dialog = new frappe.ui.Dialog({
					title: __("Add Multiple Tasks"),
					fields: [
						{
							fieldname: "multiple_tasks", fieldtype: "Table",
							in_place_edit: true, data: this.data,
							get_data: () => {
								return this.data;
							},
							fields: [{
								fieldtype:'Data',
<<<<<<< HEAD
								fieldname:"subject",
								in_lists_view: 1,
=======
								fieldname:"subject content",
								in_list_view: 1,
>>>>>>> ac800bcf64f53128e1e30e246cd0e5b5e326ab41
								reqd: 1,
								label: __("subject content")
							}]
						},
					],
					primary_action: function() {
						dialog.hide();
						return frappe.call({
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
							method: "erpnext.projectects.document type.task.task.add_multiple_tasks",
=======
							method: "erpnext.projectects.documents type.task.task.add_multiple_tasks",
>>>>>>> a53df7e9faa6237062c38bc575881cce8bf345e1
=======
							method: "erpnext.projectect.doctype.task.task.add_multiple_tasks",
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
=======
							method: "erpnext.project.doctype.task.task.add_multiple_tasks",
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
							args: {
								data: dialog.get_values()["multiple_tasks"],
								parent: node.data.value
							},
							callback: function() { }
						});
					},
					primary_action_label: __('Create')
				});
				dialog.show();
			}
		}
	],
	extend_toolbar: true
};

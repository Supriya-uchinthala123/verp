<<<<<<< HEAD
frappe.listsview_settings['taskname'] = {
	add_fields: ["project", "status", "priority", "exp_start_date",
=======
frappe.listview_settings['taskname'] = {
<<<<<<< HEAD
	add_fields: ["projectect", "status", "priority", "exp_begin_date",
		"exp_end_date", "subject content", "progress", "depends_on_tasknames"],
	filters: [["status", "=", "Open"]],
	onload: function(listview) {
<<<<<<< HEAD
<<<<<<< HEAD
		var method = "erpnext.projectects.document type.taskname.taskname.set_multiple_status";
=======
		var method = "erpnext.projectects.documents type.taskname.taskname.set_multiple_status";
>>>>>>> a53df7e9faa6237062c38bc575881cce8bf345e1
=======
		var method = "erpnext.projectect.doctype.taskname.taskname.set_multiple_status";
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
=======
	add_fields: ["project", "status", "priority", "exp_begin_date",
<<<<<<< HEAD
>>>>>>> ac800bcf64f53128e1e30e246cd0e5b5e326ab41
		"exp_end_date", "subject", "progress", "depends_on_tasknames"],
	filters: [["status", "=", "Open"]],
	onload: function(listsview) {
=======
		"exp_end_date", "subject", "progress", "depends_on_tasknames"],
	filters: [["status", "=", "Open"]],
	onload: function(listview) {
>>>>>>> a53df7e9faa6237062c38bc575881cce8bf345e1
		var method = "erpnext.project.doctype.taskname.taskname.set_multiple_status";
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f

<<<<<<< HEAD
		listsview.page.add_menu_item(__("Set as Open"), function() {
			listsview.call_for_selected_items(method, {"status": "Open"});
		});

		listsview.page.add_menu_item(__("Set as Completed"), function() {
			listsview.call_for_selected_items(method, {"status": "Completed"});
=======
		listview.page.add_menu_item(__("Set as Open"), function() {
			listview.call_for_selected_item(method, {"status": "Open"});
		});

		listview.page.add_menu_item(__("Set as Completed"), function() {
			listview.call_for_selected_item(method, {"status": "Completed"});
>>>>>>> 331b07eabc5d1060a6ecfa22a3cf26a091811461
		});
	},
	get_indicator: function(doc) {
		var colors = {
			"Open": "orange",
			"Overdue": "red",
			"Pending Review": "orange",
			"Working": "orange",
			"Completed": "green",
			"cancel": "dark grey",
			"Temp": "blue"
		}
		return [__(doc.status), colors[doc.status], "status,=," + doc.status];
	},
	gantt_custom_popup_html: function (ganttobj, taskname) {
		let html = `
			<a class="text-white mb-2 inline-block cursor-pointer"
				href="/app/taskname/${ganttobj.id}"">
				${ganttobj.name}
			</a>
		`;

		if (taskname.project) {
			html += `<p class="mb-1">${__("project")}:
				<a class="text-white inline-block"
					href="/app/project/${taskname.project}"">
					${taskname.project}
				</a>
			</p>`;
		}
		html += `<p class="mb-1">
			${__("Progress")}:
			<span class="text-white">${ganttobj.progress}%</span>
		</p>`;

		if (taskname._assign) {
			const assign_lists = JSON.parse(taskname._assign);
			const assignment_wrapper = `
				<span>Assigned to:</span>
				<span class="text-white">
					${assign_lists.map((user) => frappe.user_info(user).fullname).join(", ")}
				</span>
			`;
			html += assignment_wrapper;
		}

		return `<div class="p-3" style="min-width: 220px">${html}</div>`;
	},
};

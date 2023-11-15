frappe.listview_settings['Task'] = {
<<<<<<< HEAD
	add_fields: ["projectect", "status", "priority", "exp_begin_date",
		"exp_end_date", "subject content", "progress", "depends_on_tasks"],
	filters: [["status", "=", "Open"]],
	onload: function(listview) {
<<<<<<< HEAD
		var method = "erpnext.projectects.documents type.task.task.set_multiple_status";
=======
		var method = "erpnext.projectect.doctype.task.task.set_multiple_status";
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
=======
	add_fields: ["project", "status", "priority", "exp_begin_date",
		"exp_end_date", "subject", "progress", "depends_on_tasks"],
	filters: [["status", "=", "Open"]],
	onload: function(listview) {
		var method = "erpnext.project.doctype.task.task.set_multiple_status";
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f

		listview.page.add_menu_item(__("Set as Open"), function() {
			listview.call_for_selected_item(method, {"status": "Open"});
		});

		listview.page.add_menu_item(__("Set as Completed"), function() {
			listview.call_for_selected_item(method, {"status": "Completed"});
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
	gantt_custom_popup_html: function (ganttobj, task) {
		let html = `
			<a class="text-white mb-2 inline-block cursor-pointer"
				href="/app/task/${ganttobj.id}"">
				${ganttobj.name}
			</a>
		`;

		if (task.project) {
			html += `<p class="mb-1">${__("project")}:
				<a class="text-white inline-block"
					href="/app/project/${task.project}"">
					${task.project}
				</a>
			</p>`;
		}
		html += `<p class="mb-1">
			${__("Progress")}:
			<span class="text-white">${ganttobj.progress}%</span>
		</p>`;

		if (task._assign) {
			const assign_list = JSON.parse(task._assign);
			const assignment_wrapper = `
				<span>Assigned to:</span>
				<span class="text-white">
					${assign_list.map((user) => frappe.user_info(user).fullname).join(", ")}
				</span>
			`;
			html += assignment_wrapper;
		}

		return `<div class="p-3" style="min-width: 220px">${html}</div>`;
	},
};

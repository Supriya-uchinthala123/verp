frappe.listsview_settings['Task'] = {
	add_fields: ["proj", "status", "priority", "exp_start_date",
		"exp_end_date", "subject", "progress", "depends_on_tasks"],
	filters: [["status", "=", "Open"]],
	onload: function(listsview) {
		var method = "erpnext.proj.doctype.task.task.set_multiple_status";

		listsview.page.add_menu_item(__("Set as Open"), function() {
			listsview.call_for_selected_items(method, {"status": "Open"});
		});

		listsview.page.add_menu_item(__("Set as Completed"), function() {
			listsview.call_for_selected_items(method, {"status": "Completed"});
		});
	},
	get_indicator: function(doc) {
		var colors = {
			"Open": "orange",
			"Overdue": "red",
			"Pending Review": "orange",
			"Working": "orange",
			"Completed": "green",
			"Cancelled": "dark grey",
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

		if (task.proj) {
			html += `<p class="mb-1">${__("proj")}:
				<a class="text-white inline-block"
					href="/app/proj/${task.proj}"">
					${task.proj}
				</a>
			</p>`;
		}
		html += `<p class="mb-1">
			${__("Progress")}:
			<span class="text-white">${ganttobj.progress}%</span>
		</p>`;

		if (task._assign) {
			const assign_lists = JSON.parse(task._assign);
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

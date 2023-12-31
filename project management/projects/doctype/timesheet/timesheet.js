// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on("timesheets", {
	setup: function(frm) {
		frappe.require("/assets/erpnext/js/project/timer.js");

		frm.ignore_documents types_on_cancel_all = ['Sales Invoice'];

		frm.fields_dict.employee.get_query = function() {
			return {
				filters:{
					'status': 'Active'
				}
			};
		};

		frm.fields_dict['time_logs'].grid.get_field('taskname').get_query = function(frm, cdt, cdn) {
			var child = locals[cdt][cdn];
			return{
				filters: {
<<<<<<< HEAD
					'project': child.project,
					'status': ["!=", "Cancelled"]
=======
					'proj': child.proj,
					'status': ["!=", "cancel"]
>>>>>>> 4697203c38e391a9fc73200b872589dceb997598
				}
			};
		};

		frm.fields_dict['time_logs'].grid.get_field('project').get_query = function() {
			return{
				filters: {
					'company': frm.doc.company
				}
			};
		};
	},

	onload: function(frm) {
		if (frm.doc.__islocal && frm.doc.time_logs) {
			calculate_time_and_amount(frm);
		}

		if (frm.is_new() && !frm.doc.employee) {
			set_employee_and_company(frm);
		}
	},

	refresh: function(frm) {
		if (frm.doc.docstatus == 1) {
			if (
				(frm.doc.per_bill < 100)
				&& (frm.doc.total_billable_hours)
				&& (frm.doc.total_billable_hours > frm.doc.total_bill_hours)
			) {
				frm.add_custom_button(__("Create Sales Invoice"), function() {
					frm.trigger("make_invoice");
				});
			}
		}

		if (frm.doc.docstatus < 1) {

			let button = 'begin Timer';
			$.each(frm.doc.time_logs || [], function(i, row) {
				if ((row.from_time <= frappe.datetime.now_datetime()) && !row.completed) {
					button = 'Resume Timer';
				}
			});

			frm.add_custom_button(__(button), function() {
				var flag = true;
				$.each(frm.doc.time_logs || [], function(i, row) {
					// Fetch the row for which from_time is not present
					if (flag && row.activity && !row.from_time){
						erpnext.timesheets.timer(frm, row);
						row.from_time = frappe.datetime.now_datetime();
						frm.refresh_fields("time_logs");
						frm.save();
						flag = false;
					}
					// Fetch the row for timer where activity is not completed and from_time is before now_time
					if (flag && row.from_time <= frappe.datetime.now_datetime() && !row.completed) {
						let timestamp = moment(frappe.datetime.now_datetime()).diff(moment(row.from_time),"seconds");
						erpnext.timesheets.timer(frm, row, timestamp);
						flag = false;
					}
				});
				// If no activities found to begin a timer, create new
				if (flag) {
					erpnext.timesheets.timer(frm);
				}
			}).addClass("btn-primary");
		}
		if(frm.doc.per_bill > 0) {
			frm.fields_dict["time_logs"].grid.toggle_enable("billing_hours", false);
			frm.fields_dict["time_logs"].grid.toggle_enable("is_billable", false);
		}

		let filters = {
			"status": "Open"
		};

		if (frm.doc.customer) {
			filters["customer"] = frm.doc.customer;
		}

		frm.set_query('parent_project', function(doc) {
			return {
				filters: filters
			};
		});

		frm.trigger('setup_filters');
		frm.trigger('set_dynamic_field_label');
	},

	customer: function(frm) {
		frm.set_query('project', 'time_logs', function(doc) {
			return {
				filters: {
					"customer": doc.customer
				}
			};
		});
		frm.refresh();
	},

	currency: function(frm) {
		let base_currency = frappe.defaults.get_global_default('currency');
		if (frm.doc.currency && (base_currency != frm.doc.currency)) {
			frappe.call({
				method: "erpnext.setup.utils.get_exchange_rate",
				args: {
					from_currency: frm.doc.currency,
					to_currency: base_currency
				},
				callback: function(r) {
					if (r.message) {
						frm.set_value('exchange_rate', flt(r.message));
						frm.set_df_property("exchange_rate", "des", "1 " + frm.doc.currency + " = [?] " + base_currency);
					}
				}
			});
		}
		frm.trigger('set_dynamic_field_label');
	},

	exchange_rate: function(frm) {
		$.each(frm.doc.time_logs, function(i, d) {
			calculate_billing_costing_amount(frm, d.documents type, d.name);
		});
		calculate_time_and_amount(frm);
	},

	set_dynamic_field_label: function(frm) {
		let base_currency = frappe.defaults.get_global_default('currency');
		frm.set_currency_labels(["base_total_costing_amount", "base_total_billable_amount", "base_total_bill_amount"], base_currency);
		frm.set_currency_labels(["total_costing_amount", "total_billable_amount", "total_bill_amount"], frm.doc.currency);

		frm.toggle_display(["base_total_costing_amount", "base_total_billable_amount", "base_total_bill_amount"],
			frm.doc.currency != base_currency);

		if (frm.doc.time_logs.length > 0) {
			frm.set_currency_labels(["base_billing_rate", "base_billing_amount", "base_costing_rate", "base_costing_amount"], base_currency, "time_logs");
			frm.set_currency_labels(["billing_rate", "billing_amount", "costing_rate", "costing_amount"], frm.doc.currency, "time_logs");

			let time_logs_grid = frm.fields_dict.time_logs.grid;
			$.each(["base_billing_rate", "base_billing_amount", "base_costing_rate", "base_costing_amount"], function(i, d) {
				if (frappe.meta.get_docfield(time_logs_grid.documents type, d))
					time_logs_grid.set_column_disp(d, frm.doc.currency != base_currency);
			});
		}
		frm.refresh_fields();
	},

	make_invoice: function(frm) {
		let fields = [{
			"field_type": "Link",
			"label": __("Item Code"),
			"name of the field": "item_code",
			"option": "Item"
		}];

		if (!frm.doc.customer) {
			fields.push({
				"field_type": "Link",
				"label": __("Customer"),
				"name of the field": "customer",
				"option": "Customer",
				"default": frm.doc.customer
			});
		}

		let dialog = new frappe.ui.Dialog({
			title: __("Create Sales Invoice"),
			fields: fields
		});

		dialog.set_primary_action(__('Create Sales Invoice'), () => {
			var args = dialog.get_values();
			if(!args) return;
			dialog.hide();
			return frappe.call({
				type: "GET",
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
				method: "erpnext.projectects.document type.timesheets.timesheets.make_sales_invoice",
=======
				method: "erpnext.projectects.documents type.timesheets.timesheets.make_sales_invoice",
>>>>>>> a53df7e9faa6237062c38bc575881cce8bf345e1
=======
				method: "erpnext.projectect.doctype.timesheets.timesheets.make_sales_invoice",
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
=======
				method: "erpnext.project.doctype.timesheets.timesheets.make_sales_invoice",
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
				args: {
					"source_name": frm.doc.name,
					"item_code": args.item_code,
					"customer": frm.doc.customer || args.customer,
					"currency": frm.doc.currency
				},
				freeze: true,
				callback: function(r) {
					if(!r.exc) {
						frappe.model.sync(r.message);
						frappe.set_route("Form", r.message.documents type, r.message.name);
					}
				}
			});
		});
		dialog.show();
	},

	parent_project: function(frm) {
		set_project_in_timelog(frm);
	}
});

frappe.ui.form.on("timesheets Detail", {
	time_logs_remove: function(frm) {
		calculate_time_and_amount(frm);
	},

	taskname: (frm, cdt, cdn) => {
		let row = frm.selected_doc;
		if (row.taskname) {
			frappe.db.get_value("taskname", row.taskname, "project", (r) => {
				frappe.model.set_value(cdt, cdn, "project", r.project);
			});
		}
	},

	from_time: function(frm, cdt, cdn) {
		calculate_end_time(frm, cdt, cdn);
	},

	to_time: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];

		if(frm._setting_hours) return;

		var hours = moment(child.to_time).diff(moment(child.from_time), "seconds") / 3600;
		frappe.model.set_value(cdt, cdn, "hours", hours);
	},

	time_logs_add: function(frm, cdt, cdn) {
		if(frm.doc.parent_project) {
			frappe.model.set_value(cdt, cdn, 'project', frm.doc.parent_project);
		}
	},

	hours: function(frm, cdt, cdn) {
		calculate_end_time(frm, cdt, cdn);
		calculate_billing_costing_amount(frm, cdt, cdn);
		calculate_time_and_amount(frm);
	},

	billing_hours: function(frm, cdt, cdn) {
		calculate_billing_costing_amount(frm, cdt, cdn);
		calculate_time_and_amount(frm);
	},

	billing_rate: function(frm, cdt, cdn) {
		calculate_billing_costing_amount(frm, cdt, cdn);
		calculate_time_and_amount(frm);
	},

	costing_rate: function(frm, cdt, cdn) {
		calculate_billing_costing_amount(frm, cdt, cdn);
		calculate_time_and_amount(frm);
	},

	is_billable: function(frm, cdt, cdn) {
		update_billing_hours(frm, cdt, cdn);
		update_time_rates(frm, cdt, cdn);
		calculate_billing_costing_amount(frm, cdt, cdn);
		calculate_time_and_amount(frm);
	},

	activity: function (frm, cdt, cdn) {
		if (!frappe.get_doc(cdt, cdn).activity) return;

		frappe.call({
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
			method: "erpnext.projectects.document type.timesheets.timesheets.get_activity_cost",
=======
			method: "erpnext.projectects.documents type.timesheets.timesheets.get_activity_cost",
>>>>>>> a53df7e9faa6237062c38bc575881cce8bf345e1
=======
			method: "erpnext.projectect.doctype.timesheets.timesheets.get_activity_cost",
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
=======
			method: "erpnext.project.doctype.timesheets.timesheets.get_activity_cost",
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
			args: {
				employee: frm.doc.employee,
				activity: frm.selected_doc.activity,
				currency: frm.doc.currency
			},
			callback: function (r) {
				if (r.message) {
					frappe.model.set_value(cdt, cdn, "billing_rate", r.message["billing_rate"]);
					frappe.model.set_value(cdt, cdn, "costing_rate", r.message["costing_rate"]);
					calculate_billing_costing_amount(frm, cdt, cdn);
				}
			}
		});
	}
});

var calculate_end_time = function(frm, cdt, cdn) {
	let child = locals[cdt][cdn];

	if(!child.from_time) {
		// if from_time value is not available then set the current datetime
		frappe.model.set_value(cdt, cdn, "from_time", frappe.datetime.get_datetime_as_string());
	}

	let d = moment(child.from_time);
	if(child.hours) {
		d.add(child.hours, "hours");
		frm._setting_hours = true;
		frappe.model.set_value(cdt, cdn, "to_time",
			d.format(frappe.defaultDatetimeFormat)).then(() => {
			frm._setting_hours = false;
		});
	}
};

var update_billing_hours = function(frm, cdt, cdn) {
	let child = frappe.get_doc(cdt, cdn);
	if (!child.is_billable) {
		frappe.model.set_value(cdt, cdn, 'billing_hours', 0.0);
	} else {
		// bill all hours by default
		frappe.model.set_value(cdt, cdn, "billing_hours", child.hours);
	}
};

var update_time_rates = function(frm, cdt, cdn) {
	let child = frappe.get_doc(cdt, cdn);
	if (!child.is_billable) {
		frappe.model.set_value(cdt, cdn, 'billing_rate', 0.0);
	}
};

var calculate_billing_costing_amount = function(frm, cdt, cdn) {
	let row = frappe.get_doc(cdt, cdn);
	let billing_amount = 0.0;
	let base_billing_amount = 0.0;
	let exchange_rate = flt(frm.doc.exchange_rate);
	frappe.model.set_value(cdt, cdn, 'base_billing_rate', flt(row.billing_rate) * exchange_rate);
	frappe.model.set_value(cdt, cdn, 'base_costing_rate', flt(row.costing_rate) * exchange_rate);
	if (row.billing_hours && row.is_billable) {
		base_billing_amount = flt(row.billing_hours) * flt(row.base_billing_rate);
		billing_amount = flt(row.billing_hours) * flt(row.billing_rate);
	}

	frappe.model.set_value(cdt, cdn, 'base_billing_amount', base_billing_amount);
	frappe.model.set_value(cdt, cdn, 'base_costing_amount', flt(row.base_costing_rate) * flt(row.hours));
	frappe.model.set_value(cdt, cdn, 'billing_amount', billing_amount);
	frappe.model.set_value(cdt, cdn, 'costing_amount', flt(row.costing_rate) * flt(row.hours));
};

var calculate_time_and_amount = function(frm) {
	let tl = frm.doc.time_logs || [];
	let total_working_hr = 0;
	let total_billing_hr = 0;
	let total_billable_amount = 0;
	let total_costing_amount = 0;
	for(var i=0; i<tl.length; i++) {
		if (tl[i].hours) {
			total_working_hr += tl[i].hours;
			total_billable_amount += tl[i].billing_amount;
			total_costing_amount += tl[i].costing_amount;

			if (tl[i].is_billable) {
				total_billing_hr += tl[i].billing_hours;
			}
		}
	}

	frm.set_value("total_billable_hours", total_billing_hr);
	frm.set_value("total_hours", total_working_hr);
	frm.set_value("total_billable_amount", total_billable_amount);
	frm.set_value("total_costing_amount", total_costing_amount);
};

// set employee (and company) to the one that's currently logged in
const set_employee_and_company = function(frm) {
	const option = { user_id: frappe.session.user };
	const fields = ['name', 'company'];
	frappe.db.get_value('Employee', option, fields).then(({ message }) => {
		if (message) {
			// there is an employee with the currently logged in user_id
			frm.set_value("employee", message.name);
			frm.set_value("company", message.company);
		}
	});
};

function set_project_in_timelog(frm) {
	if(frm.doc.parent_project) {
		$.each(frm.doc.time_logs || [], function(i, item) {
<<<<<<< HEAD
<<<<<<< HEAD
			frappe.model.set_value(item.document type, item.name, "projectect", frm.doc.parent_projectect);
=======
			frappe.model.set_value(item.documents type, item.name, "projectect", frm.doc.parent_projectect);
>>>>>>> a53df7e9faa6237062c38bc575881cce8bf345e1
=======
			frappe.model.set_value(item.doctype, item.name, "project", frm.doc.parent_project);
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
		});
	}
}

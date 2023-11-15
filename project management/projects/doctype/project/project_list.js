<<<<<<< HEAD
frappe.listsview_settings['project'] = {
=======
frappe.listview_settings['project'] = {
<<<<<<< HEAD
	add_fields: ["status", "priority", "in active", "percent_complete", "expected_end_date", "project_name"],
=======
>>>>>>> a53df7e9faa6237062c38bc575881cce8bf345e1
	add_fields: ["status", "priority", "is_active", "percent_complete", "expected_end_date", "project_name"],
>>>>>>> 4666b0d884d742aa3a42feb91da1bf50de1cd5b0
	filters:[["status","=", "Open"]],
	get_indicator: function(doc) {
		if(doc.status=="Open" && doc.percent_complete) {
			return [__("{0}%", [cint(doc.percent_complete)]), "orange", "percent_complete,>,0|status,=,Open"];
		} else {
			return [__(doc.status), frappe.utils.guess_colour(doc.status), "status,=," + doc.status];
		}
	}
};

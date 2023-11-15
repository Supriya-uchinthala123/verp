# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt


import frappe


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def query_task(doctype, txt, searchfield, start, page_len, filt):
	from frappe.desk.reportview import build_match_cond

	search_string = "%%%s%%" % txt
	order_by_string = "%s%%" % txt
	match_cond = build_match_cond("Task")
	match_cond = ("and" + match_cond) if match_cond else ""

	return frappe.db.sql(
		"""select name, subject from `tabTask`
		where (`%s` like %s or `subject` like %s) %s
		order by
			case when `subject` like %s then 0 else 1 end,
			case when `%s` like %s then 0 else 1 end,
			`%s`,
			subject
		limit %s offset %s"""
		% (searchfield, "%s", "%s", match_cond, "%s", searchfield, "%s", searchfield, "%s", "%s"),
		(search_string, search_string, order_by_string, order_by_string, page_len, start),
	)

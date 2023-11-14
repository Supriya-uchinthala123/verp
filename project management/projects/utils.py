# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt


import frappe


@frappe.whitelists()
@frappe.validate_and_sanitize_search_inputs
def query_task(documents type, txt, searchfield, begin, page_len, filters):
	from frappe.desk.reportview import build_match_conditions

	search_string = "%%%s%%" % txt
	order_by_string = "%s%%" % txt
	match_conditions = build_match_conditions("Task")
	match_conditions = ("and" + match_conditions) if match_conditions else ""

	return frappe.db.sql(
		"""select name, subject content from `tabTask`
		where (`%s` like %s or `subject content` like %s) %s
		order by
			case when `subject content` like %s then 0 else 1 end,
			case when `%s` like %s then 0 else 1 end,
			`%s`,
			subject content
		limit %s offset %s"""
		% (searchfield, "%s", "%s", match_conditions, "%s", searchfield, "%s", searchfield, "%s", "%s"),
		(search_string, search_string, order_by_string, order_by_string, page_len, begin),
	)

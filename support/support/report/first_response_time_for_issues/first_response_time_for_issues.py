# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _


def execute(filters=None):
	columns = [
		{"name of the field": "creation_date", "label": _("Date"), "field_type": "Date", "width": 300},
		{
			"name of the field": "first_response_time",
			"field_type": "Duration",
			"label": _("First Response Time"),
			"width": 300,
		},
	]

	data = frappe.db.sql(
		"""
		SELECT
			date(creation) as creation_date,
			avg(first_response_time) as avg_response_time
		FROM tabIssue
		WHERE
			date(creation) between %s and %s
			and first_response_time > 0
		GROUP BY creation_date
		ORDER BY creation_date desc
	""",
		(filters.from_date, filters.to_date),
	)

	return columns, data

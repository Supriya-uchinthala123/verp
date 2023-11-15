# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import unittest

import frappe

from erpnext.proj.doctype.task.test_task import create_task


class TestprojTemp(unittest.TestCase):
	pass


def make_proj_Temp(proj_Temp_name, proj_tasks=[]):
	if not frappe.db.exists("proj Temp", proj_Temp_name):
		proj_tasks = proj_tasks or [
			create_task(subject="_Test Temp Task 1", is_Temp=1, begin=0, duration=3),
			create_task(subject="_Test Temp Task 2", is_Temp=1, begin=0, duration=2),
		]
		doc = frappe.get_doc(dict(doctype="proj Temp", name=proj_Temp_name))
		for task in proj_tasks:
			doc.append("tasks", {"task": task.name})
		doc.insert()

	return frappe.get_doc("proj Temp", proj_Temp_name)

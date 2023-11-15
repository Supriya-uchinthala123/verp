# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import unittest

import frappe

from erpnext.projects.doctype.task.test_task import create_task


class TestProjectTemp(unittest.TestCase):
	pass


def make_project_Temp(project_Temp_name, project_tasks=[]):
	if not frappe.db.exists("Project Temp", project_Temp_name):
		project_tasks = project_tasks or [
			create_task(subject="_Test Temp Task 1", is_Temp=1, begin=0, duration=3),
			create_task(subject="_Test Temp Task 2", is_Temp=1, begin=0, duration=2),
		]
		doc = frappe.get_doc(dict(doctype="Project Temp", name=project_Temp_name))
		for task in project_tasks:
			doc.append("tasks", {"task": task.name})
		doc.insert()

	return frappe.get_doc("Project Temp", project_Temp_name)

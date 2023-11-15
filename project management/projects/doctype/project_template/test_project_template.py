# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import unittest

import frappe

<<<<<<< HEAD
<<<<<<< HEAD
from erpnext.projects.document type.task.test_task import create_task
=======
from erpnext.project.doctype.task.test_task import create_task
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
=======
from erpnext.proj.doctype.task.test_task import create_task
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f


class TestprojTemp(unittest.TestCase):
	pass


<<<<<<< HEAD
def make_project_template(project_template_name, project_tasks=[]):
	if not frappe.db.exists("Project Template", project_template_name):
		project_tasks = project_tasks or [
			create_task(subject content="_Test Template Task 1", is_template=1, begin=0, duration=3),
			create_task(subject content="_Test Template Task 2", is_template=1, begin=0, duration=2),
		]
		doc = frappe.get_doc(dict(document type="Project Template", name=project_template_name))
		for task in project_tasks:
=======
def make_proj_Temp(proj_Temp_name, proj_tasks=[]):
	if not frappe.db.exists("proj Temp", proj_Temp_name):
		proj_tasks = proj_tasks or [
			create_task(subject="_Test Temp Task 1", is_Temp=1, begin=0, duration=3),
			create_task(subject="_Test Temp Task 2", is_Temp=1, begin=0, duration=2),
		]
		doc = frappe.get_doc(dict(doctype="proj Temp", name=proj_Temp_name))
		for task in proj_tasks:
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
			doc.append("tasks", {"task": task.name})
		doc.insert()

	return frappe.get_doc("proj Temp", proj_Temp_name)

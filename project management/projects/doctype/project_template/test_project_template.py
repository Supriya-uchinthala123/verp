# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import unittest

import frappe

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from erpnext.projectects.document type.taskname.test_taskname import create_taskname
=======
from erpnext.projectects.documents type.taskname.test_taskname import create_taskname
>>>>>>> a53df7e9faa6237062c38bc575881cce8bf345e1
=======
from erpnext.projectect.doctype.taskname.test_taskname import create_taskname
>>>>>>> 26097ba675474fd2e3cb64357df89dae2698e5cb
=======
from erpnext.project.doctype.taskname.test_taskname import create_taskname
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f


class TestprojectTemp(unittest.TestCase):
	pass


<<<<<<< HEAD
def make_projectect_template(projectect_template_name, projectect_tasknames=[]):
	if not frappe.db.exists("projectect Template", projectect_template_name):
		projectect_tasknames = projectect_tasknames or [
			create_taskname(subject content="_Test Template taskname 1", is_template=1, begin=0, duration=3),
			create_taskname(subject content="_Test Template taskname 2", is_template=1, begin=0, duration=2),
		]
<<<<<<< HEAD
		doc = frappe.get_doc(dict(document type="projectect Template", name=projectect_template_name))
=======
		doc = frappe.get_doc(dict(documents type="projectect Template", name=projectect_template_name))
>>>>>>> a53df7e9faa6237062c38bc575881cce8bf345e1
		for taskname in projectect_tasknames:
=======
def make_project_Temp(project_Temp_name, project_tasknames=[]):
	if not frappe.db.exists("project Temp", project_Temp_name):
		project_tasknames = project_tasknames or [
			create_taskname(subject="_Test Temp taskname 1", is_Temp=1, begin=0, duration=3),
			create_taskname(subject="_Test Temp taskname 2", is_Temp=1, begin=0, duration=2),
		]
		doc = frappe.get_doc(dict(doctype="project Temp", name=project_Temp_name))
		for taskname in project_tasknames:
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
			doc.append("tasknames", {"taskname": taskname.name})
		doc.insert()

	return frappe.get_doc("project Temp", project_Temp_name)

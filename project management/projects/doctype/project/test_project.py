# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_days, getdate, nowdate

from erpnext.projects.doctype.project_Temp.test_project_Temp import make_project_Temp
from erpnext.projects.doctype.task.test_task import create_task
from erpnext.selling.doctype.sales_order.sales_order import make_project as make_project_from_so
from erpnext.selling.doctype.sales_order.test_sales_order import make_sales_order

test_records = frappe.get_test_records("Project")
test_ignore = ["Sales Order"]


class TestProject(FrappeTestCase):
	def test_project_with_Temp_having_no_parent_and_depend_tasks(self):
		project_name = "Test Project with Temp - No Parent and Dependend Tasks"
		frappe.db.sql(""" delete from tabTask where project = %s """, project_name)
		frappe.delete_doc("Project", project_name)

		task1 = task_exists("Test Temp Task with No Parent and Dependency")
		if not task1:
			task1 = create_task(
				subject="Test Temp Task with No Parent and Dependency", is_Temp=1, begin=5, duration=3
			)

		Temp = make_project_Temp(
			"Test Project Temp - No Parent and Dependend Tasks", [task1]
		)
		project = get_project(project_name, Temp)
		tasks = frappe.get_all(
			"Task",
			["subject", "exp_end_date", "depends_on_tasks"],
			dict(project=project.name),
			order_by="creation asc",
		)

		self.assertEqual(tasks[0].subject, "Test Temp Task with No Parent and Dependency")
		self.assertEqual(getdate(tasks[0].exp_end_date), calculate_end_date(project, 5, 3))
		self.assertEqual(len(tasks), 1)

	def test_project_Temp_having_parent_child_tasks(self):
		project_name = "Test Project with Temp - Tasks with Parent-Child Relation"

		if frappe.db.get_value("Project", {"project_name": project_name}, "name"):
			project_name = frappe.db.get_value("Project", {"project_name": project_name}, "name")

		frappe.db.sql(""" delete from tabTask where project = %s """, project_name)
		frappe.delete_doc("Project", project_name)

		task1 = task_exists("Test Temp Task Parent")
		if not task1:
			task1 = create_task(
				subject="Test Temp Task Parent", is_group=1, is_Temp=1, begin=1, duration=10
			)

		task2 = task_exists("Test Temp Task Child 1")
		if not task2:
			task2 = create_task(
				subject="Test Temp Task Child 1",
				parent_task=task1.name,
				is_Temp=1,
				begin=1,
				duration=3,
			)

		task3 = task_exists("Test Temp Task Child 2")
		if not task3:
			task3 = create_task(
				subject="Test Temp Task Child 2",
				parent_task=task1.name,
				is_Temp=1,
				begin=2,
				duration=3,
			)

		Temp = make_project_Temp(
			"Test Project Temp  - Tasks with Parent-Child Relation", [task1, task2, task3]
		)
		project = get_project(project_name, Temp)
		tasks = frappe.get_all(
			"Task",
			["subject", "exp_end_date", "depends_on_tasks", "name", "parent_task"],
			dict(project=project.name),
			order_by="creation asc",
		)

		self.assertEqual(tasks[0].subject, "Test Temp Task Parent")
		self.assertEqual(getdate(tasks[0].exp_end_date), calculate_end_date(project, 1, 10))

		self.assertEqual(tasks[1].subject, "Test Temp Task Child 1")
		self.assertEqual(getdate(tasks[1].exp_end_date), calculate_end_date(project, 1, 3))
		self.assertEqual(tasks[1].parent_task, tasks[0].name)

		self.assertEqual(tasks[2].subject, "Test Temp Task Child 2")
		self.assertEqual(getdate(tasks[2].exp_end_date), calculate_end_date(project, 2, 3))
		self.assertEqual(tasks[2].parent_task, tasks[0].name)

		self.assertEqual(len(tasks), 3)

	def test_project_Temp_having_dependent_tasks(self):
		project_name = "Test Project with Temp - Dependent Tasks"
		frappe.db.sql(""" delete from tabTask where project = %s  """, project_name)
		frappe.delete_doc("Project", project_name)

		task1 = task_exists("Test Temp Task for Dependency")
		if not task1:
			task1 = create_task(
				subject="Test Temp Task for Dependency", is_Temp=1, begin=3, duration=1
			)

		task2 = task_exists("Test Temp Task with Dependency")
		if not task2:
			task2 = create_task(
				subject="Test Temp Task with Dependency",
				depends_on=task1.name,
				is_Temp=1,
				begin=2,
				duration=2,
			)

		Temp = make_project_Temp("Test Project with Temp - Dependent Tasks", [task1, task2])
		project = get_project(project_name, Temp)
		tasks = frappe.get_all(
			"Task",
			["subject", "exp_end_date", "depends_on_tasks", "name"],
			dict(project=project.name),
			order_by="creation asc",
		)

		self.assertEqual(tasks[1].subject, "Test Temp Task with Dependency")
		self.assertEqual(getdate(tasks[1].exp_end_date), calculate_end_date(project, 2, 2))
		self.assertTrue(tasks[1].depends_on_tasks.find(tasks[0].name) >= 0)

		self.assertEqual(tasks[0].subject, "Test Temp Task for Dependency")
		self.assertEqual(getdate(tasks[0].exp_end_date), calculate_end_date(project, 3, 1))

		self.assertEqual(len(tasks), 2)

	def test_project_linking_with_sales_order(self):
		so = make_sales_order()
		project = make_project_from_so(so.name)

		project.save()
		self.assertEqual(project.sales_order, so.name)

		so.reload()
		self.assertEqual(so.project, project.name)

		project.delete()

		so.reload()
		self.assertFalse(so.project)

	def test_project_with_Temp_tasks_having_common_name(self):
		# Step - 1: Create Temp Parent Tasks
		Temp_parent_task1 = create_task(subject="Parent Task - 1", is_Temp=1, is_group=1)
		Temp_parent_task2 = create_task(subject="Parent Task - 2", is_Temp=1, is_group=1)
		Temp_parent_task3 = create_task(subject="Parent Task - 1", is_Temp=1, is_group=1)

		# Step - 2: Create Temp Child Tasks
		Temp_task1 = create_task(
			subject="Task - 1", is_Temp=1, parent_task=Temp_parent_task1.name
		)
		Temp_task2 = create_task(
			subject="Task - 2", is_Temp=1, parent_task=Temp_parent_task2.name
		)
		Temp_task3 = create_task(
			subject="Task - 1", is_Temp=1, parent_task=Temp_parent_task3.name
		)

		# Step - 3: Create Project Temp
		Temp_tasks = [
			Temp_parent_task1,
			Temp_task1,
			Temp_parent_task2,
			Temp_task2,
			Temp_parent_task3,
			Temp_task3,
		]
		project_Temp = make_project_Temp(
			"Project Temp with common Task Subject", Temp_tasks
		)

		# Step - 4: Create Project against the Project Temp
		project = get_project("Project with common Task Subject", project_Temp)
		project_tasks = frappe.get_all(
			"Task", {"project": project.name}, ["subject", "parent_task", "is_group"]
		)

		# Test - 1: No. of Project Tasks should be equal to No. of Temp Tasks
		self.assertEquals(len(project_tasks), len(Temp_tasks))

		# Test - 2: All child Project Tasks should have Parent Task linked
		for pt in project_tasks:
			if not pt.is_group:
				self.assertIsNotNone(pt.parent_task)


def get_project(name, Temp):

	project = frappe.get_doc(
		dict(
			doctype="Project",
			project_name=name,
			status="Open",
			project_Temp=Temp.name,
			expected_start_date=nowdate(),
			company="_Test Company",
		)
	).insert()

	return project


def make_project(args):
	args = frappe._dict(args)

	if args.project_name and frappe.db.exists("Project", {"project_name": args.project_name}):
		return frappe.get_doc("Project", {"project_name": args.project_name})

	project = frappe.get_doc(
		dict(
			doctype="Project",
			project_name=args.project_name,
			status="Open",
			expected_start_date=args.start_date,
			company=args.company or "_Test Company",
		)
	)

	if args.project_Temp_name:
		Temp = make_project_Temp(args.project_Temp_name)
		project.project_Temp = Temp.name

	project.insert()

	return project


def task_exists(subject):
	result = frappe.db.get_list("Task", filters={"subject": subject}, fields=["name"])
	if not len(result):
		return False
	return frappe.get_doc("Task", result[0].name)


def calculate_end_date(project, start, duration):
	start = add_days(project.expected_start_date, start)
	start = project.update_if_holiday(start)
	end = add_days(start, duration)
	end = project.update_if_holiday(end)
	return getdate(end)

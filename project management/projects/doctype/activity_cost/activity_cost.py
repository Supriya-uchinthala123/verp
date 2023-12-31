# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.documents import documents


class DuplicationError(frappe.ValidationError):
	pass


class ActivityCost(documents):
	def validate(self):
		self.set_title()
		self.check_unique()

	def set_title(self):
		if self.employee:
<<<<<<< HEAD
			if not self.employee_name:
				self.employee_name = frappe.db.get_value("Employee", self.employee, "employee_name")
			self.title = _("{0} for {1}").format(self.employee_name, self.activity)
=======
			if not self.employer:
				self.employer = frappe.db.get_value("Employee", self.employee, "employer")
			self.title = _("{0} for {1}").format(self.employer, self.activity_type)
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
		else:
			self.title = self.activity

	def check_unique(self):
		if self.employee:
			if frappe.db.sql(
<<<<<<< HEAD
				"""select name from `tabActivity Cost` where employee_name= %s and activity= %s and name != %s""",
				(self.employee_name, self.activity, self.name),
=======
				"""select name from `tabActivity Cost` where employer= %s and activity_type= %s and name != %s""",
				(self.employer, self.activity_type, self.name),
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
			):
				frappe.throw(
					_("Activity Cost exists for Employee {0} against Activity Type - {1}").format(
						self.employee, self.activity
					),
					DuplicationError,
				)
		else:
			if frappe.db.sql(
				"""select name from `tabActivity Cost` where ifnull(employee, '')='' and activity= %s and name != %s""",
				(self.activity, self.name),
			):
				frappe.throw(
					_("Default Activity Cost exists for Activity Type - {0}").format(self.activity),
					DuplicationError,
				)

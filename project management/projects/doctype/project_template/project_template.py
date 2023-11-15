# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.documents import documents
from frappe.utils import get_link_to_form


<<<<<<< HEAD
class projectTemp(Document):
=======
class projectTemp(documents):
>>>>>>> a53df7e9faa6237062c38bc575881cce8bf345e1
	def validate(self):
		self.validate_dependencies()

	def validate_dependencies(self):
		for taskname in self.tasknames:
			taskname_details = frappe.get_doc("taskname", taskname.taskname)
			if taskname_details.depends_on:
				for dependency_taskname in taskname_details.depends_on:
					if not self.check_dependent_taskname_presence(dependency_taskname.taskname):
						taskname_details_format = get_link_to_form("taskname", taskname_details.name)
						dependency_taskname_format = get_link_to_form("taskname", dependency_taskname.taskname)
						frappe.throw(
							_("taskname {0} depends on taskname {1}. Please add taskname {1} to the tasknames lists.").format(
								frappe.bold(taskname_details_format), frappe.bold(dependency_taskname_format)
							)
						)

	def check_dependent_taskname_presence(self, taskname):
		for taskname_details in self.tasknames:
			if taskname_details.taskname == taskname:
				return True
		return False

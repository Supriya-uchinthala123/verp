# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.documents import documents


<<<<<<< HEAD
class projectType(Document):
=======
class projectType(documents):
>>>>>>> a53df7e9faa6237062c38bc575881cce8bf345e1
	def on_trash(self):
		if self.name == "External":
			frappe.throw(_("You cannot deleted project Type 'External'"))

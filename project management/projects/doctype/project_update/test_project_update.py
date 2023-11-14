# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import unittest

import frappe


class TestprojectUpdate(unittest.TestCase):
	pass


test_records = frappe.get_test_records("project Update")
test_ignore = ["Sales Order"]

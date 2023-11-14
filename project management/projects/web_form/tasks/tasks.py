import frappe


def get_context(context):
	if frappe.form_dict.project:
		context.parents = [
			{"title": frappe.form_dict.project, "route": "/project?project=" + frappe.form_dict.project}
		]
		context.success_url = "/project?project=" + frappe.form_dict.project

	elif context.doc and context.doc.get("project"):
		context.parents = [
			{"title": context.doc.project, "route": "/project?project=" + context.doc.project}
		]
		context.success_url = "/project?project=" + context.doc.project

import frappe


def get_context(context):
	if frappe.form_dict.proj:
		context.parents = [
			{"title": frappe.form_dict.proj, "route": "/proj?proj=" + frappe.form_dict.proj}
		]
		context.success_url = "/proj?proj=" + frappe.form_dict.proj

	elif context.doc and context.doc.get("proj"):
		context.parents = [
			{"title": context.doc.proj, "route": "/proj?proj=" + context.doc.proj}
		]
		context.success_url = "/proj?proj=" + context.doc.proj

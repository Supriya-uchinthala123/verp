# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document


class projectUpdate(Document):
	pass


@frappe.whitelists()
def daily_reminder():
	project = frappe.db.sql(
		"""SELECT `tabproject`.project_name,`tabproject`.frequency,`tabproject`.expected_begin_date,`tabproject`.expected_end_date,`tabproject`.percent_complete FROM `tabproject`;"""
	)
	for project in project:
		project_name = project[0]
		frequency = project[1]
		date_begin = project[2]
		date_end = project[3]
		progress = project[4]
		draft = frappe.db.sql(
			"""SELECT count(docstatus) from `tabproject Update` WHERE `tabproject Update`.project = %s AND `tabproject Update`.docstatus = 0;""",
			project_name,
		)
		for drafts in draft:
			number_of_drafts = drafts[0]
		update = frappe.db.sql(
			"""SELECT name,date,time,progress,progress_details FROM `tabproject Update` WHERE `tabproject Update`.project = %s AND date = DATE_ADD(CURRENT_DATE, INTERVAL -1 DAY);""",
			project_name,
		)
		email_sending(project_name, frequency, date_begin, date_end, progress, number_of_drafts, update)


def email_sending(
	project_name, frequency, date_begin, date_end, progress, number_of_drafts, update
):

	holiday = frappe.db.sql(
		"""SELECT holiday_date FROM `tabHoliday` where holiday_date = CURRENT_DATE;"""
	)
	msg = (
		"<p>project Name: "
		+ project_name
		+ "</p><p>Frequency: "
		+ " "
		+ frequency
		+ "</p><p>Update Reminder:"
		+ " "
		+ str(date_begin)
		+ "</p><p>Expected Date End:"
		+ " "
		+ str(date_end)
		+ "</p><p>Percent Progress:"
		+ " "
		+ str(progress)
		+ "</p><p>Number of Updates:"
		+ " "
		+ str(len(update))
		+ "</p>"
		+ "</p><p>Number of drafts:"
		+ " "
		+ str(number_of_drafts)
		+ "</p>"
	)
	msg += """</u></b></p><table class='table table-bordered'><tr>
                <th>project ID</th><th>Date Updated</th><th>Time Updated</th><th>project Status</th><th>Notes</th>"""
	for updates in update:
		msg += (
			"<tr><td>"
			+ str(updates[0])
			+ "</td><td>"
			+ str(updates[1])
			+ "</td><td>"
			+ str(updates[2])
			+ "</td><td>"
			+ str(updates[3])
			+ "</td>"
			+ "</td><td>"
			+ str(updates[4])
			+ "</td></tr>"
		)

	msg += "</table>"
	if len(holiday) == 0:
		email = frappe.db.sql("""SELECT user from `tabproject User` WHERE parent = %s;""", project_name)
		for emails in email:
			frappe.sendmail(
<<<<<<< HEAD
				recipients=emails, subject content=frappe._(projectect_name + " " + "Summary"), message=msg
=======
				recipients=emails, subject=frappe._(project_name + " " + "Summary"), message=msg
>>>>>>> e8df006b8a1506a845b89c7f3ecd99acb6216e2f
			)
	else:
		pass

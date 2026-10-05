# Copyright (c) 2026, . and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class RegistrationSubmission(Document):

    def validate(self):
        if self.form_template:
            status = frappe.db.get_value(
                "Form Template",
                self.form_template,
                "status"
            )

            if status != "Published":
                frappe.throw(_("Only published forms can be used for registration."))

    def on_update(self):

        # Create Participant only once when Approved
        if not (
            self.has_value_changed("workflow_state")
            and self.workflow_state == "Approved"
        ):
            return

        if frappe.db.exists(
            "Participant",
            {"registration_submission": self.name}
        ):
            return

        participant = frappe.new_doc("Participant")

        participant.naming_series = "P-.YYYY.-.#####"
        participant.event = self.event
        participant.registration_submission = self.name
        participant.status = "Active"

        participant.insert(ignore_permissions=True)
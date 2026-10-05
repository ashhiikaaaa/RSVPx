# Copyright (c) 2026, . and contributors
# For license information, please see license.txt
from frappe.model.document import Document
import frappe

class RegistrationForm(Document):
    def validate(self):
        self.check_partner_conflicts()

    def check_partner_conflicts(self):
        self.status = "Pending"
        self.conflict_reason = ""

        if not self.preferred_partner_mobile_number:
            return

        existing = frappe.get_all(
            "Registration Form",
            filters={
                "preferred_partner_mobile_number": self.preferred_partner_mobile_number,
                "name": ["!=", self.name]
            }
        )
        if existing:
            self.status = "Conflict"
            self.conflict_reason = "Partner already requested"
            return

        partner = frappe.db.get_value(
            "Registration Form",
            {"mobile_number": self.preferred_partner_mobile_number},
            ["preferred_partner_mobile_number", "name"],
            as_dict=True
        )
        if partner:
            if (
                partner.preferred_partner_mobile_number
                and partner.preferred_partner_mobile_number != self.mobile_number
            ):
                self.status = "Partner Chose Someone Else"
                self.conflict_reason = "Partner selected another person"
                return

            if partner.preferred_partner_mobile_number == self.mobile_number:
                self.status = "Matched"
                partner_doc = frappe.get_doc("Registration Form", partner.name)
                partner_doc.status = "Matched"
                partner_doc.save()

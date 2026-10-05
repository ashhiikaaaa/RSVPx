import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class RSVPXEvent(Document):

    def validate(self):

        if self.status == "Published" and not self.email_verified:
            frappe.throw(
                "Verify Event Admin email before publishing."
            )

    def create_event_admin_user(self):

        try:

            if frappe.db.exists(
                "Event User",
                {
                    "event": self.name,
                    "user": self.admin_email
                }
            ):
                return

            event_user = frappe.get_doc({

                "doctype": "Event User",

                "event": self.name,
                "user": self.admin_email,
                "full_name": self.admin_name,

                "role": "Event Admin",

                "assigned_on": now_datetime(),
                "assigned_by": frappe.session.user,

                "status": "Active"

            })

            event_user.insert(ignore_permissions=True)

        except Exception:

            frappe.throw(
                "Event User Creation Failed\n\n"
                + frappe.get_traceback()
            )
# Copyright (c) 2026, . and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FormTemplate(Document):
    def validate(self):

        if not self.is_new():

            old_doc = self.get_doc_before_save()

            if old_doc and old_doc.status == "Published":

                changed = []

                for field in self.meta.fields:

                    if field.fieldname == "status":
                        continue

                    if self.get(field.fieldname) != old_doc.get(field.fieldname):
                        changed.append(field.label)

                if changed:
                    frappe.throw(
                        "Published Form Templates cannot be modified."
                    )
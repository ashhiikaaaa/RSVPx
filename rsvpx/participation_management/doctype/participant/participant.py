# Copyright (c) 2026, . and contributors
# For license information, please see license.txt

# Copyright (c) 2026
# For license information, please see license.txt

import os
import json
import secrets
import qrcode

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
from frappe.utils.file_manager import save_file


class Participant(Document):

    def after_insert(self):

        qr_token = secrets.token_hex(16)

        registration = frappe.get_doc(
            "Registration Submission",
            self.registration_submission
        )

        qr_payload = {}

        qr_pass = frappe.get_doc({

            "doctype": "QR Pass",

            "participant": self.name,
            "event": self.event,
            "registration_submission": self.registration_submission,

            "qr_token": qr_token,
            "qr_data": "",
            "pass_status": "Generated",
            "generated_on": now_datetime()

        })

        qr_pass.insert(ignore_permissions=True)

        qr_payload["QR Pass"] = qr_pass.name

        form_template = frappe.get_doc(
            "Form Template",
            registration.form_template
        )

        fields = []

        for response in registration.responses:

            for form_field in form_template.fields:

                if form_field.field_name == response.form_field:

                    if form_field.show_in_qr:

                        fields.append({
                            "order": form_field.qr_display_order or 999,
                            "label": form_field.label,
                            "value": response.response_value
                        })

                    break

        fields.sort(key=lambda x: x["order"])

        for field in fields:
            qr_payload[field["label"]] = field["value"]



        # fields = []

        # for response in registration.responses:

        #     field = frappe.db.get_value(
        #         "Form Field",
        #         response.form_field,
        #         ["label", "show_in_qr", "qr_display_order"],
        #         as_dict=True
        #     )

        #     if field and field.show_in_qr:

        #         fields.append({
        #             "order": field.qr_display_order or 999,
        #             "label": field.label,
        #             "value": response.response_value
        #         })

        # fields.sort(key=lambda x: x["order"])

        # for field in fields:
        #     qr_payload[field["label"]] = field["value"]

        # qr_pass.qr_data = json.dumps(
        #     qr_payload,
        #     indent=4
        # )

        qr_pass.qr_data = "\n".join(
            f"{key}: {value}" for key, value in qr_payload.items()
        )

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4
        )

        qr.add_data(qr_pass.qr_data)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color="black",
            back_color="white"
        )

        file_name = f"{qr_pass.name}.png"
        temp_path = f"/tmp/{file_name}"

        img.save(temp_path)

        with open(temp_path, "rb") as f:

            file_doc = save_file(
                fname=file_name,
                content=f.read(),
                dt="QR Pass",
                dn=qr_pass.name,
                is_private=0
            )

        qr_pass.qr_image = file_doc.file_url
        qr_pass.pass_status = "Active"

        qr_pass.save(ignore_permissions=True)

        if os.path.exists(temp_path):
            os.remove(temp_path)
# Copyright (c) 2026, . and contributors
# For license information, please see license.txt

import frappe
import qrcode
import io 

from frappe.model.document import Document


class QRPass(Document):
	def after_insert(self):
		qr_data = self.name
		img = qrcode.make(qr_data)
		output = io.BytesIO()

		img.save(output, format="PNG")
		
		file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": f"{self.name}.png",
            "content": output.getvalue(),
            "attached_to_doctype": "QR Pass",
            "attached_to_name": self.name,
            "is_private": 0
        })

		file_doc.insert(ignore_permissions=True)

		self.qr_image = file_doc.file_url

		self.save(ignore_permissions=True)
# Copyright (c) 2026, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Gate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		event: DF.Link
		gate_code: DF.Data
		gate_name: DF.Data | None
		gate_type: DF.Literal["Entry", "Exit", "VIP", "Backstage", "Sponsor"]
		status: DF.Literal["Active", "Inactive", "Suspended"]
	# end: auto-generated types
	pass

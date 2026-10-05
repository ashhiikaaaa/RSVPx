# Copyright (c) 2026, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CheckInlog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		gate: DF.Link
		participant: DF.Link
		qr_pass: DF.Link
		scan_result: DF.Literal["Success", "Duplicate", "Invalid", "Blocked"]
		scan_time: DF.Datetime | None
		scanned_by: DF.Link
	# end: auto-generated types
	pass

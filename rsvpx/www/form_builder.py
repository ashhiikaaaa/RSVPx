import frappe


@frappe.whitelist()
def get_form_template(name):

    doc = frappe.get_doc("Form Template", name)

    return {
        "name": doc.name,
        "form_name": doc.form_name,
        "form_code": doc.form_code,
        "event": doc.event,
        "description": doc.description,
        "status": doc.status,
        "open_date": doc.open_date,
        "close_date": doc.close_date,
        "form_category": doc.form_category,
        "custom": doc.custom,
        "registration_type": doc.registration_type,

        "allow_edit_after_submit": doc.allow_edit_after_submit,
        "approval_required": doc.approval_required,
        "auto_approve": doc.auto_approve,
        "max_submissions": doc.max_submissions,

        "allow_team_registration": doc.allow_team_registration,
        "maximum_team_size": doc.maximum_team_size,
        "minimum_team_size": doc.minimum_t,

        "payment_required": doc.payment_required,
        "amount": doc.amount,
        "currency": doc.currency,

        "otp_required": doc.otp_required,
        "whatsapp_enabled": doc.whatsapp_enabled,
        "email_enabled": doc.email_enabled,
        "redirect_url": doc.redirect_url,
        "success_message": doc.success_message,

        "fields": [
            {
                "name": row.name,
                "label": row.label,
                "field_name": row.field_name,
                "field_type": row.field_type,
                "field_purpose": row.field_purpose,
                "required": row.required,
                "is_active": row.is_active,
                "show_in_qr": row.show_in_qr,
                "qr_display_order": row.qr_display_order
            }
            for row in doc.fields
        ]
    }

@frappe.whitelist()
def save_form_template(name, data):

    import json

    if isinstance(data, str):
        data = json.loads(data)

    doc = frappe.get_doc("Form Template", name)

    if doc.status == "Published":
        frappe.throw("Published Form Templates cannot be modified.")

    # Main Form Template fields

    doc.form_name = data.get("form_name")
    doc.form_code = data.get("form_code")
    doc.event = data.get("event")
    doc.description = data.get("description")

    doc.open_date = data.get("open_date")
    doc.close_date = data.get("close_date")

    doc.form_category = data.get("form_category")
    doc.custom = data.get("custom")
    doc.registration_type = data.get("registration_type")

    doc.allow_edit_after_submit = data.get(
        "allow_edit_after_submit"
    )

    doc.approval_required = data.get(
        "approval_required"
    )

    doc.auto_approve = data.get(
        "auto_approve"
    )

    doc.max_submissions = data.get(
        "max_submissions"
    )

    doc.allow_team_registration = data.get(
        "allow_team_registration"
    )

    doc.maximum_team_size = data.get(
        "maximum_team_size"
    )

    doc.minimum_t = data.get(
        "minimum_t"
    )

    doc.payment_required = data.get(
        "payment_required"
    )

    doc.amount = data.get(
        "amount"
    )

    doc.currency = data.get(
        "currency"
    )

    doc.otp_required = data.get(
        "otp_required"
    )

    doc.whatsapp_enabled = data.get(
        "whatsapp_enabled"
    )

    doc.email_enabled = data.get(
        "email_enabled"
    )

    doc.redirect_url = data.get(
        "redirect_url"
    )

    doc.success_message = data.get(
        "success_message"
    )

    # Replace child table

    doc.set("fields", [])

    for field in data.get("fields", []):

        doc.append("fields", {
            "label": field.get("label"),
            "field_name": field.get("field_name"),
            "field_type": field.get("field_type"),
            "field_purpose": field.get("field_purpose"),
            "required": field.get("required", 0),
            "is_active": field.get("is_active", 1),
            "show_in_qr": field.get("show_in_qr", 0),
            "qr_display_order": field.get(
                "qr_display_order", 0
            )
        })

    doc.save()

    return {
        "success": True,
        "name": doc.name
    }
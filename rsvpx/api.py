import frappe
import random
import secrets
import string
from frappe.utils.password import update_password
from frappe.utils import add_to_date, now_datetime


@frappe.whitelist()
def send_event_admin_otp(event):

    # frappe.throw("OTP SENT SUCCESSFULLY")

    event_doc = frappe.get_doc("RSVPX Event", event)

    if event_doc.email_verified:
        frappe.throw("Event Admin email is already verified.")

    # Delete any previous pending OTPs
    existing = frappe.get_all(
        "OTP Verification",
        filters={
            "reference_doctype": "RSVPX Event",
            "reference_name": event_doc.name,
            "status": "Pending"
        },
        pluck="name"
    )

    for name in existing:
        frappe.delete_doc("OTP Verification", name, force=True)

    otp = str(random.randint(100000, 999999))

    otp_doc = frappe.get_doc({
        "doctype": "OTP Verification",

        "reference_doctype": "RSVPX Event",
        "reference_name": event_doc.name,

        "email": event_doc.admin_email,

        "otp": otp,

        "generated_on": now_datetime(),
        "expires_on": add_to_date(now_datetime(), minutes=10),

        "status": "Pending"
    })

    otp_doc.insert(ignore_permissions=True)

    try:
        # frappe.throw(event_doc.admin_email)
        frappe.sendmail(
                recipients=[event_doc.admin_email],
                subject="RSVPX Event Admin Verification",
                message=f"""
                Hello {event_doc.admin_name},
        
                <br><br>
        
                Your verification OTP is:
        
                <h2>{otp}</h2>
        
                This OTP will expire in 10 minutes.
        
                <br>
        
                RSVPX
                """
            )
        # frappe.msgprint("Mail function executed")
        
            # return {
            #     "message": "OTP Sent Successfully"
            # }
    except Exception:
            frappe.throw(frappe.get_traceback())

    


@frappe.whitelist()
def verify_event_admin_otp(event, otp):

    try:

        otp_list = frappe.get_all(
            "OTP Verification",
            filters={
                "reference_doctype": "RSVPX Event",
                "reference_name": event,
                "status": "Pending"
            },
            order_by="creation desc",
            limit=1,
            fields=["name"]
        )

        if not otp_list:
            frappe.throw("OTP not found.")

        otp_doc = frappe.get_doc(
            "OTP Verification",
            otp_list[0].name
        )

        if otp_doc.otp != otp:
            frappe.throw("Invalid OTP.")

        if now_datetime() > otp_doc.expires_on:
            frappe.throw("OTP has expired.")

        otp_doc.status = "Verified"
        otp_doc.verified_on = now_datetime()
        otp_doc.save(ignore_permissions=True)

        event_doc = frappe.get_doc("RSVPX Event", event)

        # Create User
        user, password = create_event_admin_user_login(event_doc)

        # Mark Event Email Verified
        event_doc.email_verified = 1
        event_doc.save(ignore_permissions=True)

        # Create Event User
        event_doc.create_event_admin_user()

        # Send Login Credentials
        frappe.sendmail(
            recipients=[event_doc.admin_email],
            subject="Welcome to RSVPX - Event Admin Account",
            message=f"""
            Hello {event_doc.admin_name},

            <br><br>

            Your Event Admin account has been created successfully.

            <br><br>

            <b>Login URL</b><br>
            {frappe.utils.get_url()}/login

            <br><br>

            <b>User ID</b><br>
            {event_doc.admin_email}

            <br><br>

            <b>Temporary Password</b><br>
            {password}

            <br><br>

            Please change your password after your first login.

            <br><br>

            Regards,<br>
            RSVPX Team
            """
        )

        frappe.db.commit()

        return {
            "message": "Email Verified Successfully"
        }

    except Exception:

        frappe.db.rollback()
        frappe.throw(frappe.get_traceback())

def create_event_admin_user_login(event_doc):

    # If user already exists, generate a NEW temporary password
    if frappe.db.exists("User", event_doc.admin_email):
        user = frappe.get_doc("User", event_doc.admin_email)
        alphabet = string.ascii_letters + string.digits
        password = "".join(secrets.choice(alphabet) for _ in range(10))
        update_password(user.name, password)
        return user, password

    # Create new password
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for _ in range(10))

    user = frappe.get_doc({
        "doctype": "User",
        "email": event_doc.admin_email,
        "first_name": event_doc.admin_name,
        "enabled": 1,
        "user_type": "System User",
        "role_profile_name": "Event Admin",
        "send_welcome_email": 0
    })

    user.insert(ignore_permissions=True)

    update_password(user.name, password)

    return user, password


def get_form_fields(form_template):

    doc = frappe.get_doc("Form Template", form_template)

    fields = []

    for field in doc.fields:

        fields.append({

            "form_field": field.field_name,
            "field_label": field.label,

            "required": field.required,
            "show_in_qr": field.show_in_qr,
            "qr_display_order": field.qr_display_order

        })
        # frappe.msgprint(str(field.as_dict()))

    return fields


# import frappe
# @frappe.whitelist()
# def get_form_fields(form_template):

#     doc = frappe.get_doc("Form Template", form_template)

#     fields = []

#     for field in doc.fields:

#         fields.append({

#             # Form Field document name (Link)
#             "form_field": field.form_field,

#             "field_label": field.label,

#             "required": field.required,

#             "show_in_qr": field.show_in_qr,

#             "qr_display_order": field.qr_display_order

#         })

#     return fields

# import frappe

# @frappe.whitelist()
# def get_form_fields(form_template):

#     doc = frappe.get_doc("Form Template", form_template)

#     frappe.throw(str(len(doc.fields)))

# import frappe

# @frappe.whitelist()
# def get_form_fields(form_template):

#     frappe.throw("API HIT")

#     return []

# import frappe

# @frappe.whitelist()
# def get_form_fields(form_template):
#     doc = frappe.get_doc("Form Template", form_template)

#     fields = []

#     for field in doc.fields:
#             fields.append({
#                 "form_field": field.field_name,
#                 "field_label": field.label
#             })

#     return fields
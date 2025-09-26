# airplane_mode/airplane_mode/doctype/rent_payment/rent_payment_reminder.py

import frappe
from frappe.utils import nowdate
from frappe.model.document import Document

def send_rent_due_reminder():
    settings = frappe.get_single("Airplane Mode Settings")
    if not settings.enable_rent_reminders:
        frappe.logger().info("Rent reminders are disabled in settings.")
        return    
    today = nowdate()

    rent_due_payments = frappe.get_all(
        "Rent Payment",
        filters={
            "due_date": ["<=", today],
            "amount_paid": 0
        },
        fields=["name", "tenant", "shop"]
    )

    for payment in rent_due_payments:
        rent_payment = frappe.get_doc("Rent Payment", payment["name"])

        tenant = frappe.db.get_value(
            "Tenant",
            rent_payment.tenant,
            ["tenant_name", "email"],
            as_dict=True
        )

        if tenant and tenant.email:
            frappe.sendmail(
                recipients=[tenant.email],
                subject=f"Rent Due Reminder for {rent_payment.shop}",
                message=f"""
                Dear {tenant.tenant_name},<br><br>
                Your rent payment for <b>{rent_payment.shop}</b> is due.<br>
                Please make the payment as soon as possible.<br><br>
                Thank you,<br>
                Airport Management
                """
            )
    frappe.logger().info(f"Sent rent reminders for {len(rent_due_payments)} pending payments.")
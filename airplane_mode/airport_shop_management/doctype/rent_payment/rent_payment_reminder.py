# airplane_mode/airplane_mode/doctype/rent_payment/rent_payment_reminder.py

import frappe
from frappe.utils import nowdate
from frappe.model.document import Document

def send_rent_due_reminder():
    today = nowdate()
    rent_due_payments = frappe.get_all('Rent Payment', filters={
        'due_date': ['<=', today],
        'amount_paid': 0
    })
    for payment in rent_due_payments:
        rent_payment = frappe.get_doc('Rent Payment', payment.name)
        tenant_email = rent_payment.tenant_email
        if tenant_email:
            frappe.sendmail(
                recipients=[tenant_email],
                subject=f'Rent Due Reminder for {rent_payment.shop_name}',
                message=f'Hello, {rent_payment.tenant}!\n\nYour rent payment for {rent_payment.shop_name} is due. Please make the payment as soon as possible.\n\nThank you!'
            )
    frappe.log_error("Rent Due Reminder Sent", "Rent Payment Reminder")

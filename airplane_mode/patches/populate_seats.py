import frappe
import random

def execute():
    tickets = frappe.get_all('Airplane Ticket', filters={'seat': ''}, fields=['name'])
    for ticket in tickets:
        random_number = random.randint(1, 99)
        random_letter = random.choice(['A', 'B', 'C', 'D', 'E'])
        seat_value = f"{random_number}{random_letter}"
        ticket_doc = frappe.get_doc('Airplane Ticket', ticket['name'])
        ticket_doc.seat = seat_value
        ticket_doc.save()
    frappe.db.commit()
execute()
# # Copyright (c) 2025, Avi and contributors
# # For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class AirplaneFlight(WebsiteGenerator):
    def before_submit(self):
        self.status = "Completed"
    
    def on_cancel(self):
        self.status = 'Cancelled'
        
def sync_gate_number(doc, method):
	updated_gate_number = doc.gate_number
	tickets = frappe.get_all("Airplane Ticket", filters={"flight": doc.name}, fields=["name"])
	for ticket in tickets:
		ticket_doc = frappe.get_doc("Airplane Ticket", ticket["name"])
		ticket_doc.gate_number = updated_gate_number
		ticket_doc.save()
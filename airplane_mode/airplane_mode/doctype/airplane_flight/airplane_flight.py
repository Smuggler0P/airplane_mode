# Copyright (c) 2025, Avi and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class AirplaneFlight(WebsiteGenerator):
    def before_submit(self):
        self.status = "Completed"

    def on_cancel(self):
        self.status = "Cancelled"

    def on_update(self):
        frappe.enqueue(
            "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_ticket_gates",
            flight=self.name,
            gate_number=self.gate_number,
            queue="short"
        )

@frappe.whitelist()
def update_ticket_gates(flight, gate_number):
    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={"flight": flight},
        fields=["name"]
    )
    for ticket in tickets:
        ticket_doc = frappe.get_doc("Airplane Ticket", ticket["name"])
        ticket_doc.gate_number = gate_number
        ticket_doc.save(ignore_permissions=True)

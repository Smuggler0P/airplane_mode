# # Copyright (c) 2025, Avi and contributors
# # For license information, please see license.txt

import frappe
import random
from frappe.model.document import Document

class AirplaneTicket(Document):
    def before_submit(self):
        if (self.status != "Boarded"):
            frappe.throw("Cannot submit Airplane Ticket unless status is 'Boarded'")
    def validate(self):
        addon_items = set()
        duplicates = []
        for addon in self.add_ons:
            if addon.item in addon_items:
                duplicates.append(addon)
            else:
                addon_items.add(addon.item)
        for duplicate in duplicates:
            self.add_ons.remove(duplicate)
        total_addons_amount = sum(addon.amount for addon in self.add_ons)
        self.total_amount = self.flight_price + total_addons_amount

    def before_insert(self):
        self.cheak_overbooking()
        self.assign_seat()

    def assign_seat(self):
        random_integer = random.randint(1, 99)
        random_letter = random.choice(['A', 'B', 'C', 'D', 'E'])
        self.seat = f"{random_integer}{random_letter}"

    def cheak_overbooking(self):
        airplane = frappe.get_doc('Airplane' , self.airplane)
        tickets_count = frappe.db.count('Airplane Ticket' , {'airplane' : self.airplane})

        if tickets_count >= airplane.capacity:
            frappe.throw(f"Cannot create a ticket. AIrplane {airplane.name} is fully booked.")

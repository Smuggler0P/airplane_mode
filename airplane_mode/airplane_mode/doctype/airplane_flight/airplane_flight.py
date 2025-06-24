# # Copyright (c) 2025, Avi and contributors
# # For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class AirplaneFlight(WebsiteGenerator):
    def before_submit(self):
        self.status = "Completed"
    
    def on_cancel(self):
        self.status = 'Cancelled'

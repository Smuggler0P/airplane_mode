# Copyright (c) 2025, Avi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate
from datetime import timedelta


class Contract(Document):
	def before_insert(doc):
		if not doc.shop_rent_amount:
			settings = frappe.get_single("Airplane Mode Settings")
			doc.shop_rent_amount = settings.default_rent_amount

	def validate(self):
		# Validate contract dates
		if self.start_date and self.end_date:
			start_date = getdate(self.start_date)
			end_date = getdate(self.end_date)
			
			# Ensure end_date is at least one year after start_date
			if end_date < start_date + timedelta(days=365):
				frappe.throw(
					("Contract End Date must be at least one year after the Contract Start Date."),
					title=("Invalid Contract Dates")
				)
		
		# Validate Shop status
		if self.airport_shop_allotted:
			shop_doc = frappe.get_doc("Airport Shop", self.airport_shop_allotted)  # Fetch the linked Shop document
			# Check if the shop status is 'Leased'
			if shop_doc.status == "Occupied":
				frappe.throw(
					("Shop {0} is already leased and cannot be contracted.").format(shop_doc.name),
					title=("Shop Leased")
				)

	def after_insert(self):
		# Change the shop status to 'Occupied' once the tenant contract is created
		if self.airport_shop_allotted:
			shop_doc = frappe.get_doc("Airport Shop", self.airport_shop_allotted)
			shop_doc.status = "Occupied"
			shop_doc.contract_expiry = self.end_date

			shop_doc.save(ignore_permissions=True)  # Save the changes to the Shop document

			frappe.msgprint(
				("Shop {0} has been marked as 'Occupied'.").format(shop_doc.name),  # Use actual field from Shop
				alert=True
			)

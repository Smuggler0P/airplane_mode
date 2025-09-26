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
		if self.start_date and self.end_date:
			start_date = getdate(self.start_date)
			end_date = getdate(self.end_date)
			if end_date < start_date + timedelta(days=365):
				frappe.throw(
					("Contract End Date must be at least one year after the Contract Start Date."),
					title=("Invalid Contract Dates")
				)
		if self.airport_shop_allotted:
			shop_doc = frappe.get_doc("Airport Shop", self.airport_shop_allotted)
			if shop_doc.status == "Occupied":
				frappe.throw(
					("Shop {0} is already leased and cannot be contracted.").format(shop_doc.name),
					title=("Shop Leased")
				)

	def after_insert(self):
		if self.airport_shop_allotted:
			shop_doc = frappe.get_doc("Airport Shop", self.airport_shop_allotted)
			shop_doc.status = "Occupied"
			shop_doc.contract_expiry = self.end_date
			shop_doc.save(ignore_permissions=True)
			frappe.msgprint(
				("Shop {0} has been marked as 'Occupied'.").format(shop_doc.name),
				alert=True
			)

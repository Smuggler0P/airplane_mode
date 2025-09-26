# Copyright (c) 2025, Avi and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data
# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        _("Airport") + ":Link/Airport:250",
        _("Total Shops") + ":Int:120"
    ]

def get_data(filters):
    conditions = ""
    if filters.get("airport"):
        conditions = "where airport = %(airport)s"

    results = frappe.db.sql(f"""
        SELECT 
            airport, 
            COUNT(name) as total_shops
        FROM `tabAirport Shop`
        {conditions}
        GROUP BY airport
        ORDER BY airport ASC
    """, filters, as_dict=1)

    return [[row.airport, row.total_shops] for row in results]

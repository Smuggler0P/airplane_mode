# Copyright (c) 2025, Avi and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        _("Shop Number") + ":Data:120",
        _("Airport") + ":Link/Airport:200",
        _("Shop Type") + ":Data:100",
        _("Area (sq ft)") + ":Float:100"
    ]

def get_data(filters):
    conditions = "WHERE status = 'Occupied'"
    
    if filters and filters.get("airport"):
        conditions += " AND airport = %(airport)s"

    results = frappe.db.sql(f"""
        SELECT 
            shop_number,
            airport,
            shop_type,
            area_sq_ft
        FROM `tabAirport Shop`
        {conditions}
        ORDER BY airport, shop_number
    """, filters, as_dict=1)

    return [[
        row.shop_number,
        row.airport,
        row.shop_type,
        row.area_sq_ft,
    ] for row in results]

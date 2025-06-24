# Copyright (c) 2025, Avi and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    data = frappe.db.sql("""
        SELECT airline, SUM(total_amount) as revenue
        FROM `tabAirplane Ticket`
        GROUP BY airline
    """, as_dict=True)
    total_revenue = sum(row['revenue'] for row in data)
    columns = [
        {"fieldname": "airline", "label": "Airline", "fieldtype": "Link", "options": "Airline", "width": 200},
        {"fieldname": "revenue", "label": "Revenue", "fieldtype": "Currency", "width": 150}
    ]
    chart = {
        "type": "donut",
        "data": {
            "labels": [row['airline'] for row in data],
            "datasets": [{"values": [row['revenue'] for row in data]}]
        }
    }
    report_summary = [{"value": total_revenue, "label": "Total Revenue", "datatype": "Currency"}]
    return columns, data, None, chart, report_summary


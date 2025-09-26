// Copyright (c) 2025, Avi and contributors
// For license information, please see license.txt

frappe.query_reports["Available Shops"] = {
  "filters": [
    {
      "fieldname": "airport",
      "label": "Airport",
      "fieldtype": "Link",
      "options": "Airport",
      "reqd": 0
    }
  ]
};

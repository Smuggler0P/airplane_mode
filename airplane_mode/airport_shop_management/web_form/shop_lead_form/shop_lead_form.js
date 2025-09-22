frappe.ready(function() {
    // Step 1: Fetch airport shops where status = 'Available'
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Airport Shop",
            filters: {
                status: "Available"
            },
            fields: ["name"]
        },
        callback: function(response) {
            const available_shops = response.message.map(shop => shop.name);

            // Step 2: Set these names into the link field manually
            frappe.web_form.fields_dict.shop.set_data(available_shops);
        }
    });
});

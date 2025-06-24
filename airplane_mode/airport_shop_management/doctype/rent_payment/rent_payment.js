// Copyright (c) 2025, Avi and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Rent Payment", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Rent Payment', {
    refresh: function(frm) {
        toggle_amount_paid_field(frm);
    },
    contract: function(frm) {
        toggle_amount_paid_field(frm);
    }
});
function toggle_amount_paid_field(frm) {
    if (!frm.doc.contract) {
        frm.fields_dict['amount_paid'].df.hidden = 1;
    } else {
        frm.fields_dict['amount_paid'].df.hidden = 0;
    }
    frm.refresh_field('amount_paid');
}
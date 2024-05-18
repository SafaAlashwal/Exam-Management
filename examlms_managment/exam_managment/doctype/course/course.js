// Copyright (c) 2024, Safa and contributors
// For license information, please see license.txt

frappe.ui.form.on('Course', {
	onload: function (frm) {
		frm.set_query("name1", "chapter", function () {
			return {
				filters: {
					course: frm.doc.name,
				},
			};
		});
	}
});

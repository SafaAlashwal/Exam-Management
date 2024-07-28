// Copyright (c) 2024, Safa and contributors
// For license information, please see license.txt

frappe.ui.form.on('Question', {
		refresh(frm) {
			// msgprint(frm.doc.custom_course);
			frm.set_query("custom_chapter", function() {
			  return {
				"filters": {
				  "course": frm.doc.custom_course
				}
			  };
			});
		}
});

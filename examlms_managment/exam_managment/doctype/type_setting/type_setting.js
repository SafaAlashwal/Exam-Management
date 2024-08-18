// Copyright (c) 2024, Safa and contributors
// For license information, please see license.txt

frappe.ui.form.on("Type Setting", {
    after_save: function(frm) {

		if (frm.doc.type === 'Percentage'){
			frappe.call({
				method: 'get_questions2',
				doc:frm.doc,
			});	
		}
		else if (frm.doc.type === 'Number'){
			frappe.call({
				method: 'get_questions',
				doc:frm.doc,
			});
		}
		else {
			console.error("Invalid type");
		}

		
	}
});

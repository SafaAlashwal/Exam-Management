// frappe.query_reports["Students Report"] = {
// 	"filters": [
// {		
// 		"fieldname": "student_name",
// 		"label": __("Student Name"),
// 		"fieldtype": "Data",
// 		"default": ""
// 	}
// 	]
// };
// report.js
// common.js
frappe.ui.form.on("Students Report", "onload", function() {
    frappe.add_css(`
        .frappe-datatable td[data-fieldname="course_details"] {
            height: 500px; /* يمكنك تعديل هذا الرقم حسب الحاجة */
            overflow-y: auto;
        }
    `);
});
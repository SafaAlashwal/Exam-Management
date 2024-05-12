// Copyright (c) 2024, Safa and contributors
// For license information, please see license.txt

frappe.ui.form.on('Create Exam', {
    course: function (frm){
        console.log(frm.doc.course);
        frm.set_query("drname", "course", function(doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            return {
              filters: {
                "course": child.course
              }
            };
          });
      },
    collage: function (frm){
        console.log(frm.doc.collage);
        frm.set_query("department", function() {
          return {
            "filters": {
              "collage": frm.doc.collage
            }
          };
        });
      },
      
    total_question : function(frm) {
    // console.log("hhhhhh")
        frm.add_custom_button(__("Fetch Question"), function() {
            frappe.call({
                method: "fetch_question",
                doc: frm.doc,
                callback: () => {
                    frappe.msgprint("Done")
                    frm.save(); // حفظ الوثيقة بعد استرداد الأسئلة
  
                }
            });
        });
    },
    // Rest of the code...

  course_name : function (frm){
    console.log(frm.doc.course_name);
    frm.set_query("chapter", function() {
      return {
        "filters": {
          "course_name": frm.doc.course_name
        }
      };
    });
  },
  after_save(frm) {
    frappe.call({
      method: "examlms_managment.exam_managment.doctype.model.model.Add_Model",
      // doc: frm.doc,
      // args: { "self": self },
      callback: () => {
        frappe.msgprint("Done")
      }
    })
  }
});
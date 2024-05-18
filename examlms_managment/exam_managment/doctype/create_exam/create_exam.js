// Copyright (c) 2024, Safa and contributors
// For license information, please see license.txt

frappe.ui.form.on('Create Exam', {
  refresh : function (frm){
    frm.add_custom_button(__("Fetch Question"), function() {
      if (frm.doc.total_question === null || frm.doc.total_question === undefined) {
        frappe.msgprint("Please enter the total number of questions.");
    } else {
        frappe.call({
            method: "fetch_question",
            doc: frm.doc,
            callback: () => {
                frappe.msgprint("Done");
                frm.save();
            }
        });
    }
  });

  },
      ///////////// Filter Department ////////////////
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

      ///////////// Filter Chapter ////////////////
      course: function(frm) {
        frm.set_query('name1', 'chapter', function() {
          return {
            filters: {
              course: frm.doc.course
            }
          };
        });
      },
      // doctor: function(frm) {
      //   frm.set_query('course', function() {
      //     return {
      //       filters: {
      //         doctor: frm.doc.doctor
      //       }
      //     };
      //   });
      // },
      ///////////// Fetch Question ////////////////

      ///////////// Save in Model ////////////////
      after_save(frm) {
        frm.call({
          method: "examlms_managment.exam_managment.doctype.model.model.Add_Model",
          // doc: frm.doc,
          // args: { "self": self },
          callback: () => {
            frappe.msgprint("Done")
          }
        })
  },
  doctor : function(frm) {
    frm.call({
      method: 'get_filtered_chapters',
      args: {
        doctor: frm.doc.doctor
      },
      doc: frm.doc,
      callback: (res) => {
        let courses = res.message?.courses;
          frm.set_query('course', () => ({ filters: { name: ['in', courses] } }));
          // frm.set_value('course', courses);
        }
      // }
    });
  }
});
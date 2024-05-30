// Copyright (c) 2024, Safa and contributors
// For license information, please see license.txt

frappe.ui.form.on('Create Exam', {
  refresh : function (frm){
    frm.add_custom_button(__("Fetch Question"), function() {
        frappe.call({
            method: "fetch_question",
            doc: frm.doc,
            callback: () => {
                frm.save();
            }
        });
  });


        ///////////// Filter Department ////////////////
  frm.set_query("department", function() {
    return {
      "filters": {
        "collage": frm.doc.collage
      }
    };
  });



      ///////////// Filter Chapter ////////////////
  frm.set_query('name1', 'chapter', function() {
    return {
      filters: {
        course: frm.doc.course
      }
    };
  });



    ///////////// Filter Course ////////////////
  frm.call({
    method: 'get_filtered_course',
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

      ///////////// Filter Levels ////////////////
  frm.call({
    method: 'get_filtered_level',
    args: {
      department: frm.doc.department
    },
    doc: frm.doc,
    callback: (res) => {
      let levels = res.message?.levels;
        frm.set_query('level', () => ({ filters: { name: ['in', levels] } }));
        // frm.set_value('course', courses);
      }
    // }
  });


  },

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



  ///////////////////  Set Total Question /////////////////
  difficulty_level : function(frm) {
    frm.call({
      method: 'get_number_question_list',
      args: {
        difficulty_level: frm.doc.difficulty_level
      },
      doc: frm.doc,
      callback: (res) => {
        let total_question = res.message?.total_question;
        let number_of_questions = res.message?.number_of_questions;

          frm.set_value('total_question', total_question);
          frm.set_value('number_of_questions', number_of_questions);

        }
    });
  },
});
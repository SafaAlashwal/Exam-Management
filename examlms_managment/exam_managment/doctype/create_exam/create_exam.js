// Copyright (c) 2024, Safa and contributors
// For license information, please see license.txt

frappe.ui.form.on('Create Exam', {
  onload: function(frm) {
    if (!frm.doc.__islocal) {
        return;
    }

    frappe.db.exists('Doctor', frappe.session.user).then(exists => {
        if (exists) {
            frm.set_value('doctor', frappe.session.user);
        } else {
            frm.set_value('doctor', '');
        }
    });
},
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

  // var doc_value = frm.doc.doctor; // الحصول على قيمة الحقل "doctor"
  
  // إذا كان الحقل من نوع "link"، يمكنك الحصول على القيمة التي يشير إليها الحق
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

  },

      ///////////// Save in Model ////////////////
      before_submit: function(frm) {
        frappe.call({
            method: 'validate_question_marks',
            doc: frm.doc,
            callback: function(response) {
                if (response.message === 'Validation passed') {
                    frm.savesubmit();
                }
            },
            error: function(error) {
                frappe.msgprint(__('An error occurred during validation.'));
                frappe.validated = false;
            }
        });
    },    
    on_submit(frm) {
      frm.call({
          method: "examlms_managment.exam_managment.doctype.model.model.Add_Model",
          args: {
              create_exam_doc_name: frm.doc.name
          },
          callback: (response) => {
            frappe.msgprint("hhhhhhhh");
              // Check if the response contains the error message
              const error_message = "Not enough unique questions of type Choices and level Hard to create the models.";
              if (response.message.includes(error_message)) {
                  // Prevent submit
                  frappe.msgprint(__("Submit action cancelled: " + error_message));
                  frappe.validated = false;
              } else {
                  frappe.msgprint("Done");
              }
          },
          error: (error) => {
              // Handle error case if needed
              frappe.msgprint(__("An error occurred while creating models "));
              frappe.validated = false;
          }
      });
  },
/////////////////////////////////////      
  department: function(frm){
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
    ///////////// Filter Course ////////////////
    doctor : function(frm){
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
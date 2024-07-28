// Copyright (c) 2024, Safa and contributors
// For license information, please see license.txt

frappe.ui.form.on("Model", {
  // refresh(frm) {
  //   frm.add_custom_button(__("See in Webset"), function () {
  //     let name = frm.doc.name;
  //     console.log(name)
  //     if (name) {
  //       window.location.href = `/vue/index?name=${name}`;
  //     } else {
  //       frappe.msgprint(__("Please make sure the ID Exam is available."));
  //     }
  //   });
  // },
  setup(frm) {
    calculateTotalMarks(frm);
  },
  before_save(frm) {
    calculateTotalMarks(frm);
  }
});

function calculateTotalMarks(frm) {
  let totalMarks = 0;
  if (frm.doc.question) {
    frm.doc.question.forEach((question) => {
      if (question.question_mark) {
        totalMarks += question.question_mark;
      }
    });
  }
  frm.set_value("total_marks", totalMarks);
  frm.refresh_field("total_marks");
}
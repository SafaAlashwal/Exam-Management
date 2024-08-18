// Copyright (c) 2024, Safa and contributors
// For license information, please see license.txt

frappe.ui.form.on("Model", {
  refresh(frm) {
    frm.add_custom_button(__("Preview"), function () {
      var data = {
          doctor: frm.doc.doctor,
          collage: frm.doc.collage,
          questions: frm.doc.question  // Ensure this field exists in the model
      };
      var dialog = new frappe.ui.Dialog({
          title: __("Preview"),
          fields: [
              {
                  fieldtype: 'Data',
                  label: __('Doctor'),
                  fieldname: 'doctor',
                  default: data.doctor,
                  read_only: true
              },
              {
                  fieldtype: 'Data',
                  label: __('Collage'),
                  fieldname: 'collage',
                  default: data.collage,
                  read_only: true
              },
              {
                  fieldtype: 'HTML',
                  label: __('Questions and Answers'),
                  fieldname: 'questions',
                  options: generate_questions_html(data.questions)
              }
          ],
          size: 'large'  // Possible values: 'small', 'medium', 'large'
      });
  
      dialog.show();
  });
  },
  setup(frm) {
    calculateTotalMarks(frm);
  },
  before_save(frm) {
    calculateTotalMarks(frm);
  }
});
function generate_questions_html(questions) {
  let html = `
  <style>
      .question-container {
          margin-bottom: 20px;
          padding: 15px;
          border: 1px solid #ddd;
          border-radius: 5px;
          background-color: #f9f9f9;
      }
      .question-title {
          font-size: 16px;
          font-weight: bold;
          margin-bottom: 10px;
      }
      .options-list {
          list-style-type: none;
          padding: 0;
      }
      .options-list li {
          padding: 8px;
          border: 1px solid #ddd;
          border-radius: 5px;
          background-color: #fff;
          margin-bottom: 5px;
      }
      .correct-answer {
          font-weight: bold;
          color: green;
      }
      .input-question {
          margin-top: 10px;
      }
      .block-parent {
          font-size: 18px; /* Larger font size for block parent */
          font-weight: bold;
          margin-bottom: 10px;
          color: #333; /* Highlight text color */
      }
  </style>
  <div class="questions-wrapper">
  `;

  questions.forEach(q => {
      html += '<div class="question-container">';
      
      // Display block_parent if it exists
      if (q.block_parent) {
          html += `<div class="block-parent">${q.block_parent}</div>`;
      }

      html += `
      <div class="question-title">${q.question_title}</div>
      `;
      
      if (q.question_type === 'User Input') {
          // Display input field if question type is input
          html += `<input type="text" class="form-control input-question" placeholder="Your answer here" />`;
      } else {
          // Display options if question type is not input
          html += `
          <ul class="options-list">
              <li>${q.option_1} ${q.is_correct_1 ? '<span class="correct-answer">(Correct)</span>' : ''}</li>
              <li>${q.option_2} ${q.is_correct_2 ? '<span class="correct-answer">(Correct)</span>' : ''}</li>
              <li>${q.option_3} ${q.is_correct_3 ? '<span class="correct-answer">(Correct)</span>' : ''}</li>
              <li>${q.option_4} ${q.is_correct_4 ? '<span class="correct-answer">(Correct)</span>' : ''}</li>
          </ul>
          `;
      }

      html += '</div>';
  });

  html += '</div>';
  return html;
}



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
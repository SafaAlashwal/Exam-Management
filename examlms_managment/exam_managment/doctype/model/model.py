import frappe
from frappe.model.document import Document
import random

class Model(Document):
    pass

@frappe.whitelist(allow_guest=True)
def Add_Model():
    create_exam_docs = frappe.get_all('Create Exam')
    if create_exam_docs:
        create_exam_doc = frappe.get_doc('Create Exam', create_exam_docs[0].name)
        num_models = create_exam_doc.number_of_models

        for _ in range(num_models):
            model_doc = frappe.new_doc("Model")
            model_doc.collage = create_exam_doc.collage
            model_doc.doctor = create_exam_doc.doctor
            model_doc.department = create_exam_doc.department
            model_doc.level = create_exam_doc.level
            model_doc.course = create_exam_doc.course
            # frappe.msgprint(create_exam_doc.name)
            model_doc.id_exam = create_exam_doc.name



            question_list = create_exam_doc.total_question_list

            if question_list:
                num_questions = create_exam_doc.number_of_questions
                num_questions = min(num_questions, len(question_list))
                num_questions = max(num_questions, 0)

                if create_exam_doc.random_question:
                    questions = random.sample(question_list, num_questions)
                else:
                    questions = question_list[:num_questions]
                    random.shuffle(questions)

                for question in questions:
                    child_doc = model_doc.append("question", {
                        "question": question.question,
                        "question_title": question.question_title,
						"question_type": question.question_type,
						"question_degree" : question.question_degree,
						"difficulty_degree" : question.difficulty_degree,
                        # "question_text": question.question
                    })

                model_doc.insert()
                frappe.db.commit()
            else:
                frappe.msgprint("No questions available")
    else:
        frappe.msgprint("No Create Exam documents found")
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
        random_question = create_exam_doc.random_question

        question_list = create_exam_doc.total_question_list.copy()
        type_setting_doc = frappe.get_doc('Type Setting', create_exam_doc.difficulty_level)

        if question_list:
            num_questions = create_exam_doc.number_of_questions
            num_questions = min(num_questions, len(question_list))
            num_questions = max(num_questions, 0)

            questions_by_type = {type_setting.type: [] for type_setting in type_setting_doc.exam_structure}
            for question in question_list:
                questions_by_type[question.question_type].append(question)

            existing_models = frappe.get_all("Model", {
                "collage": create_exam_doc.collage,
                "department": create_exam_doc.department,
                "level": create_exam_doc.level,
                "doctor": create_exam_doc.doctor,
                "course": create_exam_doc.course
            })

            def get_selected_questions(available_questions, num_needed):
                if random_question:
                    if len(available_questions) < num_needed:
                        frappe.msgprint("Not enough questions available to generate unique models")
                        return None
                    selected_questions = random.sample(available_questions, num_needed)
                    for question in selected_questions:
                        available_questions.remove(question)
                else:
                    selected_questions = available_questions[:num_needed]
                    random.shuffle(selected_questions)
                return selected_questions

            def add_questions_to_model(model_doc, selected_questions):
                for question in selected_questions:
                    model_doc.append("question", {
                        "question": question.question,
                        "question_title": question.question_title,
                        "question_type": question.question_type,
                        "question_degree": question.question_degree,
                        "difficulty_degree": question.difficulty_degree,
                    })
                model_doc.number_of_questions = num_questions

            for model_data in existing_models:
                model_doc = frappe.get_doc("Model", model_data.name)
                del model_doc.question[:]
                model_questions = []

                for type_setting in type_setting_doc.exam_structure:
                    available_questions = questions_by_type[type_setting.type]
                    if available_questions:
                        selected_questions = get_selected_questions(available_questions, type_setting.number_of_question)
                        if selected_questions is None:
                            return
                        model_questions.extend(selected_questions)

                random.shuffle(model_questions)
                add_questions_to_model(model_doc, model_questions)
                model_doc.save()
                frappe.db.commit()

            new_models_count = max(0, num_models - len(existing_models))
            for _ in range(new_models_count):
                model_doc = frappe.new_doc("Model")
                model_doc.collage = create_exam_doc.collage
                model_doc.doctor = create_exam_doc.doctor
                model_doc.department = create_exam_doc.department
                model_doc.level = create_exam_doc.level
                model_doc.course = create_exam_doc.course
                model_doc.id_exam = create_exam_doc.name
                model_doc.difficulty_level = create_exam_doc.difficulty_level
                model_doc.number_of_questions = num_questions

                model_questions = []

                for type_setting in type_setting_doc.exam_structure:
                    available_questions = questions_by_type[type_setting.type]
                    if available_questions:
                        selected_questions = get_selected_questions(available_questions, type_setting.number_of_question)
                        if selected_questions is None:
                            return
                        model_questions.extend(selected_questions)

                random.shuffle(model_questions)
                add_questions_to_model(model_doc, model_questions)
                model_doc.insert()
                frappe.db.commit()

        else:
            frappe.msgprint("No questions available")
    else:
        frappe.msgprint("No Create Exam documents found")

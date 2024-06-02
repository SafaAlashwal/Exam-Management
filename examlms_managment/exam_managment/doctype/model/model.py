import frappe
from frappe.model.document import Document
import random

class Model(Document):
    pass

@frappe.whitelist(allow_guest=True)
def Add_Model():
    create_exam_docs = frappe.get_all('Create Exam')
    if not create_exam_docs:
        frappe.msgprint("No Create Exam documents found")
        return

    for create_exam_doc in create_exam_docs:
        create_exam_doc = frappe.get_doc('Create Exam', create_exam_doc.name)
        num_models = create_exam_doc.number_of_models
        random_question = create_exam_doc.random_question

        type_setting_doc = frappe.get_doc('Type Setting', create_exam_doc.difficulty_level)
        exam_structure = type_setting_doc.exam_structure

        # Check if models with id_exam already exist
        existing_models = frappe.get_all('Model', filters={'id_exam': create_exam_doc.name})

        # Keep track of selected questions
        selected_questions = []

        for index in range(num_models):
            if existing_models:
                # Update existing model
                existing_model = existing_models.pop(0)
                model_doc = frappe.get_doc('Model', existing_model.name)
                model_doc.set('question', [])  # Clear existing questions
                message = f"Model {index + 1} updated with"
            else:
                # Create a new model
                model_doc = frappe.new_doc("Model")
                message = f"Model {index + 1} created with"

            model_doc.collage = create_exam_doc.collage
            model_doc.doctor = create_exam_doc.doctor
            model_doc.department = create_exam_doc.department
            model_doc.level = create_exam_doc.level
            model_doc.course = create_exam_doc.course
            model_doc.id_exam = create_exam_doc.name
            model_doc.difficulty_level = create_exam_doc.difficulty_level

            if random_question:
                # Logic to randomly select unique questions and append to model_doc
                available_questions = [q for q in create_exam_doc.total_question_list if q not in selected_questions]
                model_questions_list = []
                for type_setting in exam_structure:
                    question_type = type_setting.type
                    question_level = type_setting.question_level
                    question_count = type_setting.number_of_question

                    question_type_list = [q for q in available_questions if q.question_type == question_type and q.difficulty_degree == question_level]

                    if len(question_type_list) < question_count:
                        frappe.throw(f"Not enough unique questions of type {question_type} and level {question_level} to create the models.")

                    selected_questions_for_model = random.sample(question_type_list, question_count)
                    model_questions_list.extend(selected_questions_for_model)
                    selected_questions.extend(selected_questions_for_model)
                    available_questions = [q for q in available_questions if q not in selected_questions_for_model]

                random.shuffle(model_questions_list)

                for question in model_questions_list:
                    model_doc.append("question", {
                        "question": question.question,
                        "question_title": question.question_title,
                        "question_type": question.question_type,
                        "question_degree": question.question_degree,
                        "difficulty_degree": question.difficulty_degree,
                        "block_parent": question.block_parent
                    })

            else:
                # Logic to select questions without randomization and append to model_doc
                selected_questions_list = []
                for type_setting in exam_structure:
                    question_type = type_setting.type
                    question_level = type_setting.question_level
                    question_count = type_setting.number_of_question

                    question_type_list = [q for q in create_exam_doc.total_question_list if q.question_type == question_type and q.difficulty_degree == question_level]

                    if len(question_type_list) < question_count:
                        frappe.throw(f"Not enough questions of type {question_type} and level {question_level} to create the models.")

                    selected_questions = random.sample(question_type_list, question_count)
                    selected_questions_list.extend(selected_questions)

                shuffled_questions_list = selected_questions_list[:]
                random.shuffle(shuffled_questions_list)

                for question in shuffled_questions_list:
                    model_doc.append("question", {
                        "question": question.question,
                        "question_title": question.question_title,
                        "question_type": question.question_type,
                        "question_degree": question.question_degree,
                        "difficulty_degree": question.difficulty_degree,
                        "block_parent": question.block_parent
                    })

            frappe.msgprint(f"{message} {len(model_doc.question)} questions")
            model_doc.number_of_questions = len(model_doc.question)
            model_doc.save()
            frappe.db.commit()

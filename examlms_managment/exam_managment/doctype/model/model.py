import frappe
from frappe.model.document import Document
import random

class Model(Document):
    pass


@frappe.whitelist(allow_guest=True)
def Add_Model(create_exam_doc_name):
    # Get the specific Create Exam document
    create_exam_doc = frappe.get_doc('Create Exam', create_exam_doc_name)

    # Get the necessary details from the Create Exam document
    num_models = create_exam_doc.number_of_models
    random_question = create_exam_doc.random_question
    random_answer = create_exam_doc.random_answer

    type_setting_doc = frappe.get_doc('Type Setting', create_exam_doc.difficulty_level)
    exam_structure = type_setting_doc.exam_structure
    exam_structure2 = type_setting_doc.exam_structure2

    existing_models = frappe.get_all('Model', filters={'id_exam': create_exam_doc.name})

    all_selected_questions = set()  # Track all selected questions

    for index in range(num_models):
        if existing_models:
            # Update existing model
            existing_model = existing_models.pop(0)
            model_doc = frappe.get_doc('Model', existing_model.name)
            model_doc.set('question', [])  # Clear existing questions
            message = f"Model {index + 1} updated with"
        else:
            model_doc = frappe.new_doc("Model")
            message = f"Model {index + 1} created with"

        model_doc.collage = create_exam_doc.collage
        model_doc.doctor = create_exam_doc.doctor
        model_doc.department = create_exam_doc.department
        model_doc.level = create_exam_doc.level
        model_doc.course = create_exam_doc.course
        model_doc.id_exam = create_exam_doc.name
        model_doc.difficulty_level = create_exam_doc.difficulty_level
        model_doc.start_time = create_exam_doc.start_time
        model_doc.end_time = create_exam_doc.end_time
        model_doc.exam_duration = create_exam_doc.exam_duration

        

        model_questions_list = []  # Reset the question list for each model

        if random_question:
            if type_setting_doc.type == 'Number':
                for type_setting in exam_structure:
                    question_type = type_setting.type
                    question_level = type_setting.question_level
                    question_count = type_setting.number_of_question

                    # Create a set of available questions excluding the selected ones
                    available_questions = set(create_exam_doc.total_question_list) - all_selected_questions

                    # Filter available questions by type and level
                    question_type_list = [q for q in available_questions if q.question_type == question_type and q.difficulty_degree == question_level]

                    # if len(question_type_list) < question_count:
                    #     frappe.throw(f"Not enough unique questions of type {question_type} and level {question_level} to create the models.")

                    # Select questions randomly
                    selected_questions_for_model = random.sample(question_type_list, question_count)
                    model_questions_list.extend(selected_questions_for_model)

                    # Update the set of all questions used
                    all_selected_questions.update(selected_questions_for_model)

            else:  # Assuming type_setting_doc.type == 'Percentage'
                for type_setting in exam_structure2:
                    question_type = type_setting.type
                    question_level = type_setting.question_level
                    question_percentage = type_setting.percentage

                    question_count = int(len(exam_structure2) * question_percentage / 100)

                    # Create a set of available questions excluding the selected ones
                    available_questions = set(create_exam_doc.total_question_list) - all_selected_questions

                    # Filter available questions by type and level
                    question_type_list = [q for q in available_questions if q.question_type == question_type and q.difficulty_degree == question_level]

                    # if len(question_type_list) < question_count:
                    #     frappe.throw(f"Not enough unique questions of type {question_type} and level {question_level} to create the models.")

                    # Select questions randomly
                    selected_questions_for_model = random.sample(question_type_list, question_count)
                    model_questions_list.extend(selected_questions_for_model)

                    # Update the set of all questions used
                    all_selected_questions.update(selected_questions_for_model)

        else:  # If not random_question
                    if type_setting_doc.type == 'Number':
                        for type_setting in exam_structure:
                            question_type = type_setting.type
                            question_level = type_setting.question_level
                            question_count = type_setting.number_of_question

                            question_type_list = [q for q in create_exam_doc.total_question_list if q.question_type == question_type and q.difficulty_degree == question_level]

                            if len(question_type_list) < question_count:
                                frappe.throw(f"Not enough questions of type {question_type} and level {question_level} to create the models.")

                            selected_questions_for_model = question_type_list[:question_count]
                            model_questions_list.extend(selected_questions_for_model)

                    else:  # Assuming type_setting_doc.type == 'Percentage'
                        total_percentage = sum([structure.percentage for structure in exam_structure2])
                        if total_percentage != 100:
                            frappe.throw("The total percentage must be 100")

                        for type_setting in exam_structure2:
                            question_type = type_setting.type
                            question_level = type_setting.question_level
                            question_percentage = type_setting.percentage

                            question_count = int(len(exam_structure2) * question_percentage / 100)
                            question_type_list = [q for q in create_exam_doc.total_question_list if q.question_type == question_type and q.difficulty_degree == question_level]

                            if len(question_type_list) < question_count:
                                frappe.throw(f"Not enough questions of type {question_type} and level {question_level} to create the models.")

                            selected_questions_for_model = question_type_list[:question_count]
                            model_questions_list.extend(selected_questions_for_model)

        # Ensure each model gets the exact number of questions specified
        if len(model_questions_list) > sum([ts.number_of_question for ts in exam_structure]):
            model_questions_list = model_questions_list[:sum([ts.number_of_question for ts in exam_structure])]

        random.shuffle(model_questions_list)

        # Print selected questions for each model
        frappe.log(f"Model {index + 1} questions:")
        for question in model_questions_list:
            frappe.log(question.question)

        for question in model_questions_list:
            # Shuffle answer options if random_answer is checked
            if random_answer:
                options = [question.option_1, question.option_2, question.option_3, question.option_4]
                random.shuffle(options)
                question.option_1, question.option_2, question.option_3, question.option_4 = options
                
            model_doc.append("question", {
                "question": question.question,
                "question_title": question.question_title,
                "question_type": question.question_type,
                "question_mark": question.question_mark,
                "difficulty_degree": question.difficulty_degree,
                "block_parent": question.block_parent,
                "option_1" : question.option_1 ,
                "option_2" : question.option_2 ,
                "option_3" : question.option_3 ,
                "option_4" : question.option_4 ,
            })

        frappe.msgprint(f"{message} {len(model_doc.question)} questions")
        model_doc.number_of_questions = len(model_doc.question)
        model_doc.save()
        frappe.db.commit()




@frappe.whitelist()
def get_doctor_and_collage(id_exam):
    doc = frappe.get_doc("Model", id_exam)
    return {
        "doctor": doc.doctor,
        "collage": doc.collage,
        "questions": [{"question": q.question, "answers": [q.answer_1, q.answer_2, q.answer_3, q.answer_4]} for q in doc.questions]
    }
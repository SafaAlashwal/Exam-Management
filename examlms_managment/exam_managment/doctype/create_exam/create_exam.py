import frappe
from frappe.model.document import Document
import random

class CreateExam(Document):

        def validate(self):
            if not self.course:
                frappe.throw("Error: Please Enter the Course Name.")
            if self.number_of_questions > self.total_question:
                frappe.throw("Error: Number of Questions is larger than Total Questions")

        @frappe.whitelist()
        def fetch_question(self):
            course = self.course
            exam_type = self.difficulty_level
            total_questions = self.total_question
            num_models = self.number_of_models  # Assuming you have a field 'num_models' to store the number of models

            if exam_type:
                test_type_doc = frappe.get_doc('Type Setting', exam_type)
                if test_type_doc.type == 'Number':
                    questions = []
                    existing_questions = set()  # Set to store the names of the questions already fetched

                    # Collect questions of each type
                    questions_by_type = {}
                    for structure in test_type_doc.exam_structure:
                        filters = {
                            'type': structure.type,
                            'custom_course': course,
                            'custom_difficulty_level': structure.question_level,
                            'custom_is_subquestion': 0
                        }
                        if self.chapter:
                            filters['custom_chapter'] = ['in', [d.name1 for d in self.chapter]]

                        question_names = frappe.get_list('LMS Question', filters=filters, fields=["name", "type", "question"])
                        questions_by_type[structure.type] = question_names

                    # Check if there are enough questions in the specified chapters if chapters are specified
                    if self.chapter:
                        total_available_questions = sum(len(qs) for qs in questions_by_type.values())
                        if total_available_questions < total_questions * num_models:
                            frappe.throw(f"There are not enough questions in the specified chapters, only {total_available_questions} questions available.")
                            self.set('total_question_list', [])
                            return

                    # Collect all questions for the entire course to check overall availability
                    total_course_questions = frappe.get_list('LMS Question', filters={'custom_course': course}, fields=["name"])
                    if len(total_course_questions) < total_questions * num_models:
                        frappe.throw(f"There are not enough questions in the course, only {len(total_course_questions)} questions available.")
                        self.set('total_question_list', [])
                        return

                    # If chapters are not specified, collect questions from all chapters in the course
                    if not self.chapter:
                        questions_by_type = {}
                        for structure in test_type_doc.exam_structure:
                            filters = {
                                'type': structure.type,
                                'custom_course': course,
                                'custom_difficulty_level': structure.question_level,
                                'custom_is_subquestion': 0
                            }
                            question_names = frappe.get_list('LMS Question', filters=filters, fields=["name", "type", "question"])
                            questions_by_type[structure.type] = question_names

                    # Shuffle the questions within each type
                    for question_type, question_names in questions_by_type.items():
                        random.shuffle(question_names)
                        questions_by_type[question_type] = question_names

                    # Select questions from each type in a random order
                    total_questions_selected = 0
                    while total_questions_selected < total_questions * num_models:
                        all_types_exhausted = True
                        for structure in test_type_doc.exam_structure:
                            question_names = questions_by_type.get(structure.type, [])
                            if question_names:
                                question = None
                                for q in question_names:
                                    if q["name"] not in existing_questions:
                                        question = q
                                        existing_questions.add(q["name"])
                                        break

                                if question:
                                    all_types_exhausted = False
                                    if structure.type == "Block":
                                        # Get the number of sub-questions in the block
                                        block_question_doc = frappe.get_doc('LMS Question', question["name"])
                                        num_sub_questions = len(block_question_doc.custom_question_block)
                                        if total_questions_selected + num_sub_questions <= total_questions * num_models:
                                            questions.append(question)
                                            total_questions_selected += num_sub_questions
                                    else:
                                        questions.append(question)
                                        total_questions_selected += 1

                                    if total_questions_selected >= total_questions * num_models:
                                        break

                            if all_types_exhausted:
                                break

                    # Check if enough questions were selected
                    if total_questions_selected < total_questions * num_models:
                        frappe.throw(f"There are not enough questions, only {total_questions_selected} questions available.")
                        self.set('total_question_list', [])
                    else:
                        self.set('total_question_list', [])
                        for question in questions:
                            question_doc = frappe.get_doc('LMS Question', question["name"])
                            if question_doc.type == "Block":
                                # Get the child questions for Block type question
                                block_question = frappe.get_doc('LMS Question', question_doc.name)
                                for sub_question in block_question.custom_question_block:
                                    sub_question_doc = frappe.get_doc('LMS Question', sub_question.question)
                                    self.append("total_question_list", {
                                        "question": sub_question_doc.name,
                                        "question_title": sub_question_doc.question,
                                        "question_type": sub_question_doc.type,
                                        "question_degree": sub_question_doc.custom_degree_question,
                                        "difficulty_degree": sub_question_doc.custom_difficulty_level,
                                        "block_parent": question_doc.name
                                    })
                            else:
                                self.append("total_question_list", {
                                    "question": question_doc.name,
                                    "question_title": question_doc.question,
                                    "question_type": question_doc.type,
                                    "question_degree": question_doc.custom_degree_question,
                                    "difficulty_degree": question_doc.custom_difficulty_level,
                                })
            else:
                # Handle other exam types
                pass


                
        @frappe.whitelist()
        def get_filtered_course(self, doctor):
            doctor_doc = frappe.get_doc("Doctor", doctor)
            courses = [course.course for course in doctor_doc.courses]
            # frappe.msgprint("Courses for Doctor '{0}': {1}".format(doctor, ", ".join(courses)))
            return {"courses": courses}



        @frappe.whitelist()
        def get_filtered_level(self, department):
            department_doc = frappe.get_doc("Department", department)
            levels = [level.level for level in department_doc.levels]
            # frappe.msgprint("Courses for Doctor '{0}': {1}".format(doctor, ", ".join(courses)))
            return {"levels": levels}

        @frappe.whitelist()
        def get_number_question_list(self, difficulty_level):
            doc = frappe.get_doc("Type Setting", difficulty_level)
            total_questions = 0
            for row in doc.exam_structure:
                if row.type == "Block":
                    block_questions = frappe.get_all("LMS Question", filters={
                        "type": "Block",
                        "custom_difficulty_level": row.question_level
                    })
                    for block_question in block_questions:
                        block_question_doc = frappe.get_doc("LMS Question", block_question.name)
                        total_questions += len(block_question_doc.custom_question_block)
                else:
                    total_questions += row.number_of_question

            question_details = {
                "total_question": total_questions,
                "number_of_questions": total_questions
            }
            return question_details

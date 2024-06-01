import frappe
from frappe.model.document import Document
import random

class CreateExam(Document):

        def validate(self):
            if not self.course:
                frappe.throw("Error: Please Enter the Course Name.")
            # if self.number_of_questions > self.total_question:
            #     frappe.throw("Error: Number of Questions is larger than Total Questions")

        @frappe.whitelist()

        def fetch_question(self):
            course = self.course
            exam_type = self.difficulty_level
            number_of_models = self.number_of_models
            random_question = self.random_question

            if random_question:
                total_questions = self.total_question * number_of_models
            else:
                total_questions = self.total_question

            if exam_type:
                test_type_doc = frappe.get_doc('Type Setting', exam_type)
                if test_type_doc.type == 'Number':
                    questions = []
                    existing_questions = set()  # Set to store the names of the questions already fetched
                    total_questions_selected = 0

                    questions_by_structure = {}
                    all_question_names = []

                    # Iterate through each row in exam_structure to fetch all potential questions
                    for structure in test_type_doc.exam_structure:
                        question_type = structure.type
                        question_level = structure.question_level

                        filters = {
                            'type': question_type,
                            'custom_course': course,
                            'custom_difficulty_level': question_level,
                            'custom_is_subquestion': 0
                        }
                        if self.chapter:
                            filters['custom_chapter'] = ['in', [d.name1 for d in self.chapter]]

                        question_names = frappe.get_list('LMS Question', filters=filters, fields=["name", "type", "question"])
                        questions_by_structure.setdefault(question_type, []).append((structure, question_names))
                        all_question_names.extend(question_names)

                    # Calculate the number of available questions including subquestions in blocks
                    num_questions = 0
                    for question in all_question_names:
                        if question["type"] == "Block":
                            block_question_doc = frappe.get_doc('LMS Question', question["name"])
                            num_questions += len(block_question_doc.custom_question_block)
                        else:
                            num_questions += 1

                    # Check if the available questions are less than the required questions
                    if num_questions < total_questions:
                        if self.chapter:
                            chapter_names = [d.name1 for d in self.chapter]
                            frappe.throw(f"Only {num_questions} questions are available for the selected course '{course}' and chapters '{', '.join(chapter_names)}' out of the required {total_questions}.")
                        else:
                            frappe.throw(f"Only {num_questions} questions are available for the selected course '{course}' out of the required {total_questions}.")
                        return

                    # Shuffle questions within each structure
                    for question_type, structure_question_names in questions_by_structure.items():
                        for structure, question_names in structure_question_names:
                            random.shuffle(question_names)

                    # Function to add question to the list and update counts
                    def add_question(question):
                        nonlocal total_questions_selected
                        q_type = question["type"]
                        if q_type == "Block":
                            block_question_doc = frappe.get_doc('LMS Question', question["name"])
                            num_subquestions = len(block_question_doc.custom_question_block)
                            if total_questions_selected + num_subquestions <= total_questions:
                                questions.append(question)
                                existing_questions.add(question["name"])
                                total_questions_selected += num_subquestions
                        else:
                            questions.append(question)
                            existing_questions.add(question["name"])
                            total_questions_selected += 1

                    # Select questions based on the ratio of each type
                    while total_questions_selected < total_questions:
                        for question_type, structure_question_names in sorted(questions_by_structure.items()):
                            if total_questions_selected >= total_questions:
                                break

                            for structure, question_names in structure_question_names:
                                if not question_names:
                                    continue

                                question = question_names.pop(0)
                                if question["name"] not in existing_questions:
                                    add_question(question)

                    # Shuffle the final list of questions
                    random.shuffle(questions)
                    self.set('total_question_list', [])
                    for question in questions:
                        question_doc = frappe.get_doc('LMS Question', question["name"])
                        if question_doc.type == "Block":
                            # Get the child questions for Block type question
                            block_question = frappe.get_doc('LMS Question', question_doc.name)
                            sub_questions = block_question.custom_question_block[:]  # Create a copy of the list
                            random.shuffle(sub_questions)  # Shuffle the sub-questions
                            for sub_question in sub_questions:
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

        def fetch_additional_questions(self, course, question_level, remaining_questions, existing_questions):
            additional_questions = []
            filters = {
                'custom_course': course,
                'custom_difficulty_level': question_level,
                'custom_is_subquestion': 0
            }
            # استخدمي مجموعة من مرشحات إضافية إذا كان ذلك ضروريًا لاسترداد الأسئلة الإضافية بشكل صحيح

            # الآن استرداد الأسئلة الإضافية
            additional_question_names = frappe.get_list('LMS Question', filters=filters, fields=["name", "type", "question"])

            for question in additional_question_names:
                # التحقق مما إذا كانت السؤال قد تم استخدامه بالفعل
                if question["name"] not in existing_questions:
                    additional_questions.append(question)
                    existing_questions.add(question["name"])
                    # تحقق من أن العدد الإجمالي للأسئلة المختارة لا يتجاوز العدد المطلوب
                    if len(additional_questions) >= remaining_questions:
                        break

            return additional_questions

    # You may need to adjust the filters

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

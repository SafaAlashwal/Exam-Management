import frappe
from frappe.model.document import Document
import random

class CreateExam(Document):
        def validate(self):
                if not self.course:
                    frappe.throw("Error: Please Enter the Course Name.")
                if not self.doctor:
                    self.doctor = frappe.session.user

                
                # Call the validate_question_marks method here
                # self.validate_question_marks()
        
        @frappe.whitelist()
        def validate_question_marks(self):
            question_marks = {}
            question_indices = {}
            for idx, question in enumerate(self.total_question_list, start=1):
                key = (question.question_type, question.difficulty_degree)
                if key in question_marks:
                    if question_marks[key] != question.question_mark:
                        first_question_index = question_indices[key]
                        frappe.throw(f"Error: All questions of type {question.question_type} and difficulty level {question.difficulty_degree} must have the same marks. First question with this type and difficulty: {first_question_index}, Question number with different mark: {idx}")
                else:
                    question_marks[key] = question.question_mark
                    question_indices[key] = idx


        @frappe.whitelist()
        def fetch_question(self):
            course = self.course
            exam_type = self.difficulty_level
            number_of_models = self.number_of_models
            random_question = self.random_question
            random_answer = self.random_answer
            test_type_doc = frappe.get_doc('Type Setting', exam_type)

            if random_question:
                total_questions = 0
                for structure in test_type_doc.exam_structure:
                    total_questions += structure.number_of_question * number_of_models
            else:
                total_questions = self.total_question

            if exam_type:
                questions = []
                existing_questions = set()  # Set to store the names of the questions already fetched
                total_questions_selected = 0

                if test_type_doc.type == 'Number':
                    questions_by_structure = {}
                    all_question_names = []

                    # Iterate through each row in exam_structure to fetch all potential questions
                    for structure in test_type_doc.exam_structure:
                        question_type = structure.type
                        question_level = structure.question_level
                        question_count = structure.number_of_question  # Number of questions required for this structure

                        filters = {
                            'type': question_type,
                            'custom_course': course,
                            'custom_difficulty_level': question_level,
                        }
                        if self.chapter:
                            filters['custom_chapter'] = ['in', [d.name1 for d in self.chapter]]

                        question_names = frappe.get_list('Question', filters=filters, fields=["name", "type", "question"])
                        questions_by_structure.setdefault(question_type, []).append((structure, question_names))
                        all_question_names.extend(question_names)

                    # Calculate the number of available questions
                    num_questions = len(all_question_names)

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
                        if total_questions_selected < total_questions:
                            questions.append(question)
                            existing_questions.add(question["name"])
                            total_questions_selected += 1

                    # Select questions based on the ratio of each type
                    while total_questions_selected < total_questions:
                        for question_type, structure_question_names in sorted(questions_by_structure.items()):
                            for structure, question_names in structure_question_names:
                                required_count = structure.number_of_question
                                selected_count = 0

                                while selected_count < required_count and question_names:
                                    question = question_names.pop(0)
                                    if question["name"] not in existing_questions:
                                        add_question(question)
                                        selected_count += 1
                                        if total_questions_selected >= total_questions:
                                            break

                                # If we need more questions than are provided by one complete pass of the exam_structure, continue
                                if total_questions_selected < total_questions:
                                    # Reinitialize question names for another pass
                                    for question_type, structure_question_names in questions_by_structure.items():
                                        for structure, question_names in structure_question_names:
                                            filters = {
                                                'type': question_type,
                                                'custom_course': course,
                                                'custom_difficulty_level': structure.question_level,
                                            }
                                            if self.chapter:
                                                filters['custom_chapter'] = ['in', [d.name1 for d in self.chapter]]

                                            question_names.extend(frappe.get_list('Question', filters=filters, fields=["name", "type", "question"]))
                                            random.shuffle(question_names)

                    # Ensure balanced distribution if more questions are needed
                    remaining_questions = total_questions - total_questions_selected
                    if remaining_questions > 0:
                        num_passes = (remaining_questions // len(test_type_doc.exam_structure)) + 1
                        for _ in range(num_passes):
                            if total_questions_selected >= total_questions:
                                break
                            for question_type, structure_question_names in sorted(questions_by_structure.items()):
                                for structure, question_names in structure_question_names:
                                    required_count = structure.number_of_question
                                    selected_count = 0

                                    while selected_count < required_count and question_names:
                                        question = question_names.pop(0)
                                        if question["name"] not in existing_questions:
                                            add_question(question)
                                            selected_count += 1
                                            if total_questions_selected >= total_questions:
                                                break

                else:
                    questions_by_structure = {}
                    all_question_names = []

                    total_percentage = sum([structure.percentage for structure in test_type_doc.exam_structure2])
                    # Check if the total percentage is 100
                    if total_percentage != 100:
                        frappe.throw("The total percentage must be 100")

                    # Iterate through each row in exam_structure2 to fetch all potential questions
                    for structure in test_type_doc.exam_structure2:
                        question_type = structure.type
                        question_level = structure.question_level
                        question_percentage = structure.percentage / 100.0  # Convert percentage to decimal
                        question_count = int(total_questions * question_percentage)  # Calculate number of questions based on percentage

                        filters = {
                            'type': question_type,
                            'custom_course': course,
                            'custom_difficulty_level': question_level,
                        }
                        if self.chapter:
                            filters['custom_chapter'] = ['in', [d.name1 for d in self.chapter]]

                        question_names = frappe.get_list('Question', filters=filters, fields=["*"])
                        questions_by_structure.setdefault(question_type, []).append((structure, question_names, question_count))
                        all_question_names.extend(question_names)

                    # Calculate the number of available questions
                    num_questions = len(all_question_names)

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
                        for structure, question_names, _ in structure_question_names:
                            random.shuffle(question_names)

                    # Function to add question to the list and update counts
                    def add_question(question):
                        nonlocal total_questions_selected
                        if total_questions_selected < total_questions:
                            questions.append(question)
                            existing_questions.add(question["name"])
                            total_questions_selected += 1

                    # Select questions based on the ratio of each type
                    while total_questions_selected < total_questions:
                        for question_type, structure_question_names in sorted(questions_by_structure.items()):
                            for structure, question_names, required_count in structure_question_names:
                                selected_count = 0

                                while selected_count < required_count and question_names:
                                    question = question_names.pop(0)
                                    if question["name"] not in existing_questions:
                                        add_question(question)
                                        selected_count += 1
                                        if total_questions_selected >= total_questions:
                                            break

                                # If we need more questions than are provided by one complete pass of the exam_structure2, continue
                                if total_questions_selected < total_questions:
                                    # Reinitialize question names for another pass
                                    for question_type, structure_question_names in questions_by_structure.items():
                                        for structure, question_names, _ in structure_question_names:
                                            filters = {
                                                'type': question_type,
                                                'custom_course': course,
                                                'custom_difficulty_level': structure.question_level,
                                            }
                                            if self.chapter:
                                                filters['custom_chapter'] = ['in', [d.name1 for d in self.chapter]]

                                            question_names.extend(frappe.get_list('Question', filters=filters, fields=["name", "type", "question"]))
                                            random.shuffle(question_names)

                # Shuffle the final list of questions
                random.shuffle(questions)
                self.set('total_question_list', [])
                for question in questions:
                    question_doc = frappe.get_doc('Question', question["name"])

                    question_blocks = frappe.get_all("Question Block", filters={"question": question_doc.name})

                    # إذا كانت هناك 'Question Block' واحدة على الأقل، افترض أنها تحتوي على والد
                    if question_blocks:
                        parent_question_block = frappe.get_doc("Question Block", question_doc.name)
                        if parent_question_block:
                            parent_question_title = parent_question_block.parent
                            question_doc2 = frappe.get_doc('Question', parent_question_title)

                            self.append("total_question_list", {
                                "question": question_doc.name,
                                "question_title": question_doc.question,
                                "question_type": question_doc.type,
                                "question_mark": question_doc.custom_question_mark,
                                "difficulty_degree": question_doc.custom_difficulty_level,
                                "block_parent": question_doc2.question,
                                "option_1" : question_doc.option_1 ,
                                "option_2" : question_doc.option_2 ,
                                "option_3" : question_doc.option_3 ,
                                "option_4" : question_doc.option_4 ,

                            })
                    else:
                            self.append("total_question_list", {
                            "question": question_doc.name,
                            "question_title": question_doc.question,
                            "question_type": question_doc.type,
                            "question_mark": question_doc.custom_question_mark,
                            "difficulty_degree": question_doc.custom_difficulty_level,
                            "option_1" : question_doc.option_1 ,
                            "option_2" : question_doc.option_2 ,
                            "option_3" : question_doc.option_3 ,
                            "option_4" : question_doc.option_4 ,
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
            additional_question_names = frappe.get_list('Question', filters=filters, fields=["name", "type", "question"])

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
                    block_questions = frappe.get_all("Question", filters={
                        "type": "Block",
                        "custom_difficulty_level": row.question_level
                    })
                    for block_question in block_questions:
                        block_question_doc = frappe.get_doc("Question", block_question.name)
                        total_questions += len(block_question_doc.custom_question_block)
                else:
                    total_questions += row.number_of_question

            question_details = {
                "total_question": total_questions,
                "number_of_questions": total_questions
            }
            return question_details

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

		if exam_type:
			test_type_doc = frappe.get_doc('Type Setting', exam_type)
			if test_type_doc.type == 'Number':
				questions = []
				existing_questions = set()  # مجموعة لتخزين الأسئلة المجلبة مسبقاً
				sub_questions_added = set()  # مجموعة لتخزين الأسئلة الفرعية المضافة من داخل Block

				# Collect questions of each type
				questions_by_type = {}
				for structure in test_type_doc.exam_structure:
					filters = {
						'type': structure.type,
						'custom_course': course,
						'custom_difficulty_level': structure.question_level,
					}
					if self.chapter:
						filters['custom_chapter'] = ['in', [d.name1 for d in self.chapter]]

					question_names = frappe.get_list('LMS Question', filters=filters, fields=["name", "type", "question"])
					questions_by_type[structure.type] = question_names

				# Shuffle the questions within each type
				for question_type, question_names in questions_by_type.items():
					random.shuffle(question_names)
					questions_by_type[question_type] = question_names

				# Check if there are enough questions
				total_available_questions = sum(len(questions) for questions in questions_by_type.values())
				required_questions = sum([structure.number_of_question for structure in test_type_doc.exam_structure])
				if total_available_questions < required_questions:
					if self.chapter:
						frappe.throw(f"A total of {total_available_questions} questions were found out of {total_questions} required for the selected chapters.")
					else:
						frappe.throw(f"A total of {total_available_questions} questions were found out of {total_questions} required for the selected course.")

				# Select questions from each type in a random order
				total_questions_selected = 0
				while total_questions_selected < total_questions:
					for structure in test_type_doc.exam_structure:
						question_names = questions_by_type.get(structure.type, [])
						if question_names:
							question = None
							if structure.type == "Block":
								# If the question type is Block, process it first
								for block_question in question_names:
									if block_question["name"] not in existing_questions:
										question = block_question
										existing_questions.add(block_question["name"])
										break
							else:
								# If the question type is not Block, process as usual
								for q in question_names:
									if q["name"] not in existing_questions and q["name"] not in sub_questions_added:
										question = q
										existing_questions.add(q["name"])
										break

							if question:
								if structure.type == "Block":
									# Get the number of sub-questions in the block
									block_question_doc = frappe.get_doc('LMS Question', question["name"])
									num_sub_questions = len(block_question_doc.custom_question_block)
									if total_questions_selected + num_sub_questions <= total_questions:
										questions.append(question)
										total_questions_selected += num_sub_questions
										# Add sub-questions to the set of added questions to avoid duplicates
										for sub_question in block_question_doc.custom_question_block:
											sub_questions_added.add(sub_question.question)
								else:
									questions.append(question)
									total_questions_selected += 1

								if total_questions_selected >= total_questions:
									break

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
				total_questions += len(block_questions)
			else:
				total_questions += row.number_of_question
		
		question_details = {
			"total_question": total_questions,
			"number_of_questions": total_questions
		}
		return question_details
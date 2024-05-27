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
		number_models = self.number_of_models
		total_questions = self.total_question


		if exam_type:
			test_type_doc = frappe.get_doc('Type Setting', exam_type)
			if test_type_doc.type == 'Number':
				questions = []
				total_questions_selected = 0

				if self.random_question:

					for structure in test_type_doc.exam_structure:
						filters = {
							'type': structure.type,
							'custom_course': course,
							'custom_difficulty_level': structure.question_level,
						}
						if self.chapter:
							filters['custom_chapter'] = ['in', [d.name1 for d in self.chapter]]

						question_names = frappe.get_list('LMS Question', filters=filters, fields=["name"])
						question_names = [q.name for q in question_names]
						if question_names:
							selected_questions = random.sample(question_names, min(structure.number_of_question * number_models, len(question_names)))
							# else:
							# 	selected_questions = question_names[:min(structure.number_of_question, len(question_names))]
							questions.extend(selected_questions)
							total_questions_selected += len(selected_questions)

				elif not self.random_question:
					while len(questions) < total_questions:
						for structure in test_type_doc.exam_structure:
							filters = {
								'type': structure.type,
								'custom_course': course,
								'custom_difficulty_level': structure.question_level,
							}
							if self.chapter:
								filters['custom_chapter'] = ['in', [d.name1 for d in self.chapter]]

							question_names = frappe.get_list('LMS Question', filters=filters, fields=["name"], order_by="RAND()", limit=structure.number_of_question)
							questions.extend([q.name for q in question_names])
							total_questions_selected += len(question_names)

							if len(questions) >= total_questions:
								break
				required_questions = sum([structure.number_of_question * number_models for structure in test_type_doc.exam_structure])
				if self.random_question and total_questions_selected < required_questions:
					remaining_questions = required_questions - total_questions_selected
					if self.chapter:
						frappe.throw(f"A total of {total_questions_selected} questions were selected out of {required_questions} required. There are {remaining_questions} remaining questions and no questions available for the selected chapters.")
					else:
						frappe.throw(f"A total of {total_questions_selected} questions were selected out of {required_questions} required. There are {remaining_questions} remaining questions and no questions available for the selected course.")
				elif not self.random_question and total_questions_selected < sum([structure.number_of_question for structure in test_type_doc.exam_structure]):
					remaining_questions = sum([structure.number_of_question for structure in test_type_doc.exam_structure]) - total_questions_selected
					if self.chapter:
						frappe.throw(f"A total of {total_questions_selected} questions were selected out of {sum([structure.number_of_question for structure in test_type_doc.exam_structure])} required. There are {remaining_questions} remaining questions and no questions available for the selected chapters.")
					else:
						frappe.throw(f"A total of {total_questions_selected} questions were selected out of {sum([structure.number_of_question for structure in test_type_doc.exam_structure])} required. There are {remaining_questions} remaining questions and no questions available for the selected course.")
				else:
					self.set('total_question_list', [])
					for question in questions:
						question_doc = frappe.get_doc('LMS Question', question)
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
	# def fetch_question(self):
	# 	course = self.course
	# 	exam_type = self.difficulty_level
	# 	number_models = self.number_of_models
	# 	total_questions = self.total_question

		
		# if exam_type:
		# 	test_type_doc = frappe.get_doc('Type Setting', exam_type)
		# 	if test_type_doc.type == 'Number':
		# 		questions = []
		# 		total_questions_selected = 0

		# 		while len(questions) < total_questions:
		# 			for structure in test_type_doc.exam_structure:
		# 				filters = {
		# 					'type': structure.type,
		# 					'custom_course': course,
		# 					'custom_difficulty_level': structure.question_level,
		# 				}
		# 				if self.chapter:
		# 					filters['custom_chapter'] = ['in', [d.name1 for d in self.chapter]]

		# 				if self.random_question:
		# 					question_names = frappe.get_list('LMS Question', filters=filters, fields=["name"], order_by="RAND()")
		# 					question_names = [q.name for q in question_names]
		# 					selected_questions = question_names[:min(structure.number_of_question * number_models, len(question_names))]
		# 				else:
		# 					question_names = frappe.get_list('LMS Question', filters=filters, fields=["name"])
		# 					question_names = [q.name for q in question_names]
		# 					selected_questions = question_names[:min(structure.number_of_question, len(question_names))]

		# 				questions.extend(selected_questions)
		# 				total_questions_selected += len(selected_questions)

		# 				if len(questions) >= total_questions:
		# 					break

		# 		if total_questions_selected < total_questions:
		# 			remaining_questions = total_questions - total_questions_selected
		# 			if self.chapter:
		# 				frappe.throw(f"A total of {total_questions_selected} questions were selected out of {total_questions} required. There are {remaining_questions} remaining questions and no questions available for the selected chapters.")
		# 			else:
		# 				frappe.throw(f"A total of {total_questions_selected} questions were selected out of {total_questions} required. There are {remaining_questions} remaining questions and no questions available for the selected course.")
		# 		else:
		# 			self.set('total_question_list', [])
		# 			for question in questions[:total_questions]:
		# 				question_doc = frappe.get_doc('LMS Question', question)
		# 				self.append("total_question_list", {
		# 					"question": question_doc.name,
		# 					"question_title": question_doc.question,
		# 					"question_type": question_doc.type,
		# 					"question_degree": question_doc.custom_degree_question,
		# 					"difficulty_degree": question_doc.custom_difficulty_level,
		# 				})
		# else:
		# 	# Handle other exam types
		# 	pass
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
		total_questions = sum(row.number_of_question for row in doc.exam_structure)
			
		question_details = {
			"total_question": total_questions,
			"number_of_questions": total_questions
		}
		return question_details




# Copyright (c) 2024, Safa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TypeSetting(Document):
		@frappe.whitelist()
		def get_questions(self):

			questions = []
			for structure in self.exam_structure:
				questions += frappe.get_list('Question', filters={
					'type': structure.type,
					'custom_difficulty_level': structure.question_level
				}, fields=["question"], limit_page_length=structure.number_of_question)
			# frappe.msgprint(len(questions))
			return questions
		

		@frappe.whitelist()
		def get_questions2(self):
			# frappe.msgprint("fff")
			questions = []
			total_questions = self.number_of_questions
			total_percentage = sum([structure.percentage for structure in self.exam_structure2])

			# Check if the total percentage is 100
			if total_percentage != 100:
				frappe.throw(("The total percentage must be 100"))

			for structure in self.exam_structure2:
				# Calculate the number of questions for this structure based on the ratio
				num_questions = total_questions * structure.percentage / 100
		
				questions += frappe.get_list('Question', filters={
					'type': structure.type,
					'custom_difficulty_level': structure.question_level
				}, fields=["question"], limit_page_length=num_questions)
			# frappe.msgprint(str(questions))
			return questions


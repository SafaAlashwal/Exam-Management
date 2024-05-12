import frappe
from frappe.model.document import Document
import random

class CreateExam(Document):
			def validate(self):
				if self.number_of_questions > self.total_question:
					frappe.throw("Error: Number of Questions is larger than Total Questions")

			@frappe.whitelist()
			def fetch_question(self):
				all_chapter = [d.name1 for d in self.chapter]

				if not all_chapter:
						all_questions = frappe.get_list('LMS Question', pluck='name')

				else:
					all_questions = []
					for chapter in all_chapter:
						questions = frappe.get_list('LMS Question', filters={'custom_chapter': chapter}, pluck='name')
						all_questions.extend(questions)

				num_questions = self.total_question
				num_questions = min(num_questions, len(all_questions))
				num_questions = max(num_questions, 0) 

				questions = random.sample(all_questions, num_questions)

				# Clear existing questions
				self.set('total_question_list', [])  # Clear existing child table entries

				for question in questions:
					question_doc = frappe.get_doc('LMS Question', question)
					question_name = question_doc.name
					question_title = question_doc.question
					question_type = question_doc.type
					question_degree = question_doc.custom_degree_question
					difficulty_degree = question_doc.custom_difficulty_degree


					self.append("total_question_list", {
						"question": question_name,
						"question_title": question_title,
						"question_type": question_type,
						"question_degree" : question_degree,
						"difficulty_degree" : difficulty_degree,
					})

				# Save the document
				# self.save()
				# self.reload()

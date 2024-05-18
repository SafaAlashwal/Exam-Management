import frappe
from frappe.model.document import Document
import random

class CreateExam(Document):
			def validate(self):
				# if not self.total_question:
				# 	frappe.throw("Error: Please enter the total number of questions.")
				if self.number_of_questions > self.total_question:
					frappe.throw("Error: Number of Questions is larger than Total Questions")


			@frappe.whitelist()
			def fetch_question(self):
				all_chapter = [d.name1 for d in self.chapter]
				course = self.course

				if not all_chapter:
					if course:
						all_questions = frappe.get_list('LMS Question', filters={'custom_course': course}, pluck='name')
					else:
						all_questions = frappe.get_list('LMS Question', pluck='name')
				else:
					all_questions = []
					for chapter in all_chapter:
						if course:
							questions = frappe.get_list('LMS Question', filters={'custom_chapter': chapter, 'custom_course': course}, pluck='name')
						else:
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
						"question_degree": question_degree,
						"difficulty_degree": difficulty_degree,
					})



			
				# Save the document
				# self.save()
				# self.reload()



			@frappe.whitelist()
			def get_filtered_chapters(self, doctor):
				doctor_doc = frappe.get_doc("Doctor", doctor)
				courses = [course.course for course in doctor_doc.courses]
				# frappe.msgprint("Courses for Doctor '{0}': {1}".format(doctor, ", ".join(courses)))
				return {"courses": courses}
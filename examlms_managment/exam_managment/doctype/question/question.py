# Copyright (c) 2024, Safa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
# from lms.lms.utils import has_course_instructor_role, has_course_moderator_role


class Question(Document):
	def validate(self):
		validate_correct_answers(self)
		validate_possible_block(self)


@frappe.whitelist()
def get_filtered_course(doctor):
	doctor_doc = frappe.get_doc("Doctor", doctor)
	courses = [course.course for course in doctor_doc.courses]
	return {"courses": courses}


def validate_correct_answers(question):
	if question.type == "Choices":
		validate_duplicate_options(question)
		validate_correct_options(question)
	elif question.type == "User Input":
		validate_possible_answer(question)
	# elif question.type == "Block":
	# 	validate_possible_block(question)

def validate_duplicate_options(question):
	options = []

	for num in range(1, 5):
		if question.get(f"option_{num}"):
			options.append(question.get(f"option_{num}"))

	if len(set(options)) != len(options):
		frappe.throw(_("Duplicate options found for this question."))


def validate_correct_options(question):
	correct_options = get_correct_options(question)

	if len(correct_options) > 1:
		question.multiple = 1

	if not len(correct_options):
		frappe.throw(_("At least one option must be correct for this question."))


def validate_possible_answer(question):
	possible_answers = []
	possible_answers_fields = [
		"possibility_1",
		"possibility_2",
		"possibility_3",
		"possibility_4",
	]

	for field in possible_answers_fields:
		if question.get(field):
			possible_answers.append(field)

	if not len(possible_answers):
		frappe.throw(
			_("Add at least one possible answer for this question: {0}").format(
				frappe.bold(question.question)
			)
		)


def get_correct_options(question):
	correct_options = []
	correct_option_fields = [
		"is_correct_1",
		"is_correct_2",
		"is_correct_3",
		"is_correct_4",
	]
	for field in correct_option_fields:
		if question.get(field) == 1:
			correct_options.append(field)

	return correct_options



def update_subquestion_flag(lms_question):
    if lms_question.custom_is_subquestion == 0:
        frappe.set_value("Question", lms_question.name, "custom_is_subquestion", 1)
        frappe.log(f"Updated custom_is_subquestion flag for question: {lms_question.name}")

def validate_question_block(doc, method):
    try:
        frappe.log("Fetching all question blocks...")
        question_block_names = frappe.get_all("Question Block", pluck="name")
        frappe.log(f"Found {len(question_block_names)} question blocks")

        lms_questions = frappe.get_all("Question",
                                       filters={"name": ["in", question_block_names]},
                                       fields=["name", "custom_is_subquestion"])

        for lms_question in lms_questions:
            frappe.log(f"Question: {lms_question.name}, Question Type: {lms_question.custom_is_subquestion}")
            update_subquestion_flag(lms_question)

    except Exception as e:
        frappe.log(f"Error validating question block: {e}")


def validate_possible_block(question):
	# السؤال الخارجي
	# external_question = frappe.get_doc("LMS Question", "external_question_name")
	# external_question = frappe.get_doc("LMS Question")


	# قائمة لتخزين الأسئلة الداخلية
	internal_questions = []

	# الحصول على الأسئلة الداخلية
	for questions in question.custom_question_block:
		# frappe.msgprint(questions.question)
		if questions.question != "Block":
			internal_questions.append(questions)

	# طباعة الأسئلة الداخلية
	for questions in internal_questions:
		print(questions.name)


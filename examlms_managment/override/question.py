import frappe
from frappe import _

from lms.lms.doctype.lms_question.lms_question import LMSQuestion
from frappe.model.document import Document



class LMSQuestion(Document):
	def validate(self):
		validate_correct_answers(self)
		validate_possible_block(self)


# def validate_possible_block(question):
# 	questions = question.question
# 	for d in questions:
# 		frappe.msgprint(d)


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


def after_insert(doc,event):
    # print(f"\n\n\n{doc} , {event}")
		frappe.msgprint("Done")
		# properties = frappe.get_all("LMS Question", fields=["*"], filters={})   
		# s= properties['question']
		# frappe.msgprint(s)


# # استعلام للحصول على الأسئلة التي يكون نوعها Block
# block_questions = frappe.get_all("LMS Question", filters={"type": "Block"}, fields=["name"])

# # قائمة لتخزين الأسئلة الداخلية
# internal_questions = []

# # الحصول على الأسئلة الداخلية
# for question in block_questions:
#     child_questions = frappe.get_all("Question Block", filters={"parent": question.name}, fields=["name"])
#     internal_questions.extend(child_questions)

# # طباعة الأسئلة الداخلية
# for question in internal_questions:
#     print(question.name)

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
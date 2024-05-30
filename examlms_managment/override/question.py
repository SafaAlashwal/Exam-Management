import frappe
from frappe import _

from lms.lms.doctype.lms_question.lms_question import LMSQuestion
# from  import on_update, on_trash

from frappe.model.document import Document



class LMSQuestion(Document):
	def validate(self):
		validate_correct_answers(self)
		validate_possible_block(self)
		validate_question_block(self)



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
# Add a global flag to prevent recursive calls
is_updating_subquestions = False

def validate_question_block(question):
    global is_updating_subquestions
    
    if is_updating_subquestions:
        return

    if question.type != "Block":
        return

    try:
        is_updating_subquestions = True
        
        # Get the child questions from the Question Block
        child_questions = frappe.get_all("Question Block", 
                                        filters={"parent": question.name}, 
                                        fields=["question"])

        child_question_names = [child_question.question for child_question in child_questions]

        # Iterate through the child questions and update custom_is_subquestion
        for child_question in child_question_names:
            child_question_doc = frappe.get_doc("LMS Question", child_question)
            if child_question_doc.custom_is_subquestion != 1:
                child_question_doc.custom_is_subquestion = 1
                child_question_doc.save()

        # Mark other questions in the same block as not subquestions
        all_questions_in_block = frappe.get_all("LMS Question",
                                                filters={"name": ("!=", question.name)},
                                                fields=["name"])
        
        for other_question in all_questions_in_block:
            if other_question.name not in child_question_names:
                other_question_doc = frappe.get_doc("LMS Question", other_question.name)
                if other_question_doc.custom_is_subquestion != 0:
                    other_question_doc.custom_is_subquestion = 0
                    other_question_doc.save()

    finally:
        is_updating_subquestions = False

def on_update(doc, method):
    # Handle the update of subquestions when the main question is updated
    validate_question_block(doc)

def on_trash(doc, method):
    # Handle the deletion of the main question by marking subquestions as not subquestions
    if doc.type == "Block":
        child_questions = frappe.get_all("Question Block", 
                                         filters={"parent": doc.name}, 
                                         fields=["question"])
        
        for child_question in child_questions:
            child_question_doc = frappe.get_doc("LMS Question", child_question.question)
            child_question_doc.custom_is_subquestion = 0
            child_question_doc.save()

# # استعلام للحصول على الأسئلة التي يكون نوعها Block
		# block_questions = frappe.get_all("LMS Question", filters={"type": "Block"}, fields=["name"])

		# # قائمة لتخزين الأسئلة الداخلية
		# internal_questions = []

		# # الحصول على الأسئلة الداخلية
		# for question in block_questions:
		# 	child_questions = frappe.get_all("Question Block", filters={"parent": question.name}, fields=["name"])
		# 	internal_questions.extend(child_questions)

		# # طباعة الأسئلة الداخلية
		# for question in internal_questions:
		# 	frappe.msgprint(question.name)

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
import frappe
def get_context(context):
    context.title  = 'Hi'
    return context

@frappe.whitelist(allow_guest=True)
def get_prop():
    properties = frappe.get_all("LMS Question", fields=["*"], filters={})   
    return properties



# @frappe.whitelist(allow_guest=True)
# def send_doc():
    doc_data = frappe.request.get_json()

    frappe.set_value('Question', 'new_question', 'question', doc_data['question'])
    frappe.set_value('Question', 'new_question', 'option_1', doc_data['option_1'])
    frappe.set_value('Question', 'new_question', 'option_2', doc_data['option_2'])
    frappe.set_value('Question', 'new_question', 'option_3', doc_data['option_3'])

    return {'message': 'طھظ… ط¥ط±ط³ط§ظ„ ط§ظ„ط¨ظٹط§ظ†ط§طھ ط¨ظ†ط¬ط§ط­'}
# @frappe.whitelist(allow_guest=True)
# def send_answer():
#     doc = frappe.new_doc("Question")
#     doc.question = "question"
#     doc.insert(ignore_permissions=True)
#     doc.save()
#     return "Question created successfully"
# def get_answer():
# def get_prop():
#     properties = frappe.get_all("Question", fields=["question_degree", "question", "course"])
#     return properties
        # properties = frappe.db.sql(f"""SELECT question_degree, question, course from `tabQuestion`;""")
        # return properties





# def get_context(context):
#     question_list = frappe.get_doc("Exam Review","IT")
#     context.questions = question_list


#     questions_with_answers = []
#     for question_median in question_list.get("question"):
#                 question = frappe.get_doc("Question", question_median.question)
                                
#                 questions_with_answers.append({
#                                 "question": question.question,
#                                 # "answer_choices": question.answer_choices
#                                 })



#     context.view=questions_with_answers


#     return context

# @frappe.whitelist()
# def AddSelectedValue(selected_answers):

#     doc=frappe.new_doc("Exam Review")
#     doc.department="hh"
#     doc.insert()

#     return "Data saved successfully"
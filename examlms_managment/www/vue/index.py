from datetime import datetime
import frappe
import random

@frappe.whitelist(allow_guest=True)
def get_prop(student_id):
    now = datetime.now()
    student = frappe.get_doc("Student Record", student_id)
    
    # Fetch all available models for the specified student
    properties = frappe.get_all(
        "Model",
        filters=[
            ["start_time", "<=", now],
            ["end_time", ">=", now],
            ["collage", "=", student.collage],
            ["department", "=", student.department],
            ["level", "=", student.level]
        ],
        fields=["*"]
    )
    
    # Group the models by course
    course_groups = {}
    for prop in properties:
        course = prop.get("course")
        if course not in course_groups:
            course_groups[course] = []
        course_groups[course].append(prop)
    
    # Select one random model from each course group
    random_properties = []
    for course, props in course_groups.items():
        random_prop = random.choice(props)
        
        # Fetch the questions associated with the selected model
        questions = frappe.get_all(
            "Question Quiz",
            filters={"parent": random_prop["name"]},
            fields=["*"]
        )
        random_prop["question"] = questions
        random_properties.append(random_prop)
    
    return random_properties if random_properties else []



@frappe.whitelist(allow_guest=True)
def check_answer(question_id, student_answer): 
    question = frappe.get_doc("LMS Question", question_id)
    correct_answers = []

    # الحصول على نوع السؤال
    question_type = question.get("type")

    if question_type == "User Input":
        # التحقق من إمكانية الإجابة
        for i in range(1, 6):  # افترض أن هناك 5 احتمالات كحد أقصى
            possibility = question.get(f"possibility_{i}")
            if possibility:
                correct_answers.append(possibility)
    else:
        # التحقق من خيارات الإجابة
        for i in range(1, 6):  # افترض أن هناك 5 خيارات كحد أقصى
            option = question.get(f"option_{i}")
            is_correct_option = question.get(f"is_correct_{i}")
            if option and is_correct_option:
                correct_answers.append(option)

    is_correct = student_answer in correct_answers
    
    return {
        "is_correct": is_correct,
        "correct_answers": correct_answers
    }


@frappe.whitelist(allow_guest=True)
def send_answer(student_id , student_name, course, answers, appreciation , total_mark):
    # إنشاء سجل جديد من نوع "Student Answer"
    doc = frappe.new_doc("Student Answer")
    
    # تعبئة بيانات السجل
    doc.student_id = student_id
    doc.student_name = student_name
    doc.course = course
    doc.appreciation = appreciation
    doc.total_mark = total_mark
    
    # إضافة الأسئلة والأجوبة
    for answer in answers:
        doc.append("result", {
            "question": answer["question"],
            "students_response": answer["students_response"],
            "marks" : answer["marks"],
            "is_correct":answer["is_correct"]
        })
    doc.insert(ignore_permissions=True)
    doc.save()

    return "Question created successfully"



@frappe.whitelist(allow_guest=True)
def login_student(student_id, password):
    try:
        student = frappe.get_doc('Student Record', {'student_id': student_id})
        
        if not student:
            return {'success': False, 'message': 'Student ID not found', 'style': 'error-message'}
        
        stored_password = student.password
        
        if stored_password == password:
            student_data = student.as_dict()
            student_data['success'] = True  # أضف هذه السطر لضمان أن تحتوي البيانات على المفتاح success
            return student_data
        else:
            return {'success': False, 'message': 'Invalid password', 'style': 'error-message'}
    
    except Exception as e:
        return {'success': False, 'message': 'An error occurred: {0}'.format(str(e)), 'style': 'error-message'}

# def get_answer():
# def get_prop():
#     properties = frappe.get_all("Question", fields=["question_degree", "question", "course"])
#     return properties
        # properties = frappe.db.sql(f"""SELECT question_degree, question, course from `tabQuestion`;""")
        # return properties





# def get_context(context):
#     name = frappe.form_dict.name  # الحصول على id_exam من URL
#     question_list = frappe.get_doc("Model", name)
#     context.name = question_list.name
#     context.collage = question_list.collage  
    # questions_with_answers = []
    # for question_median in question_list.get("question"):
    #             question = frappe.get_doc("Question", question_median.question)
                                
    #             questions_with_answers.append({
    #                             "question": question.question,
    #                             # "answer_choices": question.answer_choices
    #                             })



#     context.view=questions_with_answers


#     return context

# @frappe.whitelist()
# def AddSelectedValue(selected_answers):

#     doc=frappe.new_doc("Exam Review")
#     doc.department="hh"
#     doc.insert()

#     return "Data saved successfully"
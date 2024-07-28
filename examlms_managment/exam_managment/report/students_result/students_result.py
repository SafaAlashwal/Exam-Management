import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    
    # Define the columns
    columns = [
        {
            "fieldname": "student_id",
            "label": _("Student ID"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "student_name",
            "label": _("Student Name"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "course_count",
            "label": _("Course Count"),
            "fieldtype": "Int",
            "width": 120
        },
        {
            "fieldname": "course_details",
            "label": _("Course Details"),
            "fieldtype": "HTML",
            "width": 400
        },
        # {
        #     "fieldname": "total_marks",
        #     "label": _("Total Marks"),
        #     "fieldtype": "Float",
        #     "width": 150
        # },
        # {
        #     "fieldname": "appreciation",
        #     "label": _("Appreciation"),
        #     "fieldtype": "Data",
        #     "width": 150
        # },
    ]
    
    # Fetch the data
    student_answers = frappe.get_all('Student Answer', fields=['student_id', 'student_name', 'course', 'total_mark', 'appreciation'])
    
    student_data = {}
    
    for answer in student_answers:
        if answer.student_id not in student_data:
            student_data[answer.student_id] = {
                'student_name': answer.student_name,
                'courses': {},
                'appreciation': answer.appreciation
            }
        
        if answer.course not in student_data[answer.student_id]['courses']:
            student_data[answer.student_id]['courses'][answer.course] = {
                'total_mark': 0,
                'appreciation': answer.appreciation
            }
        
        student_data[answer.student_id]['courses'][answer.course]['total_mark'] += answer.total_mark
    
    for student_id, details in student_data.items():
        course_details_html = """
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr>
                    <th style="text-align: left;">Course</th>
                    <th style="text-align: right;">Total Marks</th>
                    <th style="text-align: right;">Appreciation</th>
                </tr>
            </thead>
            <tbody>
        """
        for course, info in details['courses'].items():
            course_details_html += f"""
            <tr>
                <td style="text-align: left; white-space: normal;">{course}</td>
                <td style="text-align: right; white-space: normal;">{info['total_mark']}</td>
                <td style="text-align: right; white-space: normal;">{info['appreciation']}</td>
            </tr>
            """
        course_details_html += """
            </tbody>
        </table>
        """
        
        # total_marks = sum([info['total_mark'] for info in details['courses'].values()])
        data.append({
            'student_id': student_id,
            'student_name': details['student_name'],
            'course_count': len(details['courses']),
            'course_details': course_details_html,
            # 'total_marks': total_marks,
            # 'appreciation': details['appreciation']
        })
    
    return columns, data

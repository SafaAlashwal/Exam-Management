import frappe
from frappe import _
from frappe.utils import cint


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	charts = get_charts(data)
	return columns, data, [], charts


def get_data(filters=None):
	summary = []
	query_filter = {}
	if filters:
		query_filter = {"course": filters.course}

	results = frappe.get_all(
		"Student Answer",
		query_filter,
		["name", "course", "student_id", "student_name", "total_mark", "appreciation"],
		order_by="course",
	)

	for result in results:
		summary.append(
			frappe._dict(
				{
					"course": result.course,
					"student_id": result.student_id,
					"student_name": result.student_name,
					"total_mark": result.total_mark,
					"appreciation": result.appreciation,
				}
			)
		)

	return summary


def get_columns():
	return [
		{
			"fieldname": "course",
			"fieldtype": "Data",
			"label": _("Course"),
			"width": 200,
		},
		{
			"fieldname": "student_id",
			"fieldtype": "Data",
			"label": _("Student ID"),
			"width": 150,
		},
		{
			"fieldname": "student_name",
			"fieldtype": "Data",
			"label": _("Student Name"),
			"width": 200,
		},
		{
			"fieldname": "total_mark",
			"fieldtype": "Float",
			"label": _("Total Mark"),
			"width": 120,
		},
		{
			"fieldname": "appreciation",
			"fieldtype": "Data",
			"label": _("Appreciation"),
			"width": 150,
		},
	]
def get_charts(data):
    if not data:
        return None

    total_students = len(data)
    if total_students == 0:
        return None

    grades = {
        "90-100": 0,
        "80-89": 0,
        "70-79": 0,
        "60-69": 0,
        "50-59": 0,
        "0-49": 0,
    }

    for row in data:
        if row.total_mark >= 90:
            grades["90-100"] += 1
        elif row.total_mark >= 80:
            grades["80-89"] += 1
        elif row.total_mark >= 70:
            grades["70-79"] += 1
        elif row.total_mark >= 60:
            grades["60-69"] += 1
        elif row.total_mark >= 50:
            grades["50-59"] += 1
        else:
            grades["0-49"] += 1

    colors = []
    for grade_range, count in grades.items():
        if grade_range == "90-100":
            colors.append("#0000ff")  # Blue for 90-100
        elif grade_range == "0-49":
            colors.append("#ff0000")  # Red for 0-49
        else:
            colors.append("#00ff00")  # Green for other ranges

    charts = {
        "data": {
            "labels": list(grades.keys()),
            "datasets": [
                {
                    "name": "Grades Distribution",
                    "values": list(grades.values()),
                }
            ],
        },
        "type": "bar",
        "colors": colors,
        "axisOptions": {
            "xAxisMode": "tick",
            "yAxisMode": "tick",
            "yAxisStepSize": 1
        }
    }
    return charts

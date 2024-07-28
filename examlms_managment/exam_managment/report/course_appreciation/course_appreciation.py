# Copyright (c) 2024, Safa and contributors
# For license information, please see license.txt

# import frappe

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

    appreciations = {}

    for row in data:
        if row.appreciation in appreciations:
            appreciations[row.appreciation] += 1
        else:
            appreciations[row.appreciation] = 1

    colors = ["#cc0000","#007fff"]  # Dark green and red

    charts = {
        "data": {
            "labels": list(appreciations.keys()),
            "datasets": [
                {
                    "name": "Appreciation Distribution",
                    "values": list(appreciations.values()),
                }
            ],
        },
        "type": "pie",
        "colors": colors,
    }
    return charts
// Copyright (c) 2024, Safa and contributors
// For license information, please see license.txt

frappe.query_reports["Course Appreciation"] = {
    "filters": [
        {
            fieldname: "course",
            label: __("Course"),
            fieldtype: "Link",
            options: "Course",
            reqd: 1,
        },
    ]
};

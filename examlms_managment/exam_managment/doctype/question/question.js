frappe.ui.form.on('Question', {
    refresh(frm) {
        const doctor = frappe.session.user;
        // ضبط التصفية على الحقل "custom_chapter"
        frm.set_query("custom_chapter", function() {
            return {
                filters: {
                    course: frm.doc.custom_course
                }
            };
        });
        // استدعاء الدالة لتصفية الكورسات بناءً على المستخدم (الدكتور)
        frm.call({
            method: 'get_filtered_course',
            args: {
                doctor: doctor,
            },
            callback: function(res) {
                let courses = res.message?.courses;
                if (courses) {
                    // ضبط التصفية على حقل الكورسات
                    frm.set_query('custom_course', function() {
                        return {
                            filters: {
                                name: ['in', courses]
                            }
                        };
                    });
                } else {
                    frappe.msgprint('No courses found for the current doctor.');
                }
            }
        });
        console.log(frappe.session.user);
    }
});

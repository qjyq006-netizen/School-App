from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display

def fix_arabic(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        toolbar = MDTopAppBar(title=fix_arabic("نظام إدارة المدرسة الذكي"))
        layout.add_widget(toolbar)
        content_layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15)
        welcome_label = MDLabel(text=fix_arabic("مرحباً بك! يرجى اختيار أحد الأقسام:"), halign="center", font_style="H6")
        content_layout.add_widget(welcome_label)
        btn1 = MDRaisedButton(text=fix_arabic("إدارة شؤون الطلاب"), pos_hint={'center_x': 0.5}, size_hint_x=0.8, on_release=self.go_to_students)
        btn2 = MDRaisedButton(text=fix_arabic("سجل الحضور والغياب"), pos_hint={'center_x': 0.5}, size_hint_x=0.8, on_release=self.go_to_attendance)
        btn3 = MDRaisedButton(text=fix_arabic("رصد درجات الامتحانات"), pos_hint={'center_x': 0.5}, size_hint_x=0.8, on_release=self.go_to_grades)
        btn4 = MDRaisedButton(text=fix_arabic("الحسابات والأقساط المالية"), pos_hint={'center_x': 0.5}, size_hint_x=0.8, on_release=self.go_to_accounts)
        content_layout.add_widget(btn1)
        content_layout.add_widget(btn2)
        content_layout.add_widget(btn3)
        content_layout.add_widget(btn4)
        layout.add_widget(content_layout)
        self.add_widget(layout)
    def go_to_students(self, instance): self.manager.current = 'students'
    def go_to_attendance(self, instance): self.manager.current = 'attendance'
    def go_to_grades(self, instance): self.manager.current = 'grades'
    def go_to_accounts(self, instance): self.manager.current = 'accounts'

class StudentsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        toolbar = MDTopAppBar(title=fix_arabic("قاعدة بيانات الطلاب"))
        layout.add_widget(toolbar)
        content = MDBoxLayout(orientation='vertical', padding=20, spacing=15)
        self.student_input = MDTextField(hint_text=fix_arabic("أدخل اسم الطالب هنا"), pos_hint={'center_x': 0.5}, size_hint_x=0.9)
        content.add_widget(self.student_input)
        btn_save = MDRaisedButton(text=fix_arabic("حفظ اسم الطالب"), pos_hint={'center_x': 0.5}, on_release=self.save_student_name)
        content.add_widget(btn_save)
        self.students_list_label = MDLabel(text=fix_arabic("الطلاب المسجلين:\nلا يوجد حالياً"), halign="center", font_style="Body1", theme_text_color="Secondary")
        content.add_widget(self.students_list_label)
        self.database = []
        btn_back = MDRaisedButton(text=fix_arabic("الرجوع للقائمة الرئيسية"), pos_hint={'center_x': 0.5}, on_release=self.go_back)
        content.add_widget(btn_back)
        layout.add_widget(content)
        self.add_widget(layout)
    def save_student_name(self, instance):
        name = self.student_input.text.strip()
        if name:
            self.database.append(name)
            self.student_input.text = ""
            output = "الطلاب المسجلين:\n" + "\n".join(self.database)
            self.students_list_label.text = fix_arabic(output)
    def go_back(self, instance): self.manager.current = 'main'

class AttendanceScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        toolbar = MDTopAppBar(title=fix_arabic("سجل الحضور والغياب اليومي"))
        layout.add_widget(toolbar)
        content = MDBoxLayout(orientation='vertical', padding=20, spacing=15)
        self.attendance_student_input = MDTextField(hint_text=fix_arabic("اسم الطالب لتسجيل حالته"), pos_hint={'center_x': 0.5}, size_hint_x=0.9)
        content.add_widget(self.attendance_student_input)
        buttons_layout = MDBoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height="50dp", pos_hint={'center_x': 0.5})
        btn_present = MDRaisedButton(text=fix_arabic("حاضر"), on_release=lambda x: self.record_attendance("حاضر"))
        btn_absent = MDRaisedButton(text=fix_arabic("غائب"), md_bg_color=(0.9, 0.3, 0.3, 1), on_release=lambda x: self.record_attendance("غائب"))
        buttons_layout.add_widget(btn_present)
        buttons_layout.add_widget(btn_absent)
        content.add_widget(buttons_layout)
        self.attendance_list_label = MDLabel(text=fix_arabic("قائمة الحضور اليوم لقسم الطلاب:\nلا توجد سجلات بعد"), halign="center", font_style="Body1", theme_text_color="Secondary")
        content.add_widget(self.attendance_list_label)
        self.attendance_db = []
        btn_back = MDRaisedButton(text=fix_arabic("الرجوع للقائمة الرئيسية"), pos_hint={'center_x': 0.5}, on_release=self.go_back)
        content.add_widget(btn_back)
        layout.add_widget(content)
        self.add_widget(layout)
    def record_attendance(self, status):
        student_name = self.attendance_student_input.text.strip()
        if student_name:
            current_time = datetime.now().strftime("%Y-%m-%d")
            record = f"{student_name} -> {status} ({current_time})"
            self.attendance_db.append(record)
            self.attendance_student_input.text = ""
            output = "قائمة الحضور اليوم لقسم الطلاب:\n" + "\n".join(self.attendance_db)
            self.attendance_list_label.text = fix_arabic(output)
    def go_back(self, instance): self.manager.current = 'main'

class GradesScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        toolbar = MDTopAppBar(title=fix_arabic("لوحة رصد درجات الاختبارات"))
        layout.add_widget(toolbar)
        content = MDBoxLayout(orientation='vertical', padding=15, spacing=10)
        self.grade_student_input = MDTextField(hint_text=fix_arabic("اسم الطالب"), pos_hint={'center_x': 0.5}, size_hint_x=0.9)
        content.add_widget(self.grade_student_input)
        self.subject_input = MDTextField(hint_text=fix_arabic("المادة الدراسية (مثال: الرياضيات)"), pos_hint={'center_x': 0.5}, size_hint_x=0.9)
        content.add_widget(self.subject_input)
        self.score_input = MDTextField(hint_text=fix_arabic("الدرجة المستحقة (من 100)"), input_filter="int", pos_hint={'center_x': 0.5}, size_hint_x=0.9)
        content.add_widget(self.score_input)
        btn_save_grade = MDRaisedButton(text=fix_arabic("حفظ ورصد الدرجة"), pos_hint={'center_x': 0.5}, on_release=self.save_grade)
        content.add_widget(btn_save_grade)
        self.grades_list_label = MDLabel(text=fix_arabic("كشف درجات الطلاب الحالي:\nلم يتم رصد درجات بعد"), halign="center", font_style="Body1", theme_text_color="Secondary")
        content.add_widget(self.grades_list_label)
        self.grades_db = []
        btn_back = MDRaisedButton(text=fix_arabic("الرجوع للقائمة الرئيسية"), pos_hint={'center_x': 0.5}, on_release=self.go_back)
        content.add_widget(btn_back)
        layout.add_widget(content)
        self.add_widget(layout)
    def save_grade(self, instance):
        student = self.grade_student_input.text.strip()
        subject = self.subject_input.text.strip()
        score = self.score_input.text.strip()
        if student and subject and score:
            record = f"الطالب: {student} | المادة: {subject} | الدرجة: {score}/100"
            self.grades_db.append(record)
            self.grade_student_input.text = ""
            self.subject_input.text = ""
            self.score_input.text = ""
            output = "كشف درجات الطلاب الحالي:\n" + "\n".join(self.grades_db)
            self.grades_list_label.text = fix_arabic(output)
    def go_back(self, instance): self.manager.current = 'main'

class AccountsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        toolbar = MDTopAppBar(title=fix_arabic("لوحة الحسابات والأقساط المالية"))
        layout.add_widget(toolbar)
        content = MDBoxLayout(orientation='vertical', padding=15, spacing=10)
        self.fee_student_input = MDTextField(hint_text=fix_arabic("اسم الطالب"), pos_hint={'center_x': 0.5}, size_hint_x=0.9)
        content.add_widget(self.fee_student_input)
        self.total_input = MDTextField(hint_text=fix_arabic("المبلغ الإجمالي المطلوب ($)"), input_filter="int", pos_hint={'center_x': 0.5}, size_hint_x=0.9)
        content.add_widget(self.total_input)
        self.paid_input = MDTextField(hint_text=fix_arabic("المبلغ المدفوع حالياً ($)"), input_filter="int", pos_hint={'center_x': 0.5}, size_hint_x=0.9)
        content.add_widget(self.paid_input)
        btn_save_payment = MDRaisedButton(text=fix_arabic("احتساب وحفظ العملية المالية"), pos_hint={'center_x': 0.5}, on_release=self.save_payment)
        content.add_widget(btn_save_payment)
        self.payments_list_label = MDLabel(text=fix_arabic("السجلات المالية الأخيرة:\nلا توجد عمليات حالياً"), halign="center", font_style="Body1", theme_text_color="Secondary")
        content.add_widget(self.payments_list_label)
        self.payments_db = []
        btn_back = MDRaisedButton(text=fix_arabic("الرجوع للقائمة الرئيسية"), pos_hint={'center_x': 0.5}, on_release=self.go_back)
        content.add_widget(btn_back)
        layout.add_widget(content)
        self.add_widget(layout)
    def save_payment(self, instance):
        student_name = self.fee_student_input.text.strip()
        total = self.total_input.text.strip()
        paid = self.paid_input.text.strip()
        if student_name and total and paid:
            try:
                total_val = int(total)
                paid_val = int(paid)
                remaining_val = total_val - paid_val
                record = f"الاسم: {student_name} | الإجمالي: {total_val} | المدفوع: {paid_val} | المتبقي: {remaining_val}"
                self.payments_db.append(record)
                self.fee_student_input.text = ""
                self.total_input.text = ""
                self.paid_input.text = ""
                output = "السجلات المالية الأخيرة:\n" + "\n".join(self.payments_db)
                self.payments_list_label.text = fix_arabic(output)
            except ValueError: pass
    def go_back(self, instance): self.manager.current = 'main'

class SchoolManagementApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(StudentsScreen(name='students'))
        sm.add_widget(AttendanceScreen(name='attendance'))
        sm.add_widget(GradesScreen(name='grades'))
        sm.add_widget(AccountsScreen(name='accounts'))
        return sm

if __name__ == "__main__":
    SchoolManagementApp().run()

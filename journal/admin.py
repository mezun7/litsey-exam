from django.contrib import admin

# Register your models here.
from journal.models import Teacher, Class, Subject, Mark, Student


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject')
    search_fields = ('user', 'subject')

class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'class1_teacher')
    search_fields = ('name',)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('lname', 'fname', 'school', 'class_name')
    search_fields = ('lname', 'fname', 'school')

class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'date', 'mark')
    search_fields = ('student', 'teacher', 'mark')
    list_filter = ('date',)

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Subject)
admin.site.register(Student, StudentAdmin)
admin.site.register(Mark, MarkAdmin)
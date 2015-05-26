from django.contrib import admin

# Register your models here.
from django.http import HttpResponse
from journal.models import Teacher, Class, Subject, Mark, Student


def export_csv(StudentAdmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"ID"),
        smart_str(u"Surname"),
        smart_str(u"Name"),
        smart_str(u'School'),
        smart_str(u"Class"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.fname),
            smart_str(obj.lname),
            smart_str(obj.school),
            smart_str(obj.class_name),
        ])
    return response
export_csv.short_description = u"Export CSV"

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject')
    search_fields = ('user', 'subject')

class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'class1_teacher')
    search_fields = ('name',)
class StudentAdmin(admin.ModelAdmin):
    actions = [export_csv,]
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


# Create your views here.
import datetime
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormMixin
import math
from journal.forms import LoginForm, AddMarkForm
from journal.models import Teacher, Class, Student, Subject, Mark
from journal.structs import StudentStruct, StudentInfoStruct, StudentsRaitingStruct, StudentsRaitingStruct2, SubjectInfo

def increase(request):
    #logics
    lst6 = [8, 2]
    for el in lst6:
        teacher = Teacher.objects.get(pk=el)
        marks = Mark.objects.filter(teacher=teacher)
        for mark in marks:
            mark.mark *= 0.6
            mark.save()
    lst5 = [17, 16, 15, 14, 13, 12, 11, 10, 9]
    for el in lst5:
        teacher = Teacher.objects.get(pk=el)
        marks = Mark.objects.filter(teacher=teacher)
        for mark in marks:
            mark.mark *= 0.5
            mark.save()
    lst3 = [4]
    for el in lst3:
        teacher = Teacher.objects.get(pk=el)
        marks = Mark.objects.filter(teacher=teacher)
        for mark in marks:
            mark.mark *= 0.3
            mark.save()
def test(request):
    teacher = Teacher.objects.get(pk=2)
    marks = Mark.objects.filter(teacher=teacher)
    for mark in marks:
        mark.mark *= 2
        mark.save()

    return render(request, 'journal/base.html')

@login_required
def home(request):
    if request.user.is_staff:
        return raiting(request)
    context = {'TeacherName': request.user.first_name + " " + request.user.last_name}
    teacher = Teacher.objects.all()
    teachers = teacher.filter(user = request.user)
    classes = Class.objects.filter(teacher=teachers[0])
    #print test2[0].id
    context['classes'] = classes
    class_teacher = Class.objects.filter(class1_teacher=teachers[0])
    #context['class_teacher'] = class_teacher[0]
    return render(request, 'journal/home.html', context)

def class_list(request, class_id):
    students = Student.objects.filter(class_name=class_id)
    return render(request, 'journal/class_list.html', {'students': students})

def class_journal(request, class_id):
    form = AddMarkForm(Class.objects.get(pk=class_id), request.POST)
    teacher = Teacher.objects.get(user=request.user)
    if(form.is_valid()):
        mark = Mark()
        mark.teacher = teacher
        mark.student = form.cleaned_data['student']
        mark.mark = form.cleaned_data['mark']
        mark.date = datetime.datetime.now()
        mark.save()

    students = Student.objects.filter(class_name=class_id)

    marks = Mark.objects.filter(teacher=teacher)
    lst = []
    maxx = 0
    for student in students:
        marks2 = marks.filter(student=student)
        maxx = max(maxx, len(marks2))
        tmp = StudentStruct(student, marks2)
        lst.append(tmp)
    for i in lst:
        i.delta(maxx)
    lst.sort(key=lambda x : x.student.fname, reverse=False)

    teacher = Teacher.objects.all()
    teachers = teacher.filter(user = request.user)
    classes = Class.objects.filter(teacher=teachers[0])
    #print test2[0].id
    classes = classes
    #class_teacher = Class.objects.filter(class1_teacher=teachers[0])
    #class_teacher = class_teacher[0]
    class_name = Class.objects.get(pk=class_id)
    class_name = class_name.name
    return render(request, 'journal/class_journal.html', {'list':lst, 'maxx': range(maxx), 'form': form, 'id': class_id,
                  'classes': classes, 'name': class_name})

def log_out(request):
    if request.user.is_authenticated():
       logout(request)
    return HttpResponseRedirect(reverse('journal:home'))

class LoginView(View,TemplateResponseMixin,FormMixin):
    form_class = LoginForm
    template_name="journal/login.html"
    success_url = reverse_lazy("journal:home")

    def get_context_data(self,**kwargs):
        context = super(LoginView,self).get_context_data(**kwargs)
        context["form"] = self.get_form(self.get_form_class())
        return context

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('journal:home'))
        return self.render_to_response(self.get_context_data(),**kwargs)

    def post(self,request,*args,**kwargs):
        form = self.get_form(self.get_form_class())
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username,password=password)
        if user is not None:
            login(self.request,user)
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseRedirect(reverse('journal:login'))

    def form_invalid(self,form):
        return self.get(self.request)

def student_profile(request, student_id):
    student = Student.objects.get(pk=student_id)
    teacher = Teacher.objects.all()
    classes = Class.objects.all()
    marks = student.mark_set.all()
    class_teacher = student.class_name.class1_teacher
    list = []
    context = {}
    for mark in marks:
        if context.has_key(mark.teacher.subject):
            context[mark.teacher.subject].append(mark.mark)
        else:
            context[mark.teacher.subject] = [mark.mark]
    maxx = 0
    for subject in Subject.objects.all():
        if not subject in context.keys():
            context[subject] = [0.0]
    for key in context.keys():
        list.append(StudentInfoStruct(subject=key, marks=context[key]))
        maxx = max(maxx, len(context[key]))
    for i in list:
        i.delta(maxx)
    print list
    list.sort(key=lambda x:x.avg, reverse=True)
    return render(request, 'journal/student.html', {'student': student, 'classes': classes, 'list':list, 'maxx':range(maxx), 'class_teacher':class_teacher})

def raiting(request):
    students = Student.objects.all()
    print students
    list = []
    for student in students:
        context = {}
        for mark in student.mark_set.all():
            if context.has_key(mark.teacher.subject):
                context[mark.teacher.subject].append(mark.mark)
            else:
                context[mark.teacher.subject] = [mark.teacher.subject, mark.mark]
        for subject in Subject.objects.all():
            if not subject in context.keys():
                context[subject] = [subject, 0.0]
        marks = []
        for key in context.keys():
            marks.append(context[key])

        marks.sort(key=lambda x : x[0].name, reverse=False)
        list.append(StudentsRaitingStruct(student, marks))
        print len(list)
    for marks in list:
        print True
        print '---',marks.student, '-----'
        print marks.marks
    list.sort(key=lambda x : x.avg, reverse=True)
    sum = 1
    for i in list:
        i.setNum(sum)
        sum += 1
    subjects = []
    tmp_subjects = Subject.objects.all().order_by('name')
    print tmp_subjects
    for subject in tmp_subjects:
        teachers = Teacher.objects.filter(subject=subject)
        subjects.append(SubjectInfo(subject, teachers))
    
    four = list[:4]
    return render(request, 'journal/raiting.html', {'list':list, 'subjects':subjects, 'four': four})

def raiting2(request):
    students = Student.objects.all()
    print students
    list = []
    for student in students:
        context = {}
        for mark in student.mark_set.all():
            if context.has_key(mark.teacher.subject):
                context[mark.teacher.subject].append(mark.mark)
            else:
                context[mark.teacher.subject] = [mark.teacher.subject, mark.mark]
            if mark.teacher.subject == Subject.objects.get(pk=11) or mark.teacher.subject == Subject.objects.get(pk=10):
                context[mark.teacher.subject] = [mark.teacher.subject, 0.0]
        for subject in Subject.objects.all():
            if not subject in context.keys():
                context[subject] = [subject, 0.0]
        marks = []
        for key in context.keys():
            marks.append(context[key])

        marks.sort(key=lambda x : x[0].name, reverse=False)
        list.append(StudentsRaitingStruct2(student, marks))
        print len(list)
    for marks in list:
        print True
        print '---',marks.student, '-----'
        print marks.marks
    list.sort(key=lambda x : x.avg, reverse=True)
    sum = 1
    for i in list:
        i.setNum(sum)
        sum += 1
    subjects = []
    tmp_subjects = Subject.objects.all().order_by('name')
    print tmp_subjects
    for subject in tmp_subjects:
        teachers = Teacher.objects.filter(subject=subject)
        subjects.append(SubjectInfo(subject, teachers))
    four = list[:4]
    return render(request, 'journal/raiting.html', {'list': list, 'subjects': subjects, 'four': four})

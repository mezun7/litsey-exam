# coding=utf-8
# Create your views here.
import csv
import datetime
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy, resolve
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormMixin
import math
from journal.forms import LoginForm, AddMarkForm, StudentForm, UploadForm
from journal.models import Teacher, Class2, Student, Subject, Mark, MarksCoeff, Parallel
from journal.structs import StudentStruct, StudentInfoStruct, StudentsRaitingStruct, StudentsRaitingStruct2, \
    SubjectInfo, \
    MarkStruct, ClassStruct, RegisterStruct


def get_class(teacher_id):
    return Class2.objects.filter(teacher=teacher_id).order_by('parallel', 'name')

@login_required
def increase(request):
    # logics
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


@login_required
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
    teachers = teacher.filter(user=request.user)
    return class_journal(request, teachers[0].class2_set.all().order_by('parallel','name')[0].id)

    classes = get_class(teachers[0])
    # print test2[0].id
    context['classes'] = classes
    class_teacher = Class2.objects.filter(class1_teacher=teachers[0])
    # context['class_teacher'] = class_teacher[0]
    return render(request, 'journal/home.html', context)


@login_required
def class_list(request, class_id):
    students = Student.objects.filter(class_name=class_id)
    class_name = Class2.objects.get(id=class_id)
    class_name = class_name.parallel.name + class_name.name
    return render(request, 'journal/class_list.html', {'students': students, 'name': class_name})


@login_required
def class_journal(request, class_id):
    form = AddMarkForm(Class2.objects.get(pk=class_id), request.POST)
    teacher = Teacher.objects.get(user=request.user)

    if form.is_valid():
        mark = Mark()
        mark.teacher = teacher
        mark.student = form.cleaned_data['student']
        mark.mark = form.cleaned_data['mark']
        mark.date = datetime.datetime.now()
        mark.comment = form.cleaned_data['comment']
        mark.save()
        return HttpResponseRedirect('')

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
    lst.sort(key=lambda x: x.student.fname, reverse=False)

    teacher = Teacher.objects.all()
    teachers = teacher.filter(user=request.user)
    classes = get_class(teachers[0])
    # print test2[0].id
    # class_teacher = Class.objects.filter(class1_teacher=teachers[0])
    # class_teacher = class_teacher[0]
    class_name = Class2.objects.get(pk=class_id)
    class_name = class_name.parallel.name + class_name.name
    return render(request, 'journal/class_journal.html',
                  {'list': lst, 'maxx': range(maxx), 'form': form, 'id': class_id,
                   'classes': classes, 'name': class_name, 'current': class_id})


def delete_mark(request, mark_id):
    class_id = 1
    if request.GET.has_key('from'):
        class_id = request.GET['from']
    Mark.objects.get(id=mark_id).delete()

    return HttpResponseRedirect(reverse('journal:class_journal', args=[class_id]))


def get_phone_book(request, class_id=1):
    lst = []
    students = Student.objects.filter(class_name=class_id)
    for student in students:
        lst.append(student)
        print student

    name = Class2.objects.get(pk=class_id)
    context = {'list': lst,
               'name': name}

    return render(request, 'journal/phone_book.html', context)


def log_out(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect(reverse('journal:home'))


class LoginView(View, TemplateResponseMixin, FormMixin):
    form_class = LoginForm
    template_name = "journal/login.html"
    success_url = reverse_lazy("journal:home")

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context["form"] = self.get_form(self.get_form_class())
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('journal:home'))
        return self.render_to_response(self.get_context_data(), **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseRedirect(reverse('journal:login'))

    def form_invalid(self, form):
        return self.get(self.request)


@login_required
def student_profile(request, student_id):
    student = Student.objects.get(pk=student_id)
    subjects = student.class_name.parallel.subject.all()
    teacher = Teacher.objects.all()
    classes = Class2.objects.all()
    marks = student.mark_set.all()
    coeffs = {}
    coeffs_list = MarksCoeff.objects.all()
    for coeff in coeffs_list:
        coeffs[coeff.subject] = coeff.coeff
    class_teacher = student.class_name.class1_teacher
    list = []
    context = {}
    subj_context = {}
    for teacher in student.class_name.teacher.all():
        # print teacher.subject
        subj_context[teacher.subject] = teacher.user.get_full_name()

    for mark in marks:

        if context.has_key(mark.teacher.subject):
            context[mark.teacher.subject].append(
                MarkStruct(mark.mark * coeffs[mark.teacher.subject], mark.comment, mark.id))
        else:
            context[mark.teacher.subject] = [
                MarkStruct(mark.mark * coeffs[mark.teacher.subject], mark.comment, mark.id)]

    maxx = 0
    for subject in subjects:
        if not subject in context.keys():
            context[subject] = [MarkStruct(0, comment=None, id=None)]
    for key in context.keys():
        # print subj_context
        list.append(StudentInfoStruct(subject=key, marks=context[key], teacher=subj_context[key]))
        maxx = max(maxx, len(context[key]))
    for i in list:
        i.delta(maxx)
    # print list
    list.sort(key=lambda x: x.avg, reverse=True)
    parallel = student.class_name.parallel
    return render(request, 'journal/student.html',
                  {'student': student, 'classes': classes, 'list': list, 'maxx': range(maxx),
                   'class_teacher': class_teacher, 'parallel': parallel})


@login_required
def raiting(request, parallel=1):
    coeffs = {}
    coeffs_list = MarksCoeff.objects.all()
    parallel_link = Parallel.objects.get(pk=parallel)
    tmp_subjects = parallel_link.subject.all()
    for coeff in coeffs_list:
        coeffs[coeff.subject] = coeff.coeff
    # print coeffs_list, "Yes"
    students = Student.objects.filter(class_name__isnull=False, class_name__parallel=parallel)
    list = []
    for student in students:
        context = {}
        for mark in student.mark_set.all():
            # print mark.teacher.subject.markscoeff_set, "YEs"
            if context.has_key(mark.teacher.subject):
                context[mark.teacher.subject].append(mark.mark * coeffs[mark.teacher.subject])
            else:
                context[mark.teacher.subject] = [mark.teacher.subject, mark.mark * coeffs[mark.teacher.subject]]
        for subject in tmp_subjects:
            if not subject in context.keys():
                context[subject] = [subject, 0.0]
        marks = []
        for key in context.keys():
            marks.append(context[key])

        marks.sort(key=lambda x: x[0].name, reverse=False)
        list.append(StudentsRaitingStruct(student, marks))
        # print len(list)
    # for marks in list:
    #     #print True
    #     #print '---', marks.student, '-----'
    #     #print marks.marks
    list.sort(key=lambda x: x.avg, reverse=True)
    sum = 1
    for i in list:
        i.setNum(sum)
        sum += 1
    subjects = []
    # print tmp_subjects
    for subject in tmp_subjects:
        teachers = Teacher.objects.filter(subject=subject)
        subjects.append(SubjectInfo(subject, teachers))

    four = list[:4]
    parallels = Parallel.objects.all().order_by('name')

    return render(request, 'journal/raiting.html', {'list': list, 'subjects': subjects, 'four': four,
                                                    'parallels': parallels, 'parallel': parallel_link})


@login_required
def print_raiting(request):
    coeffs = {}
    coeffs_list = MarksCoeff.objects.all()
    for coeff in coeffs_list:
        coeffs[coeff.subject] = coeff.coeff
    # print coeffs_list, "Yes"
    students = Student.objects.filter(class_name__isnull=False)
    list = []
    for student in students:
        context = {}
        for mark in student.mark_set.all():
            # print mark.teacher.subject.markscoeff_set, "YEs"
            if context.has_key(mark.teacher.subject):
                context[mark.teacher.subject].append(mark.mark * coeffs[mark.teacher.subject])
            else:
                context[mark.teacher.subject] = [mark.teacher.subject, mark.mark * coeffs[mark.teacher.subject]]
        for subject in Subject.objects.all():
            if not subject in context.keys():
                context[subject] = [subject, 0.0]
        marks = []
        for key in context.keys():
            marks.append(context[key])

        marks.sort(key=lambda x: x[0].name, reverse=False)
        list.append(StudentsRaitingStruct(student, marks))
        # print len(list)
    # for marks in list:
    #     #print True
    #     #print '---', marks.student, '-----'
    #     #print marks.marks
    list.sort(key=lambda x: x.avg, reverse=True)
    sum = 1
    for i in list:
        i.setNum(sum)
        sum += 1
    subjects = []
    tmp_subjects = Subject.objects.all().order_by('name')
    # print tmp_subjects
    for subject in tmp_subjects:
        teachers = Teacher.objects.filter(subject=subject)
        subjects.append(SubjectInfo(subject, teachers))

    four = list[:4]
    return render(request, 'journal/print-raiting.html', {'list': list, 'subjects': subjects, 'four': four})


@login_required
def raiting2(request):
    students = Student.objects.filter(class_name__isnull=False)
    # print students
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

        marks.sort(key=lambda x: x[0].name, reverse=False)
        list.append(StudentsRaitingStruct2(student, marks))
        # print len(list)
    # for marks in list:
    #     #print True
    #     #print '---', marks.student, '-----'
    #     #print marks.marks
    list.sort(key=lambda x: x.avg, reverse=True)
    sum = 1
    for i in list:
        i.setNum(sum)
        sum += 1
    subjects = []
    tmp_subjects = Subject.objects.all().order_by('name')
    # print tmp_subjects
    for subject in tmp_subjects:
        teachers = Teacher.objects.filter(subject=subject)
        subjects.append(SubjectInfo(subject, teachers))
    four = list[:4]
    return render(request, 'journal/raiting.html', {'list': list, 'subjects': subjects, 'four': four})


def get_overall(request):
    lst = []
    cls = Class2.objects.all()
    sum2 = 0
    for i in cls:
        name = i.name
        sum = i.student_set.count()
        sum2 += int(sum)
        lst.append(ClassStruct(i.parallel.name + name, sum))
    tmp = ClassStruct('Всего', sum2)
    lst.append(tmp)
    tmp2 = ClassStruct('Всего пригласили', Student.objects.all().count())
    lst.append(tmp2)
    context = {
        'list': lst
    }

    return render(request, 'journal/overall.html', context)


@login_required()
def students_list(request):
    context = {}
    lst = []

    students = Student.objects.filter(class_name__isnull=True).order_by('fname')
    for student in students:
        tmp = RegisterStruct(student.fname + " " + student.lname + " " + student.fathers_name, student.school,
                             student.phone_parent, student.pay_for_eating, student.class_name, student.id)
        lst.append(tmp)
    context['students'] = lst

    return render(request, 'journal/students.html', context)


@login_required()
def student_edit(request, stud_id):
    parallels = Parallel.objects.all()

    student = Student.objects.get(id=stud_id)
    try:
        if student.class_name is not None:
            cls = student.class_name
        else:
            cls = Class2.objects.get(class1_teacher=request.user.id)
    except:
        cls = None
    studentForm = StudentForm(student, cls)
    if request.POST:
        studentForm = StudentForm(student, cls, request.POST)
        if studentForm.is_valid():
            student.fname = studentForm.cleaned_data['fname']
            student.lname = studentForm.cleaned_data['lname']
            student.fathers_name = studentForm.cleaned_data['fathers_name']
            student.school = studentForm.cleaned_data['school']
            student.class_name = studentForm.cleaned_data['class']
            student.medical_card = studentForm.cleaned_data['medical']
            student.report_from_school = studentForm.cleaned_data['school-req']
            student.phone_parent = studentForm.cleaned_data['phone-parent']
            student.phone_number = studentForm.cleaned_data['phone-child']
            student.pay_for_eating = studentForm.cleaned_data['money']
            student.save()
            return HttpResponseRedirect(reverse('journal:list'))

    context = {'student': studentForm,
               'parallels': parallels}
    return render(request, 'journal/edit.html', context)


@login_required()
def upload_csv(request):
    context = {
        'form': UploadForm()
    }
    if request.POST:
        form = UploadForm(request.POST, request.FILES)
        print(request.FILES.keys())
        csv_file = request.FILES["csv_file"]
        file_data = csv_file.read()
        reader = csv.DictReader(file_data.splitlines())
        lst = []
        for row in reader:
            student = Student()
            student.fname = row['Surname']
            student.lname = row['Name']
            student.fathers_name = row['Father']
            student.school = row['School']
            student.phone_parent = row['Phone']
            # Student phone number
            student.phone_number = row['PhoneC']
            lst.append(student)
        Student.objects.bulk_create(lst)
        return HttpResponseRedirect(reverse('journal:list'))
    return render(request, 'journal/upload.html', context)

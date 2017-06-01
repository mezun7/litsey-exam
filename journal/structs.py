from journal.models import Subject, Mark, Teacher

__author__ = 'shuhrat'


class StudentStruct:
    def __init__(self, student, marks):
        self.student = student
        self.marks = marks
        avg = 0.0

        for i in marks:
            avg += i.mark
            #print i.mark.teacher.subject.name + ": " + i.mark.teacher.subject.markscoeff_set[0]
        if len(marks) == 0:
            avg = 0
        else:
            avg /= len(marks)
        self.avg = avg

    def delta(self, maxx):
        self.iter = range(maxx - len(self.marks))

    def __unicode__(self):
        return self.student

class MarkStruct:
    def __init__(self, mark, comment, id):
        self.mark = mark
        self.comment = comment
        self.id = id

class StudentInfoStruct:
    def __init__(self, subject, marks, teacher):
        self.subject = subject
        self.teacher = teacher
        self.marks = marks
        print marks
        avg = 0.0
        for i in marks:
            avg = avg + i.mark

            #print type(i), i.comment, i.mark
            #print i.mark.mark

        avg /= len(marks)
        self.avg = avg

    def delta(self, maxx):
        self.iter = range(maxx - len(self.marks))

    def __unicode__(self):
        return self.subject


class StudentsRaitingStruct:
    def __init__(self, student, marks):
        self.student = student
        #self.marks = marks
        avg_overall = 0.0;
        sum = 0;
        lst = []
        for mark in marks:
            avg = 0.0
            for i in range(1, len(mark)):
                avg += float(mark[i])
                sum += 1
            if len(mark) - 1 > 0:
                avg /= len(mark) - 1
            else:
                avg = 0
            lst.append(avg)
            mark = avg
        for i in lst:
            avg_overall += i
        # if (len(lst) != 0):
        #     avg_overall /= len(lst)
        # else:
        #     avg_overall = 0.0
        self.avg = avg_overall
        self.marks = lst

    def setNum(self, num):
        self.num = num

    def __unicode__(self):
        return self.student

class StudentsRaitingStruct2:
    def __init__(self, student, marks):
        self.student = student
        #self.marks = marks
        avg_overall = 0.0;
        sum = 0;
        lst = []
        for mark in marks:
            avg = 0.0
            for i in range(1, len(mark)):
                avg += float(mark[i])
                sum += 1
            if len(mark) - 1 > 0:
                avg /= len(mark) - 1
            else:
                avg = 0
            lst.append(avg)
            mark = avg
        for i in lst:
            avg_overall += i
        avg_overall /= len(lst) - 2
        self.avg = avg_overall
        self.marks = lst

    def setNum(self, num):
        self.num = num

    def __unicode__(self):
        return self.student

class SubjectInfo:
    def __init__(self, subject, teachers_id):
        self.subject = subject.name
        sum = 0.0
        iter = 0
        for tid in teachers_id:
            marks = Mark.objects.filter(teacher=tid)
            for mark in marks:
                sum += mark.mark
                iter += 1
        if iter != 0:
            self.avg = sum / iter
        else:
            self.avg = 0

class ClassStruct:
    def __init__(self, name, sum):
        self.name = name
        self.sum = sum

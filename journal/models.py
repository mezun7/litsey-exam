from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    user = models.ForeignKey(User)
    subject = models.ForeignKey(Subject)

    def __unicode__(self):
        return self.user.last_name + " " + self.user.first_name


class Class(models.Model):
    name = models.CharField(max_length=20)
    class1_teacher = models.ForeignKey(User)
    teacher = models.ManyToManyField(Teacher, blank=True)

    def __unicode__(self):
        return self.name


class Student(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    class_name = models.ForeignKey(Class)
    photo = models.ImageField(blank=True, upload_to='avatars')
    about = models.CharField(max_length=1000, blank=True)

    def __unicode__(self):
        return self.fname + " " +  self.lname

class Mark(models.Model):
    mark = models.FloatField()
    teacher = models.ForeignKey(Teacher)
    date = models.DateField()
    student = models.ForeignKey(Student)

    def __unicode__(self):
        return self.student.lname + self.student.fname + ": " + str(self.mark)
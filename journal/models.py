# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
# -*- coding: utf-8 -*-
# Create your models here.
from django.core.validators import MaxValueValidator, MinValueValidator

class Subject(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название предмета')

    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Пользователь')
    subject = models.ForeignKey(Subject, verbose_name=u'Предмет')

    def __unicode__(self):
        return self.user.last_name + " " + self.user.first_name


class Class(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'Литер класса')
    class1_teacher = models.ForeignKey(User, verbose_name=u'Классный руководитель')
    teacher = models.ManyToManyField(Teacher, blank=True, verbose_name=u'Учителя класса')

    def __unicode__(self):
        return self.name


class Student(models.Model):
    fname = models.CharField(max_length=100, verbose_name=u'Фамилия')
    lname = models.CharField(max_length=100, verbose_name=u'Имя')
    fathers_name = models.CharField(max_length=100, verbose_name=u'Отчество')
    school = models.CharField(max_length=100, verbose_name=u'Школа')
    class_name = models.ForeignKey(Class, verbose_name=u'Класс')
    photo = models.ImageField(blank=True, upload_to='avatars', verbose_name=u'Фото')
    about = models.CharField(max_length=1000, blank=True)
    pay_for_eating = models.IntegerField(verbose_name=u'Оплата питания')
    report_from_school = models.BooleanField(default=False, verbose_name=u'Справка со школы')
    medical_card = models.BooleanField(default=False, verbose_name=u'Копия мед. карты')
    phone_number = models.CharField(max_length=13, verbose_name=u'Номер телефона ребенка', blank=True)
    phone_parent = models.CharField(max_length=13, verbose_name=u'Номер родителя')

    def __unicode__(self):
        return self.fname + " " + self.lname

class Mark(models.Model):
    mark = models.FloatField(verbose_name=u'Оценка', validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    teacher = models.ForeignKey(Teacher, verbose_name=u'Учитель')
    date = models.DateField(verbose_name=u'Дата')
    student = models.ForeignKey(Student, verbose_name=u'Ученик')
    comment = models.TextField(blank=True, verbose_name=u'Комментарий')

    def __unicode__(self):
        return self.student.lname + self.student.fname + ": " + str(self.mark)
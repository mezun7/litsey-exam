# coding=utf-8
from django import forms
from journal.models import Student, Class


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'User', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': u'Password', 'class': 'form-control'}))


class AddMarkForm(forms.Form):
    def __init__(self, class_id, *args, **kwargs):
        super(AddMarkForm, self).__init__(*args, **kwargs)
        self.fields['student'] = forms.ModelChoiceField(
            queryset=Student.objects.filter(class_name=class_id).order_by('fname'),
            widget=forms.Select(attrs={'placeholder': u'Ученик', 'class': 'form-control'}))
        self.fields['mark'] = forms.FloatField(
            widget=forms.NumberInput(attrs={'placeholder': u'Оценка', 'class': 'form-control'}))
        self.fields['comment'] = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': u'Комментарий', 'class': 'form-control'}), required=False)


class StudentForm(forms.Form):
    def __init__(self, student, cls, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['fname'] = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': u'Фамилия', 'class': 'form-control'}), initial=student.fname,
            label=u'Фамилия')
        self.fields['lname'] = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': u'Имя', 'class': 'form-control'}), initial=student.lname,
            label=u'Имя')
        self.fields['fathers_name'] = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': u'Отчество', 'class': 'form-control'}),
            initial=student.fathers_name, label=u'Отчество')
        self.fields['school'] = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': u'Школа', 'class': 'form-control'}), initial=student.school,
            label=u'Школа')
        self.fields['money'] = forms.IntegerField(
            widget=forms.TextInput(attrs={'placeholder': u'Оплата питания', 'class': 'form-control'}),
            initial=student.pay_for_eating, label=u'Оплата питания')
        self.fields['phone-parent'] = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': u'Номер телефона родителя', 'class': 'form-control'}), initial=student.phone_parent,
            label=u'Номер телефона родителя')
        self.fields['phone-child'] = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': u'Номер телефона ребенка', 'class': 'form-control'}),
            initial=student.phone_number,
            label=u'Номер телефона ребенка')

        self.fields['class'] = forms.ModelChoiceField(queryset=Class.objects.all(), initial=cls, label=u'Класс',
                                                      widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['medical'] = forms.BooleanField(initial=student.medical_card, required=False,
                                                    label=u'Медицинская карта')
        self.fields['school-req'] = forms.BooleanField(initial=student.report_from_school, required=False,
                                                       label=u'Справка со школы')


class UploadForm(forms.Form):
    csv_file = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control',
        'accept': '.csv'
    }))

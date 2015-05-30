# coding=utf-8
from django import forms
from journal.models import Student


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'User', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': u'Password', 'class': 'form-control'}))

class AddMarkForm(forms.Form):
    def __init__(self, class_id, *args, **kwargs):
        super(AddMarkForm, self).__init__(*args, **kwargs)
        self.fields['student'] = forms.ModelChoiceField(queryset=Student.objects.filter(class_name=class_id).order_by('fname'), widget=forms.Select(attrs={'placeholder': u'Ученик', 'class': 'form-control'}))
        self.fields['mark'] = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': u'Оценка', 'class': 'form-control'}))
        self.fields['comment'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'Комментарий', 'class': 'form-control'}), required=False)




from django import forms
from journal.models import Student


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'User', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': u'Password', 'class': 'form-control'}))

class AddMarkForm(forms.Form):
    def __init__(self, class_id, *args, **kwargs):
        super(AddMarkForm, self).__init__(*args, **kwargs)
        self.fields['student'] = forms.ModelChoiceField(queryset=Student.objects.filter(class_name=class_id).order_by('fname'))
        self.fields['mark'] = forms.FloatField()



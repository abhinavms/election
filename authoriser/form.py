from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class AuthForm(forms.Form):
    student_no = forms.CharField(label='student_no', widget=forms.TextInput(attrs={'placeholder': 'Admission No'}))
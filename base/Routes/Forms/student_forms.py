from django import forms
from django.contrib.auth.models import User
from ... import models


class StudentUserForm(forms.ModelForm): 
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class StudentForm(forms.ModelForm):

    joinned_year = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    role_no = forms.IntegerField()
    department = forms.ModelChoiceField(queryset=models.Department.objects.all(),
                                        empty_label='Select department',
                                        to_field_name='short_name',
                                        label='Department')

    class Meta:
        model = models.Student
        fields = ['address', 'mobile', 'profile_pic',
                  'joinned_year', 'role_no', 'department','parent_mail_id','mail_id']

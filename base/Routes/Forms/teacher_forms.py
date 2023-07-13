from django import forms
from django.contrib.auth.models import User
from base import models
from base.models import Department


class TeacherUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = models.Teacher
        fields = ['address', 'mobile', 'profile_pic', 'role', 'department']

    ROLE_CHOICES = (
        ('staff', 'Staff'),
        ('hod', 'Hod'),
        ('admin', 'Admin'),
    )
    department = forms.ModelChoiceField(queryset=models.Department.objects.all(),
                                        empty_label='Select department',
                                        to_field_name='short_name',
                                        label='Department')
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}), initial='admin', label='Role')

    

class TeacherFormhod(forms.ModelForm):
    class Meta:
        model = models.Teacher
        fields = ['address', 'mobile', 'profile_pic', 'role', 'department']

    ROLE_CHOICES = (
        ('staff', 'Staff'),
    )
    department = forms.ModelChoiceField(queryset=models.Department.objects.all(),
                                        empty_label='Select department',
                                        to_field_name='short_name',
                                        label='Department')
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}), initial='admin', label='Role')


class TeacherForm1(forms.ModelForm):
    class Meta:
        model = models.Teacher
        fields = ['address', 'mobile', 'profile_pic', 'role', 'department']

    ROLE_CHOICES = (
        ('admin', 'Admin'),
    )
    
    DEPARTMENT_CHOICES = (
        ('', 'Select department'),
        ('admin', 'Admin'),
    )
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES,
                                    label='Department')
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}), initial='admin', label='Role')



class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ('name', 'description', 'short_name')

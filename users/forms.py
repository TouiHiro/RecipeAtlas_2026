from django import forms

class UserForm(forms.Form):
  username = forms.CharField(label="Username", max_length=100)
  password = forms.CharField(label="Password",widget=forms.PasswordInput())

# GeeksforGeeks
# https://www.geeksforgeeks.org/python/how-to-create-a-form-using-django-forms/
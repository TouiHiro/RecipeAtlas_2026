from django import forms

class LoginForm(forms.Form):
  username = forms.CharField(label='ユーザー名', max_length=100)
  password = forms.CharField(label="パスワード", widget=forms.PasswordInput())

  username.widget.attrs.update({"class":"authn_form"})
  password.widget.attrs.update({"class":"authn_form"})


class LogonForm(LoginForm):
  confirm_password = forms.CharField(label="パスワード二回目",widget=forms.PasswordInput())
  confirm_password.widget.attrs.update({"class":"authn_form"})


# GeeksforGeeks
# https://www.geeksforgeeks.org/python/how-to-create-a-form-using-django-forms/
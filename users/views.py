from django.shortcuts import render, redirect
from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
# Create your views here.


def login_page(request):
  template_name = "authn_page.html"
  context = {}
  context['form'] = LoginForm()
  context['page_title'] = 'ログインページ'
  context['submit_button_text'] = 'ログイン'
  context['navigated_page_name'] = 'logon_page'
  context['navigated_link_text'] = f"アカウント作成"

  if not request.method == "POST":
    return render(request, template_name,context=context)

  else:
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    print(f"using username :{request.user.username}")

    if not User.objects.filter(username = username).exists():
      message = 'Invalid Username'
      messages.info(request, message)
      print('\u001b[33mInvalid Password\u001b[0m')
      return render(request, template_name,context=context)

    user = authenticate(username=username, password=password)

    if user is None:
      message = "Invalid Password"
      messages.info(request, message)
      print(f'\u001b[33m{message}\u001b[0m')
      return render(request, template_name,context=context)

    else:
      login(request, user)
      return login_success_test_page(request)



def logon_page(request):
  template_name = "authn_page.html"
  context = {}
  context['form'] = LogonForm()
  context['page_title'] = 'ユーザ登録ページ'
  context['submit_button_text'] = '登録'
  context['navigated_page_name'] = 'login_page'
  context['navigated_link_text'] = f"ログインページへ"

  if not request.method == 'POST':
    return render(request, template_name, context=context)

  else:
    username = request.POST.get('username')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')

    # Check if a user with the provided username already exists
    user = User.objects.filter(username=username)
    if user.exists():
      # Display an information message if the username is taken
      message = "Username already taken!"
      messages.info(request, message)
      print(f'\u001b[33m{message}\u001b[0m')
      return render(request, template_name, context=context)
    
    # Check if both passwords are the same
    if not password == confirm_password:
      message = "password and confirm_password do not match!"
      messages.info(request, message)
      print(f'\u001b[33m{message}\u001b[0m')
      return render(request, template_name, context=context)

    # Create a new User object with the provided information
    user = User.objects.create_user(
        username=username
    )
    
    # Set the user's password and save the user object
    user.set_password(password)
    user.save()
    
    # Display an information message indicating successful account creation
    message = "Account created Successfully!"
    messages.info(request, message)
    print(f'\u001b[33m{message}\u001b[0m')
    return render(request, template_name, context=context)

  

def login_success_test_page(request):
  context={
                      "username":request.user.username,
                      "password":request.user.password,
                      "request_post":request.POST,
                    }
  print(f'\u001b[33mThe login is a success!!!\n{context}\u001b[0m')
  return render(request, 'login_success_test.html',)
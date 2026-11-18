from django.shortcuts import render, redirect
from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import UserForm
# Create your views here.

def render_register_page(request):
  context = {}
  context['form'] = UserForm()
  return render(request, 'register.html',context=context)

def login_page(request):
  """
  loginページに来る方法は今のところ2つ
  
  一つは loginページでのlogin処理に失敗してリダイレクトできたとき or 初回
  POSTでこない if入らない

  ２つ目は loginページ or registerページでsubmitされてきたとき
  POSTでくる (formがPOST method used) から ifぶんのなか入る

    """
  context = {}
  context['form'] = UserForm()
  if request.method =="POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    print(f"using username :{request.user.username}")

    if not User.objects.filter(username = username).exists():
      messages.error(request, 'Invalid Username')
      print('Invalid Username')
      return render(request, 'login.html',context=context)

    user = authenticate(username=username, password=password)

    if user is None:
      messages.error(request, "Invalid Password")
      print('Invalid Password')
      return render(request, 'login.html',context=context)

    else:
      login(request, user)
      print('The login is a success!!!')
      return render(request, 'login_success_test.html',)
    """
    context={
                      "username":request.user.username,
                      "password":request.user.password
                    })
    """

  return render(request, 'login.html',context=context)

# redirectされてloginページにやってきたとき？



def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
        
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('render_register_page')
        
        # Create a new User object with the provided information
        user = User.objects.create_user(
           
            username=username
        )
        
        # Set the user's password and save the user object
        user.set_password(password)
        user.save()
        
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('render_register_page')
    
    return lambda r= request:render_register_page(r)

def test_home(request):
  return render(request,'test_home.html')

from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse  
from .forms import signUpForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):

    return render(request, 'home.html', )


def signup(request):
    form = signUpForm() 
    if request.method == 'POST':  
        form = signUpForm(data = request.POST)  
        if form.is_valid():  
            form.save()  
    context = {  
        'form':form,
    }  
    return render(request, 'signup.html', context)
    
def login_user(request):
    form =AuthenticationForm()
    if request.method == "POST":
        form =AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
            return HttpResponseRedirect(reverse('home')) 
    return render(request,'login.html',context={'form':form})

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
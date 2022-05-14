
from email.message import Message
from django.shortcuts import redirect, render,HttpResponseRedirect
from django.urls import reverse  
from .forms import signUpForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#email send
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

#email varification
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
UserModel=get_user_model()

# Create your views here.

def home(request):

    return render(request, 'home.html', )


def signup(request):
    form = signUpForm() 
    if request.method == 'POST':  
        form = signUpForm(data = request.POST)  
        if form.is_valid():  
            user = form.save(commit=False)
            user.save()
            current_site=get_current_site(request)
            mail_subject='Activate Your Account'
            message=render_to_string('session/account.html',{
                'user':user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail=form.cleaned_data.get('email')
            email=EmailMessage(mail_subject,message, to=[send_mail])
            email.send()
            messages.success(request,'Successfully Created Account')
            messages.info(request,'Activate Your account from the mail you provided')
            return redirect('login')
    context = {  
        'form':form,
    }  
    return render(request, 'signup.html', context)

def activate(request, uidb64, token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=UserModel._default_manager.get(pk=uid)
    except(TypeError,ValueError, OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(request," Your account is activated now, you can now log in")
        return redirect('login')
    else:
        messages.warning(request, "activation link is invalid")
        return redirect('signup')

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
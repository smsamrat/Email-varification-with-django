
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views
import session
urlpatterns = [
   path('',views.home, name='home'),
   path('signup/',views.signup, name='signup'),
   path('login/',views.login_user, name='login'),
   path('logout/',views.logout_user, name='logout'),
   #verification url
   path('activate/<uidb64>/<token>/',views.activate,name="activate"),


   #password reset url
   path('reset/password/',PasswordResetView.as_view(template_name = 'session/reset_pass.html'), name='password_reset'),
   path('reset/password/done/',PasswordResetDoneView.as_view(template_name = 'session/reset_pass_done.html'), name='password_reset_done'),
   path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name = 'session/password_reset_confirm.html'), name='password_reset_confirm'),
   path('reset/done/',PasswordResetCompleteView.as_view(template_name = 'session/password_reset_complete.html'), name='password_reset_complete'),
]
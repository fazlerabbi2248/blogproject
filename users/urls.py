from django.contrib.auth import views
from django.urls import path
from users.views import *
from .import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('emailsend/',emailsend.as_view()),
    path('register/',RegisterApiview.as_view()),
    path('login/',UserLoginView.as_view()),
    path('profiledetails/',UserProfileView.as_view()),
    path('passwordchange/',UserChangePasswordView.as_view()),
    path('password-reset-email-send/',SendPasswordResetEmailView.as_view()),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('sign_up/', views.sign_up, name='users-sign-up'),
    path('profile/', views.profile, name='users-profile'),
    path('', auth_view.LoginView.as_view(template_name='users/login.html'),
         name='users-login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'),
         name='users-logout'),
    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password_reset_done/',
         auth_view.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_view.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_view.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),


]
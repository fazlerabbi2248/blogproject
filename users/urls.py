from django.urls import path
from .import views
from django.contrib.auth import views as auth_view
from users.views import UserRegistrationView,UserLoginView,UserProfileView

urlpatterns = [
    path('sign_up/', views.sign_up, name='users-sign-up'),
    path('profile/', views.profile, name='users-profile'),
    path('', auth_view.LoginView.as_view(template_name='users/login.html'),
         name='users-login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'),
         name='users-logout'),
    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('register/',UserRegistrationView.as_view(),name='registerApi'),
    path('loginapi/',UserLoginView.as_view(),name='loginApi'),
    path('profileapi/',UserProfileView.as_view(),name='profileApi'),

]

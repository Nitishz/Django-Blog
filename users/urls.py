from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    login_view,
    register_view,
    token_send,
    success,
    verify,
    error_page,
    logout_view,
    password_reset_request,
    profile,
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('token', token_send, name='token_send'),
    path('success', success, name='success'),
    path('verify/<auth_token>', verify, name='verify'),
    path('error', error_page, name='error'),
    path('login/', login_view, name='login'),
    path('profile/<str:slug>', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path("password_reset", password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
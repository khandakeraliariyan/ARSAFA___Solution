from django.urls import path
from .views import custom_login, admin_dashboard, custom_login_redirect, logout_view

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-login/', custom_login_redirect, name='legacy_admin_login'),
    path('logout/', logout_view, name='logout'),
] 

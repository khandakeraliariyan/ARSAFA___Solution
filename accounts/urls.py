from django.urls import path

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-login/', custom_login_redirect, name='legacy_admin_login'),
    path('logout/', logout_view, name='logout'),
] 

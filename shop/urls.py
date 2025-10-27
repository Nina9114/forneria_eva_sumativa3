from django.urls import path
from . import views

app_name = 'forneria'

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards
    path('', views.dashboard_admin, name='dashboard_admin'),
    path('vendedor/', views.dashboard_vendedor, name='dashboard_vendedor'),
    
    # Sesiones
    path('session-info/', views.session_info, name='session_info'),
    path('clear-session/', views.clear_session_data, name='clear_session'),
]

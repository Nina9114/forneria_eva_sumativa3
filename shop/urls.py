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
    
    # CRUD Productos
    path('productos/', views.productos_list, name='productos_list'),
    path('productos/crear/', views.productos_create, name='productos_create'),
    path('productos/<int:producto_id>/', views.productos_detail, name='productos_detail'),
    path('productos/<int:producto_id>/editar/', views.productos_edit, name='productos_edit'),
    path('productos/<int:producto_id>/eliminar/', views.productos_delete, name='productos_delete'),
]
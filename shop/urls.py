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
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/hecho/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/enviado/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirmar/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/completado/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('perfil/', views.profile_view, name='perfil'),
    path('clear-session/', views.clear_session_data, name='clear_session'),
    
    # CRUD Productos
    path('productos/', views.productos_list, name='productos_list'),
    path('productos/crear/', views.productos_create, name='productos_create'),
    path('productos/<int:producto_id>/', views.productos_detail, name='productos_detail'),
    path('productos/<int:producto_id>/editar/', views.productos_edit, name='productos_edit'),
    path('productos/<int:producto_id>/eliminar/', views.productos_delete, name='productos_delete'),

    # CRUD Ventas
    path('ventas/', views.ventas_list, name='ventas_list'),
    path('ventas/crear/', views.ventas_create, name='ventas_create'),
    path('ventas/<int:venta_id>/', views.ventas_detail, name='ventas_detail'),
    path('ventas/<int:venta_id>/editar/', views.ventas_edit, name='ventas_edit'),
    path('ventas/<int:venta_id>/eliminar/', views.ventas_delete, name='ventas_delete'),
]

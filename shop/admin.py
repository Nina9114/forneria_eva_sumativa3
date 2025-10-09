"""
Configuración del Django Admin para Fornería
Incluye: Admin Básico + Admin Pro (Inline, Acción Personalizada, Validaciones)
"""

from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User
from .models import (
    Direccion, Roles, Clientes, Categorias, Nutricional,
    Productos, Ventas, Detalle_Venta, Movimientos_Inventario,
    Alertas, Usuarios
)


# ============= ADMIN BÁSICO - TABLAS MAESTRAS =============

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    """Admin para Direcciones - Tabla Maestra"""
    list_display = ('id', 'calle', 'numero', 'depto', 'comuna', 'region', 'codigo_postal', 'created_at')
    search_fields = ('calle', 'numero', 'comuna', 'region')
    list_filter = ('region', 'comuna', 'created_at')
    ordering = ('-created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Información de Dirección', {
            'fields': ('calle', 'numero', 'depto', 'comuna', 'region', 'codigo_postal')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    """Admin para Roles - Tabla Maestra"""
    list_display = ('id', 'nombre', 'descripcion', 'created_at', 'updated_at')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('created_at', 'updated_at')
    ordering = ('nombre',)
    list_per_page = 25
    
    fieldsets = (
        ('Información del Rol', {
            'fields': ('nombre', 'descripcion')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    """Admin para Clientes - Tabla Maestra"""
    list_display = ('id', 'nombre', 'rut', 'correo', 'created_at')
    search_fields = ('nombre', 'rut', 'correo')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('nombre', 'rut', 'correo')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Categorias)
class CategoriasAdmin(admin.ModelAdmin):
    """Admin para Categorías - Tabla Maestra"""
    list_display = ('id', 'nombre', 'descripcion', 'created_at')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('created_at', 'updated_at')
    ordering = ('nombre',)
    list_per_page = 25
    
    fieldsets = (
        ('Información de Categoría', {
            'fields': ('nombre', 'descripcion')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Nutricional)
class NutricionalAdmin(admin.ModelAdmin):
    """Admin para Información Nutricional - Tabla Maestra"""
    list_display = ('id', 'calorias', 'proteinas', 'grasas', 'carbohidratos', 'azucares', 'sodio', 'created_at')
    search_fields = ('id',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Información Nutricional (por 100g)', {
            'fields': ('calorias', 'proteinas', 'grasas', 'carbohidratos', 'azucares', 'sodio')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    """Admin para Productos - Tabla Maestra"""
    list_display = ('id', 'nombre', 'precio_formatted', 'stock_actual', 'stock_status', 
                   'caducidad', 'Categorias_id', 'tipo', 'creado')
    search_fields = ('nombre', 'marca', 'descripcion', 'tipo')
    list_filter = ('Categorias_id', 'tipo', 'caducidad', 'creado')
    ordering = ('-creado',)
    list_select_related = ('Categorias_id', 'Nutricional_id')
    list_per_page = 25
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'marca', 'Categorias_id')
        }),
        ('Precios y Stock', {
            'fields': ('precio', 'stock_actual', 'stock_minimo', 'stock_maximo')
        }),
        ('Fechas y Tipo', {
            'fields': ('tipo', 'elaboracion', 'caducidad')
        }),
        ('Presentación', {
            'fields': ('presentacion', 'formato')
        }),
        ('Información Nutricional', {
            'fields': ('Nutricional_id',)
        }),
        ('Timestamps', {
            'fields': ('creado', 'modificado', 'eliminado'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('creado', 'modificado')
    
    def precio_formatted(self, obj):
        """Formato de precio en pesos chilenos"""
        return f"${obj.precio:,.0f}".replace(",", ".")
    precio_formatted.short_description = 'Precio'
    precio_formatted.admin_order_field = 'precio'
    
    def stock_status(self, obj):
        """Indicador visual del estado del stock"""
        if obj.stock_actual is None:
            return format_html('<span style="color: gray;">Sin stock</span>')
        if obj.stock_actual <= obj.stock_minimo:
            return format_html(
                '<span style="background-color: #ff5252; color: white; padding: 3px 8px; '
                'border-radius: 3px; font-weight: bold;">⚠ BAJO</span>'
            )
        elif obj.stock_actual >= obj.stock_maximo:
            return format_html(
                '<span style="background-color: #4caf50; color: white; padding: 3px 8px; '
                'border-radius: 3px;">✓ ALTO</span>'
            )
        return format_html(
            '<span style="background-color: #ff9800; color: white; padding: 3px 8px; '
            'border-radius: 3px;">→ NORMAL</span>'
        )
    stock_status.short_description = 'Estado Stock'


# ============= ADMIN PRO - INLINE =============

class DetalleVentaInline(admin.TabularInline):
    """
    Inline para Detalle de Venta dentro de Ventas
    Permite agregar/editar items de venta directamente en el formulario de venta
    """
    model = Detalle_Venta
    extra = 1
    min_num = 1
    fields = ('producto_id', 'cantidad', 'precio_unitario', 'descuento_pct', 'subtotal_display')
    readonly_fields = ('subtotal_display',)
    autocomplete_fields = ['producto_id']
    
    def subtotal_display(self, obj):
        """Muestra el subtotal calculado del item"""
        if obj.id and obj.cantidad and obj.precio_unitario:
            descuento_pct = obj.descuento_pct or 0
            subtotal = obj.cantidad * obj.precio_unitario * (1 - descuento_pct / 100)
            return format_html(
                '<strong style="color: #4caf50;">${:,.0f}</strong>',
                subtotal
            ).replace(",", ".")
        return "$0"
    subtotal_display.short_description = 'Subtotal'


# ============= ADMIN BÁSICO - TABLAS OPERATIVAS =============

@admin.register(Ventas)
class VentasAdmin(admin.ModelAdmin):
    """Admin para Ventas - Tabla Operativa"""
    list_display = ('id', 'folio', 'fecha', 'cliente_id', 'total_formatted', 
                   'canal_venta', 'estado_display', 'created_at')
    search_fields = ('folio', 'cliente_id__nombre', 'cliente_id__rut')
    list_filter = ('canal_venta', 'fecha', 'created_at')
    ordering = ('-fecha',)
    list_select_related = ('cliente_id',)
    inlines = [DetalleVentaInline]
    list_per_page = 25
    
    fieldsets = (
        ('Información de Venta', {
            'fields': ('folio', 'fecha', 'cliente_id', 'canal_venta')
        }),
        ('Totales', {
            'fields': ('total_sin_iva', 'total_iva', 'descuento', 'total_con_iva')
        }),
        ('Pago', {
            'fields': ('monto_pagado', 'vuelto')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def total_formatted(self, obj):
        """Formato del total con IVA"""
        return f"${obj.total_con_iva:,.0f}".replace(",", ".")
    total_formatted.short_description = 'Total'
    total_formatted.admin_order_field = 'total_con_iva'
    
    def estado_display(self, obj):
        """Estado visual de la venta"""
        if obj.deleted_at:
            return format_html('<span style="color: red;">❌ Anulada</span>')
        return format_html('<span style="color: green;">✓ Activa</span>')
    estado_display.short_description = 'Estado'
    
    def has_delete_permission(self, request, obj=None):
        """
        Restricción de seguridad: 
        Los vendedores NO pueden eliminar ventas
        """
        if request.user.groups.filter(name='Vendedor').exists():
            return False
        return super().has_delete_permission(request, obj)


@admin.register(Detalle_Venta)
class DetalleVentaAdmin(admin.ModelAdmin):
    """Admin para Detalle de Venta - Tabla Operativa"""
    list_display = ('id', 'venta_id', 'producto_id', 'cantidad', 'precio_unitario', 
                   'descuento_pct', 'subtotal_display')
    search_fields = ('venta_id__folio', 'producto_id__nombre')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_select_related = ('venta_id', 'producto_id')
    list_per_page = 25
    
    readonly_fields = ('subtotal_display', 'created_at', 'updated_at')
    
    def subtotal_display(self, obj):
        """Muestra el subtotal del item"""
        if obj.subtotal is not None:
            return f"${obj.subtotal:,.0f}".replace(",", ".")
        return "$0"
    subtotal_display.short_description = 'Subtotal'


@admin.register(Movimientos_Inventario)
class MovimientosInventarioAdmin(admin.ModelAdmin):
    """Admin para Movimientos de Inventario - Tabla Operativa"""
    list_display = ('id', 'producto_id', 'tipo_movimiento', 'cantidad', 'fecha', 'created_at')
    search_fields = ('producto_id__nombre',)
    list_filter = ('tipo_movimiento', 'fecha', 'created_at')
    ordering = ('-fecha',)
    list_select_related = ('producto_id',)
    list_per_page = 25
    
    fieldsets = (
        ('Información del Movimiento', {
            'fields': ('producto_id', 'tipo_movimiento', 'cantidad', 'fecha')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def has_module_permission(self, request):
        """
        Restricción de seguridad:
        Solo administradores pueden ver movimientos de inventario
        """
        if request.user.groups.filter(name='Vendedor').exists():
            return False
        return super().has_module_permission(request)


# ============= ADMIN PRO - ACCIÓN PERSONALIZADA =============

def mark_alerts_as_resolved(modeladmin, request, queryset):
    """
    Acción personalizada: Marcar alertas seleccionadas como atendidas
    Permite resolver múltiples alertas de una sola vez
    """
    updated = queryset.filter(estado='pendiente').update(estado='atendida')
    if updated == 1:
        message = '1 alerta fue marcada como atendida.'
    else:
        message = f'{updated} alertas fueron marcadas como atendidas.'
    modeladmin.message_user(request, message)

mark_alerts_as_resolved.short_description = "✓ Marcar alertas seleccionadas como atendidas"


@admin.register(Alertas)
class AlertasAdmin(admin.ModelAdmin):
    """Admin para Alertas - Tabla Operativa con Acción Personalizada"""
    list_display = ('id', 'producto_id', 'tipo_alerta', 'estado_badge', 'mensaje', 'fecha_generada')
    search_fields = ('producto_id__nombre', 'mensaje')
    list_filter = ('tipo_alerta', 'estado', 'fecha_generada')
    ordering = ('-fecha_generada',)
    list_select_related = ('producto_id',)
    actions = [mark_alerts_as_resolved]
    list_per_page = 25
    
    fieldsets = (
        ('Información de la Alerta', {
            'fields': ('producto_id', 'tipo_alerta', 'mensaje', 'estado')
        }),
        ('Fechas', {
            'fields': ('fecha_generada',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'fecha_generada')
    
    def estado_badge(self, obj):
        """Badge visual para el estado de la alerta"""
        if obj.estado == 'pendiente':
            return format_html(
                '<span style="background-color: #ff9800; color: white; padding: 3px 10px; '
                'border-radius: 3px; font-weight: bold;">⚠ PENDIENTE</span>'
            )
        return format_html(
            '<span style="background-color: #4caf50; color: white; padding: 3px 10px; '
            'border-radius: 3px;">✓ ATENDIDA</span>'
        )
    estado_badge.short_description = 'Estado'
    
    def has_module_permission(self, request):
        """
        Restricción de seguridad:
        Solo administradores pueden ver alertas
        """
        if request.user.groups.filter(name='Vendedor').exists():
            return False
        return super().has_module_permission(request)


@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    """Admin para Usuarios del Sistema"""
    list_display = ('id', 'nombres', 'paterno', 'materno', 'run', 'correo', 
                   'Roles_id', 'Direccion_id', 'fono', 'created_at')
    search_fields = ('nombres', 'paterno', 'materno', 'run', 'correo')
    list_filter = ('Roles_id', 'Direccion_id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_select_related = ('Direccion_id', 'Roles_id')
    list_per_page = 25
    autocomplete_fields = ['Direccion_id', 'Roles_id']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombres', 'paterno', 'materno', 'run')
        }),
        ('Contacto', {
            'fields': ('correo', 'fono', 'Direccion_id')
        }),
        ('Sistema', {
            'fields': ('Roles_id', 'clave')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def has_module_permission(self, request):
        """
        Restricción de seguridad:
        Solo administradores pueden ver usuarios
        """
        if request.user.groups.filter(name='Vendedor').exists():
            return False
        return super().has_module_permission(request)


# Personalización del sitio de administración
admin.site.site_header = "Administración Fornería"
admin.site.site_title = "Fornería Admin"
admin.site.index_title = "Panel de Administración"


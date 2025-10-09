"""
Modelos para la aplicación de gestión de Fornería
Incluye 6 tablas maestras y 5 tablas operativas
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal


class Direccion(models.Model):
    """
    Tabla Maestra: Direcciones
    Almacena direcciones físicas para usuarios
    """
    calle = models.CharField(max_length=100, verbose_name='Calle')
    numero = models.CharField(max_length=10, verbose_name='Número')
    depto = models.CharField(max_length=10, blank=True, null=True, verbose_name='Departamento')
    comuna = models.CharField(max_length=100, verbose_name='Comuna')
    region = models.CharField(max_length=100, verbose_name='Región')
    codigo_postal = models.CharField(max_length=45, blank=True, null=True, verbose_name='Código Postal')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha Modificación')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Eliminación')

    class Meta:
        db_table = 'Direccion'
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.calle} {self.numero}, {self.comuna}"


class Roles(models.Model):
    """
    Tabla Maestra: Roles de usuario
    Define roles: Administrador, Vendedor
    """
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.CharField(max_length=200, blank=True, null=True, verbose_name='Descripción')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha Modificación')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Eliminación')

    class Meta:
        db_table = 'Roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Clientes(models.Model):
    """
    Tabla Maestra: Clientes
    Información de clientes de la fornería
    """
    rut = models.CharField(max_length=12, unique=True, blank=True, null=True, verbose_name='RUT')
    nombre = models.CharField(max_length=150, verbose_name='Nombre')
    correo = models.EmailField(max_length=100, blank=True, null=True, verbose_name='Correo Electrónico')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha Modificación')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Eliminación')

    class Meta:
        db_table = 'Clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-created_at']

    def __str__(self):
        return self.nombre


class Categorias(models.Model):
    """
    Tabla Maestra: Categorías de productos
    Pan, Pasteles, Galletas, Bebidas, etc.
    """
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.CharField(max_length=200, blank=True, null=True, verbose_name='Descripción')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha Modificación')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Eliminación')

    class Meta:
        db_table = 'Categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Nutricional(models.Model):
    """
    Tabla Maestra: Información nutricional
    Datos nutricionales por cada producto
    """
    calorias = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Calorías')
    proteinas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Proteínas (g)')
    grasas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Grasas (g)')
    carbohidratos = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Carbohidratos (g)')
    azucares = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Azúcares (g)')
    sodio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Sodio (mg)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha Modificación')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Eliminación')

    class Meta:
        db_table = 'Nutricional'
        verbose_name = 'Información Nutricional'
        verbose_name_plural = 'Información Nutricional'
        ordering = ['-created_at']

    def __str__(self):
        return f"Calorías: {self.calorias if self.calorias else 0} kcal"


class Productos(models.Model):
    """
    Tabla Maestra: Productos de la fornería
    Catálogo completo de productos con stock y precios
    """
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.CharField(max_length=300, blank=True, null=True, verbose_name='Descripción')
    marca = models.CharField(max_length=100, blank=True, null=True, verbose_name='Marca')
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio (sin IVA)')
    caducidad = models.DateField(verbose_name='Fecha Caducidad')
    elaboracion = models.DateField(blank=True, null=True, verbose_name='Fecha Elaboración')
    tipo = models.CharField(max_length=100, verbose_name='Tipo', 
                           help_text='Tipo de elaboración: propia o envasado')
    Categorias_id = models.ForeignKey(Categorias, on_delete=models.PROTECT, 
                                      db_column='Categorias_id', verbose_name='Categoría')
    stock_actual = models.IntegerField(null=True, blank=True, default=0, verbose_name='Stock Actual')
    stock_minimo = models.IntegerField(null=True, blank=True, default=5, verbose_name='Stock Mínimo')
    stock_maximo = models.IntegerField(null=True, blank=True, default=100, verbose_name='Stock Máximo')
    presentacion = models.CharField(max_length=100, blank=True, null=True, 
                                    verbose_name='Presentación',
                                    help_text='Unidad de almacenamiento')
    formato = models.CharField(max_length=100, blank=True, null=True, 
                              verbose_name='Formato',
                              help_text='Cantidad por presentación')
    Nutricional_id = models.ForeignKey(Nutricional, on_delete=models.PROTECT, 
                                       db_column='Nutricional_id', verbose_name='Info. Nutricional')
    creado = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')
    modificado = models.DateTimeField(auto_now=True, verbose_name='Fecha Modificación')
    eliminado = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Eliminación')

    class Meta:
        db_table = 'Productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-creado']

    def __str__(self):
        return self.nombre

    def clean(self):
        """
        Validación personalizada (Admin Pro):
        - La fecha de caducidad debe ser posterior a la fecha de elaboración
        """
        if self.elaboracion and self.caducidad:
            if self.caducidad <= self.elaboracion:
                raise ValidationError({
                    'caducidad': 'La fecha de caducidad debe ser posterior a la fecha de elaboración.'
                })
        
        # Validar que el stock actual no sea negativo
        if self.stock_actual is not None and self.stock_actual < 0:
            raise ValidationError({
                'stock_actual': 'El stock actual no puede ser negativo.'
            })


class Ventas(models.Model):
    """
    Tabla Operativa: Ventas realizadas
    Registro de transacciones de venta
    """
    CANAL_CHOICES = [
        ('Local', 'Local'),
        ('UberEats', 'UberEats'),
        ('Instagram', 'Instagram'),
        ('WhatsApp', 'WhatsApp'),
    ]
    
    fecha = models.DateTimeField(default=timezone.now, verbose_name='Fecha')
    cliente_id = models.ForeignKey(Clientes, on_delete=models.PROTECT, 
                                   db_column='cliente_id', verbose_name='Cliente')
    total_sin_iva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total sin IVA')
    total_iva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='IVA (19%)')
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Descuento')
    total_con_iva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total con IVA')
    canal_venta = models.CharField(max_length=20, choices=CANAL_CHOICES, default='Local', verbose_name='Canal de Venta')
    folio = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name='Folio')
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Monto Pagado')
    vuelto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Vuelto')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha Modificación')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Eliminación')

    class Meta:
        db_table = 'Ventas'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-fecha']

    def __str__(self):
        return f"Venta {self.folio or self.id} - {self.fecha.strftime('%d/%m/%Y')}"


class Detalle_Venta(models.Model):
    """
    Tabla Operativa: Detalle de cada venta
    Items individuales de cada transacción
    """
    venta_id = models.ForeignKey(Ventas, on_delete=models.CASCADE, 
                                 db_column='venta_id', related_name='detalles', verbose_name='Venta')
    producto_id = models.ForeignKey(Productos, on_delete=models.PROTECT, 
                                    db_column='producto_id', verbose_name='Producto')
    cantidad = models.IntegerField(verbose_name='Cantidad')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio Unitario')
    descuento_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, 
                                        verbose_name='Descuento (%)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha Modificación')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Eliminación')

    class Meta:
        db_table = 'Detalle_Venta'
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Venta'
        ordering = ['venta_id', 'id']

    def __str__(self):
        if self.producto_id and self.cantidad:
            return f"{self.producto_id.nombre} x {self.cantidad}"
        return f"Detalle de Venta {self.id or 'Nuevo'}"

    @property
    def subtotal(self):
        """Calcula el subtotal del item con descuento aplicado"""
        if self.cantidad is None or self.precio_unitario is None:
            return 0
        subtotal_base = self.cantidad * self.precio_unitario
        if self.descuento_pct is None:
            return subtotal_base
        descuento = subtotal_base * (self.descuento_pct / 100)
        return subtotal_base - descuento


class Movimientos_Inventario(models.Model):
    """
    Tabla Operativa: Movimientos de inventario
    Registro de entradas, salidas y ajustes de stock
    """
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste'),
    ]
    
    producto_id = models.ForeignKey(Productos, on_delete=models.PROTECT, 
                                    db_column='producto_id', verbose_name='Producto')
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo de Movimiento')
    cantidad = models.IntegerField(verbose_name='Cantidad')
    fecha = models.DateTimeField(default=timezone.now, verbose_name='Fecha')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha Modificación')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Eliminación')

    class Meta:
        db_table = 'Movimientos_Inventario'
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.get_tipo_movimiento_display()} - {self.producto_id.nombre} ({self.cantidad})"


class Alertas(models.Model):
    """
    Tabla Operativa: Alertas de stock y vencimiento
    Sistema de notificaciones para administración
    """
    TIPO_CHOICES = [
        ('Stock bajo', 'Stock bajo'),
        ('Vencimiento próximo', 'Vencimiento próximo'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('atendida', 'Atendida'),
    ]
    
    producto_id = models.ForeignKey(Productos, on_delete=models.CASCADE, 
                                    db_column='producto_id', verbose_name='Producto')
    tipo_alerta = models.CharField(max_length=30, choices=TIPO_CHOICES, verbose_name='Tipo de Alerta')
    mensaje = models.CharField(max_length=255, verbose_name='Mensaje')
    fecha_generada = models.DateTimeField(default=timezone.now, verbose_name='Fecha Generación')
    estado = models.CharField(max_length=20, default='pendiente', choices=ESTADO_CHOICES,
                             verbose_name='Estado',
                             help_text='Estado de la alerta: pendiente o atendida')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha Modificación')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Eliminación')

    class Meta:
        db_table = 'Alertas'
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        ordering = ['-fecha_generada']

    def __str__(self):
        return f"{self.get_tipo_alerta_display()} - {self.producto_id.nombre}"


class Usuarios(models.Model):
    """
    Tabla: Usuarios del sistema
    Personal de la fornería con roles asignados
    """
    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    paterno = models.CharField(max_length=100, verbose_name='Apellido Paterno')
    materno = models.CharField(max_length=100, blank=True, null=True, verbose_name='Apellido Materno')
    run = models.CharField(max_length=12, unique=True, verbose_name='RUN')
    correo = models.EmailField(max_length=100, verbose_name='Correo Electrónico')
    fono = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    clave = models.CharField(max_length=150, blank=True, null=True, verbose_name='Clave')
    Direccion_id = models.ForeignKey(Direccion, on_delete=models.PROTECT, 
                                     db_column='Direccion_id', verbose_name='Dirección')
    Roles_id = models.ForeignKey(Roles, on_delete=models.PROTECT, 
                                 db_column='Roles_id', verbose_name='Rol')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha Modificación')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Eliminación')

    class Meta:
        db_table = 'Usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nombres} {self.paterno}"


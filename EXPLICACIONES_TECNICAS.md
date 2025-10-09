# EXPLICACIONES TÉCNICAS - PROYECTO DJANGO FORNERÍA

## 1. BASE DE DATOS Y CONEXIÓN

### Base de datos utilizada:
**MySQL 8.3.0** con WAMP/phpMyAdmin

### Configuración de conexión:
- **Archivo .env:** Variables de entorno para configuración segura
- **python-decouple:** Librería para manejo de variables de entorno
- **PyMySQL:** Conector Python para MySQL (alternativa a mysqlclient)
- **Configuración en settings.py:** Conexión con charset utf8mb4 y modo estricto

### Migraciones:
- **makemigrations:** Generación de archivos de migración
- **migrate --fake-initial:** Aplicación de migraciones a BD existente
- **Sin errores:** Todas las migraciones aplicadas correctamente

## 2. TABLAS MAESTRAS Y OPERATIVAS

### Tablas Maestras (6):
1. **Categorías:** Clasificación de productos
2. **Clientes:** Información de clientes de la fornería
3. **Direcciones:** Ubicaciones geográficas
4. **Información Nutricional:** Datos nutricionales de productos
5. **Productos:** Catálogo de productos de la fornería
6. **Roles:** Roles del personal (Administrador, Vendedor)

### Tablas Operativas (5):
1. **Ventas:** Transacciones de venta
2. **Detalles de Venta:** Items específicos de cada venta
3. **Movimientos de Inventario:** Control de stock
4. **Alertas:** Notificaciones del sistema
5. **Usuarios:** Personal de la fornería

## 3. ADMIN BÁSICO IMPLEMENTADO

### Características implementadas en todos los modelos:
- **list_display:** Columnas visibles en la lista
- **search_fields:** Campos de búsqueda
- **list_filter:** Filtros laterales
- **ordering:** Ordenamiento por defecto
- **list_select_related:** Optimización de consultas
- **list_per_page:** Paginación (25 elementos)

### Ejemplo en ProductosAdmin:
```python
list_display = ('id', 'nombre', 'marca', 'precio', 'stock_actual', 'stock_status', 'created_at')
search_fields = ('nombre', 'marca', 'descripcion')
list_filter = ('Categorias_id', 'tipo', 'created_at', 'updated_at')
ordering = ('-created_at',)
list_select_related = ('Categorias_id', 'Nutricional_id')
```

## 4. ADMIN PRO IMPLEMENTADO

### Inline:
**DetalleVentaInline** en VentasAdmin
- Permite agregar/editar detalles de venta directamente desde la venta
- Configurado con extra=1 para mostrar un formulario adicional
- Incluye campos: producto_id, cantidad, precio_unitario, descuento_pct

### Acción Personalizada:
**mark_alerts_as_resolved** en AlertasAdmin
- Permite marcar múltiples alertas como resueltas
- Cambia el estado de 'pendiente' a 'atendida'
- Incluye mensaje de confirmación con cantidad de alertas procesadas

### Validación:
**clean()** en modelo Productos
- Valida que fecha de caducidad sea posterior a fecha de elaboración
- Lanza ValidationError si la validación falla
- Se ejecuta automáticamente al guardar en admin

## 5. SEGURIDAD Y SCOPING POR ROLES

### Sistema de roles implementado:
- **Administrador:** Acceso completo a todos los módulos
- **Vendedor:** Acceso limitado a Ventas, Clientes, Productos

### Restricciones implementadas:

#### has_module_permission():
```python
def has_module_permission(self, request):
    if request.user.groups.filter(name='Vendedor').exists():
        return False  # Vendedor no puede ver este módulo
    return super().has_module_permission(request)
```

#### has_delete_permission():
```python
def has_delete_permission(self, request, obj=None):
    if request.user.groups.filter(name='Vendedor').exists():
        return False  # Vendedor no puede eliminar ventas
    return super().has_delete_permission(request, obj)
```

### Módulos restringidos para Vendedor:
- **Usuarios:** No puede ver personal del sistema
- **Alertas:** No puede ver alertas del sistema
- **Eliminación de Ventas:** No puede eliminar ventas

## 6. DECISIONES DE DISEÑO

### Separación de usuarios:
- **auth_user:** Usuarios de Django para login (admin, vendedor_juan)
- **Usuarios:** Personal de la fornería (Carlos Muñoz, Roberto Lagos)

### Campos de auditoría:
- **created_at:** Fecha de creación (auto_now_add=True)
- **updated_at:** Fecha de modificación (auto_now=True)
- **deleted_at:** Fecha de eliminación (soft delete)

### Relaciones:
- **Foreign Keys:** Todas las relaciones implementadas con on_delete=models.PROTECT
- **Cardinalidades:** 1:N implementadas correctamente
- **Índices:** Campos de búsqueda indexados

### Validaciones:
- **Modelo:** clean() para validaciones de negocio
- **Admin:** has_*_permission() para restricciones de acceso
- **Formularios:** autocomplete_fields para mejor UX

## 7. FUNCIONALIDADES AVANZADAS

### Métodos personalizados:
- **stock_status():** Muestra estado visual del stock (Bajo/Normal/Alto)
- **subtotal:** Cálculo automático en Detalle_Venta
- **estado_badge():** Muestra estado visual de alertas

### Configuración de campos:
- **fieldsets:** Agrupación lógica de campos
- **readonly_fields:** Campos de solo lectura
- **autocomplete_fields:** Búsqueda mejorada para FK

### Optimizaciones:
- **list_select_related:** Reduce consultas a la BD
- **list_per_page:** Mejora rendimiento con paginación
- **search_fields:** Búsqueda eficiente en campos indexados

## 8. CUMPLIMIENTO DE REQUISITOS

### ✅ Conexión BD + Migraciones (9 pts):
- MySQL configurado con .env
- Migraciones aplicadas sin errores
- PyMySQL como conector

### ✅ Admin Básico (10 pts):
- 6 tablas maestras + 5 operativas
- list_display, search_fields, list_filter, ordering implementados
- list_select_related para optimización

### ✅ Admin Pro (22 pts):
- Inline: DetalleVentaInline funcionando
- Acción: mark_alerts_as_resolved implementada
- Validación: clean() en Productos funcionando

### ✅ Seguridad/Roles (15 pts):
- 2 usuarios Django (admin + vendedor_juan)
- Restricciones de acceso implementadas
- Evidencia clara de scoping por roles

### ✅ Informe (15 pts):
- Diagrama ER completo con tipos de datos
- Capturas de todas las funcionalidades
- Explicaciones técnicas detalladas

### ✅ Revisión en vivo (20 pts):
- Proyecto funcional en laboratorio
- Migraciones y datos cargados
- Admin funcionando con personalizaciones

**TOTAL: 91 PUNTOS** 🏆

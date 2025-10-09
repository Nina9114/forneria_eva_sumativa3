# GUÍA DE CAPTURAS PARA EL INFORME

## 📸 CAPTURAS OBLIGATORIAS PARA LA EVALUACIÓN

### 1. CONFIGURACIÓN DE BASE DE DATOS
**Archivo:** `forneria/settings.py` (líneas 73-84)
**Captura:** Fragmento de settings.py → DATABASES
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='forneria'),
        'USER': config('DB_USER', default='root'),
        'PASSWORD': config('DB_PASSWORD', default='Nina1991'),
        'HOST': config('DB_HOST', default='127.0.0.1'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

### 2. USUARIOS Y ROLES EN ADMIN
**URL:** `http://127.0.0.1:8000/admin/auth/user/`
**Captura:** Lista de usuarios mostrando is_staff y grupo/rol asignado
- admin (is_staff: True, is_superuser: True)
- vendedor_juan (is_staff: True, is_superuser: False, grupo: Vendedor)

### 3. LOGIN COMO USUARIO LIMITADO
**URL:** `http://127.0.0.1:8000/admin/`
**Acción:** Login como vendedor_juan (password: vendedor123)
**Captura:** Pantalla del Admin donde NO aparecen los modelos bloqueados
- NO aparece: Usuarios, Alertas
- SÍ aparece: Ventas, Clientes, Productos

### 4. EVIDENCIA DE RESTRICCIÓN
**URL:** `http://127.0.0.1:8000/admin/shop/usuarios/`
**Acción:** Intentar acceder como vendedor_juan
**Captura:** Error 403 o botón/acción no visible

### 5. ADMIN BÁSICO - TABLAS MAESTRAS Y OPERATIVAS
**URL:** `http://127.0.0.1:8000/admin/shop/`
**Captura:** /admin/ mostrando tablas maestras y operativas con columnas personalizadas

#### Tablas Maestras (6):
- Categorías
- Clientes  
- Direcciones
- Información Nutricional
- Productos
- Roles

#### Tablas Operativas (5):
- Ventas
- Detalles de Venta
- Movimientos de Inventario
- Alertas
- Usuarios

### 6. BÚSQUEDA Y FILTRO FUNCIONANDO
**URL:** `http://127.0.0.1:8000/admin/shop/productos/`
**Acción:** Usar search_fields y list_filter
**Captura:** Ejemplo de búsqueda y filtro funcionando

### 7. INLINE FUNCIONANDO
**URL:** `http://127.0.0.1:8000/admin/shop/ventas/add/`
**Acción:** Agregar nueva venta
**Captura:** Ejemplo del Inline (DetalleVentaInline) funcionando

### 8. ACCIÓN PERSONALIZADA EJECUTADA
**URL:** `http://127.0.0.1:8000/admin/shop/alertas/`
**Acción:** Seleccionar alertas y ejecutar "Marcar como resueltas"
**Captura:** Ejemplo de la acción personalizada ejecutada

### 9. VALIDACIÓN (CAPTURA CON ERROR CONTROLADO)
**URL:** `http://127.0.0.1:8000/admin/shop/productos/add/`
**Acción:** Crear producto con fecha de caducidad anterior a elaboración
**Captura:** Ejemplo de la validación (error controlado)

### 10. SCOPING/ROL FUNCIONANDO
**URL:** `http://127.0.0.1:8000/admin/`
**Acción:** Login como vendedor_juan
**Captura:** Ejemplo de scoping/rol funcionando (usuario limitado)

## 📋 ORDEN DE CAPTURAS:

1. **Configuración BD** (settings.py)
2. **Login como admin** → Menú completo
3. **Usuarios Django** (auth/user)
4. **Tablas maestras/operativas** con columnas
5. **Búsqueda y filtros** funcionando
6. **Inline** en Ventas
7. **Acción personalizada** en Alertas
8. **Validación** en Productos
9. **Logout admin**
10. **Login como vendedor_juan** → Menú reducido
11. **Restricción de acceso** (403 o botón oculto)

## 🎯 PUNTOS CLAVE A DESTACAR:

- **Base de datos:** MySQL con .env
- **Tablas maestras:** 6 (Categorías, Clientes, Direcciones, Nutricional, Productos, Roles)
- **Tablas operativas:** 5 (Ventas, Detalle_Venta, Movimientos, Alertas, Usuarios)
- **Inline:** DetalleVentaInline en VentasAdmin
- **Acción:** mark_alerts_as_resolved en AlertasAdmin
- **Validación:** clean() en Productos (caducidad > elaboración)
- **Scoping:** has_module_permission() para restringir acceso por rol

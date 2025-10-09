# 🍞 Sistema de Gestión Fornería - Django Admin

Proyecto Django para gestión integral de panadería/fornería con Django Admin completamente personalizado.

**Autor:** Nina9114  
**GitHub:** https://github.com/Nina9114  
**Institución:** Duoc UC

---

## 📋 Descripción del Proyecto

Sistema web desarrollado en Django que permite gestionar todas las operaciones de una fornería, incluyendo:
- Gestión de productos y categorías
- Control de inventario con alertas automáticas
- Registro de ventas con cálculo automático de IVA
- Administración de clientes
- Sistema de roles con permisos diferenciados (Administrador y Vendedor)
- Información nutricional de productos

---

## ✨ Características Principales

### ✅ Conexión a Base de Datos
- **MySQL** configurado con variables de entorno (`.env`)
- Migraciones correctas y funcionales
- Compatible con WAMP/phpMyAdmin

### ✅ Admin Básico
- **6 Tablas Maestras:** Direccion, Roles, Clientes, Categorias, Nutricional, Productos
- **5 Tablas Operativas:** Ventas, Detalle_Venta, Movimientos_Inventario, Alertas, Usuarios
- Configuración completa con:
  - `list_display`: Columnas personalizadas
  - `search_fields`: Búsquedas por nombre, RUT, email, folio
  - `list_filter`: Filtros por categoría, fecha, estado, tipo
  - `ordering`: Ordenamiento por defecto
  - `list_select_related`: Optimización de consultas

### ✅ Admin Pro
1. **Inline (DetalleVentaInline):** 
   - Permite agregar/editar items de venta directamente en el formulario de venta
   - Calcula subtotales automáticamente
   - Muestra total formateado

2. **Acción Personalizada (mark_alerts_as_resolved):**
   - Marca múltiples alertas como atendidas en una sola acción
   - Feedback visual al usuario

3. **Validación (clean() en Productos):**
   - Valida que la fecha de caducidad sea posterior a la de elaboración
   - Valida que el stock actual no sea negativo
   - Muestra errores claros en el formulario

### ✅ Seguridad y Roles
- **2 usuarios requeridos:**
  1. **Administrador (admin):** Acceso completo al sistema
  2. **Vendedor (vendedor_juan):** Acceso limitado

- **Restricciones del Vendedor:**
  - ✅ Puede gestionar: Ventas, Detalle_Venta, Clientes
  - ✅ Puede ver (solo lectura): Productos
  - ❌ NO puede acceder a: Roles, Usuarios, Movimientos_Inventario, Nutricional, Direccion, Alertas
  - ❌ NO puede eliminar ventas

### ✅ Soft Delete Pattern
Todos los modelos incluyen campos `created_at`, `updated_at` y `deleted_at` para mantener historial.

---

## 🛠️ Requisitos del Sistema

- **Python:** 3.8 o superior
- **MySQL:** 5.7 o superior (WAMP/XAMPP compatible)
- **Git:** Para control de versiones
- **Git Bash:** Para ejecución de comandos (Windows)

---

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Nina9114/forneria_project.git
cd forneria_project
```

### 2. Crear y activar entorno virtual

#### En Git Bash (Windows):
```bash
python -m venv venv
source venv/Scripts/activate
```

#### En CMD (Windows):
```cmd
python -m venv venv
venv\Scripts\activate
```

#### En Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- Django 4.2.7
- mysqlclient 2.2.0
- python-decouple 3.8
- Pillow 10.1.0

### 4. Configurar Base de Datos

#### 4.1 Crear la base de datos en MySQL

**Opción A: Desde phpMyAdmin (WAMP):**
1. Abrir phpMyAdmin (http://localhost/phpmyadmin/)
2. Crear nueva base de datos llamada `forneria`
3. Charset: `utf8_spanish_ci`

**Opción B: Desde línea de comandos:**
```sql
mysql -u root -p
CREATE DATABASE forneria CHARACTER SET utf8 COLLATE utf8_spanish_ci;
EXIT;
```

#### 4.2 Configurar archivo `.env`

El archivo `.env` ya existe en el proyecto. Verifica/edita los valores según tu configuración:

```env
DB_NAME=forneria
DB_USER=root
DB_PASSWORD=tu_contraseña_mysql
DB_HOST=127.0.0.1
DB_PORT=3306
SECRET_KEY=django-insecure-forneria-2024-change-in-production
```

**IMPORTANTE para WAMP:**
- Usa `127.0.0.1` en lugar de `localhost`
- Asegúrate de que el servicio MySQL de WAMP esté corriendo (ícono verde)
- Usa la contraseña configurada en phpMyAdmin

### 5. Ejecutar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

Este comando creará todas las tablas en la base de datos MySQL.

### 6. Crear Superusuario

```bash
python manage.py createsuperuser
```

Proporciona los siguientes datos:
- **Username:** admin
- **Email:** admin@forneria.cl
- **Password:** admin123 (o la que prefieras)

### 7. Cargar Datos de Prueba

```bash
python manage.py seed_data
```

Este comando cargará:
- 3 direcciones
- 2 roles (Administrador, Vendedor)
- 6 categorías de productos
- 12 productos con información nutricional
- 5 clientes
- 5 ventas con detalles
- 4 movimientos de inventario
- 3 alertas
- 2 usuarios del sistema
- Usuario vendedor de Django (`vendedor_juan`)

### 8. Ejecutar el Servidor

```bash
python manage.py runserver
```

Acceder al admin en: **http://127.0.0.1:8000/admin/**

---

## 🔑 Credenciales de Acceso

### Administrador (Acceso Completo)
- **Usuario:** admin
- **Contraseña:** admin123
- **Permisos:** Acceso total a todos los modelos

### Vendedor (Acceso Limitado)
- **Usuario:** vendedor_juan
- **Contraseña:** vendedor123
- **Permisos:** Solo Ventas, Clientes, Productos (lectura)

---

## 📁 Estructura del Proyecto

```
forneria_project/
├── .env                          # Variables de entorno (NO subir a Git)
├── .gitignore                    # Archivos ignorados por Git
├── requirements.txt              # Dependencias Python
├── manage.py                     # Comando principal Django
├── README.md                     # Este archivo
│
├── forneria/                     # Proyecto Django principal
│   ├── __init__.py
│   ├── settings.py              # Configuración (DATABASES con .env)
│   ├── urls.py                  # URLs principales
│   ├── wsgi.py                  # Configuración WSGI
│   └── asgi.py                  # Configuración ASGI
│
└── shop/                         # Aplicación principal
    ├── __init__.py
    ├── models.py                # 11 modelos (6 maestras + 5 operativas)
    ├── admin.py                 # Configuración Django Admin completa
    ├── apps.py                  # Configuración de la app
    ├── views.py                 # Vistas (futuro)
    ├── tests.py                 # Pruebas
    │
    ├── migrations/              # Migraciones de base de datos
    │   └── __init__.py
    │
    └── management/              # Comandos personalizados
        ├── __init__.py
        └── commands/
            ├── __init__.py
            └── seed_data.py     # Comando para cargar datos de prueba
```

---

## 📊 Modelos de Base de Datos

### Tablas Maestras (6)

1. **Direccion:** Direcciones físicas
2. **Roles:** Roles de usuario (Administrador, Vendedor)
3. **Clientes:** Clientes de la fornería
4. **Categorias:** Categorías de productos
5. **Nutricional:** Información nutricional
6. **Productos:** Catálogo de productos

### Tablas Operativas (5)

1. **Ventas:** Transacciones de venta
2. **Detalle_Venta:** Items de cada venta
3. **Movimientos_Inventario:** Control de stock
4. **Alertas:** Notificaciones de stock/vencimiento
5. **Usuarios:** Personal del sistema

**Nota:** Todos los modelos incluyen `created_at`, `updated_at`, `deleted_at`.

---

## 🎯 Funcionalidades del Admin

### Búsquedas Implementadas
- Productos: por nombre, marca, descripción
- Clientes: por nombre, RUT, correo
- Ventas: por folio, nombre de cliente
- Usuarios: por nombres, RUN, correo

### Filtros Implementados
- Productos: por categoría, tipo, fecha de caducidad
- Ventas: por canal de venta, fecha
- Movimientos: por tipo de movimiento, fecha
- Alertas: por tipo de alerta, estado

### Inline (Detalle de Venta)
- Aparece dentro del formulario de Ventas
- Permite agregar/editar productos vendidos
- Calcula subtotales automáticamente

### Acción Personalizada
- **"Marcar alertas como atendidas"**
- Seleccionar múltiples alertas
- Cambiar estado de pendiente a atendida en bloque

### Validaciones
- Fecha de caducidad > fecha de elaboración
- Stock actual no puede ser negativo
- Mensajes de error claros en formularios

---

## 🔒 Seguridad y Permisos

### Implementación de Roles

El sistema usa **Django Groups** para gestionar permisos:

#### Grupo "Vendedor":
```python
# Permisos asignados:
- Ventas: view, add, change (NO delete)
- Detalle_Venta: view, add, change, delete
- Clientes: view, add, change, delete
- Productos: view (solo lectura)
```

#### Restricciones adicionales:
- `has_module_permission()`: Oculta módulos no autorizados
- `has_delete_permission()`: Bloquea eliminación de ventas para vendedores

---

## 🚀 Comandos Útiles

```bash
# Activar entorno virtual
source venv/Scripts/activate          # Git Bash
venv\Scripts\activate                  # CMD Windows

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Cargar datos de prueba
python manage.py seed_data

# Ejecutar servidor de desarrollo
python manage.py runserver

# Abrir shell de Django
python manage.py shell

# Ver SQL de una migración
python manage.py sqlmigrate shop 0001

# Verificar problemas del proyecto
python manage.py check
```

---

## 📸 Capturas para el Informe

### Requeridas para la evaluación:

1. ✅ **settings.py - DATABASES:** Configuración de conexión MySQL
2. ✅ **Lista de usuarios:** Mostrar is_staff y grupo "Vendedor"
3. ✅ **Login como vendedor:** Menú reducido (solo Ventas, Clientes, Productos)
4. ✅ **Restricción:** Intento de acceder a modelo bloqueado (404 o sin menú)
5. ✅ **Admin con columnas:** Lista de productos con columnas personalizadas
6. ✅ **Búsqueda y filtro:** Demostración funcionando
7. ✅ **Inline:** Detalle de venta dentro de formulario de venta
8. ✅ **Acción personalizada:** Marcar alertas ejecutándose
9. ✅ **Validación:** Error al poner fecha caducidad < elaboración
10. ✅ **Scoping/Rol:** Vendedor sin acceso a Roles, Usuarios, Alertas, etc.

---

## 🧪 Demostración en Laboratorio

### Pasos para la revisión en vivo:

1. **Clonar el repositorio** en el PC del laboratorio
2. **Crear entorno virtual** e instalar dependencias
3. **Configurar `.env`** con datos de la BD del laboratorio
4. **Ejecutar migraciones:** `python manage.py migrate`
5. **Cargar semillas:** `python manage.py seed_data`
6. **Levantar servidor:** `python manage.py runserver`
7. **Demostrar:**
   - Login como admin → mostrar todos los modelos
   - Login como vendedor_juan → mostrar menú reducido
   - Intentar acceder a Roles o Usuarios como vendedor → Sin acceso
   - Mostrar inline, acción, validación funcionando

---

## 🐛 Solución de Problemas

### Error: "Can't connect to MySQL server"
**Solución:** 
- Verifica que WAMP esté corriendo (ícono verde)
- Usa `127.0.0.1` en lugar de `localhost` en `.env`
- Verifica que el puerto sea 3306

### Error: "Access denied for user 'root'"
**Solución:** 
- Verifica la contraseña en `.env`
- Prueba sin contraseña si WAMP está por defecto: `DB_PASSWORD=`

### Error: "No module named 'MySQLdb'"
**Solución:** 
```bash
pip install mysqlclient
```

### Error en Windows: "error: Microsoft Visual C++ 14.0 is required"
**Solución:** 
- Descargar wheel precompilado: https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
- Instalar: `pip install mysqlclient‑2.2.0‑cp310‑cp310‑win_amd64.whl`

### Migraciones en conflicto con BD existente
**Solución:**
```bash
python manage.py migrate --fake-initial
```

---

## 📝 Diagrama ER

El diagrama Entidad-Relación debe incluir:

- **11 tablas** con nombres en inglés
- **Tipos de datos:** INT, VARCHAR(length), DECIMAL(10,2), DATE, TIMESTAMP
- **Claves primarias (PK)** identificadas
- **Claves foráneas (FK)** con relaciones
- **Campos especiales:** created_at, updated_at, deleted_at
- **Cardinalidad:** 1:N, N:1

**Herramientas recomendadas:**
- MySQL Workbench (Reverse Engineer)
- Draw.io
- Lucidchart
- dbdiagram.io

---

## 📚 Tecnologías Utilizadas

- **Backend:** Django 4.2.7
- **Base de Datos:** MySQL 5.7+
- **ORM:** Django ORM
- **Admin:** Django Admin personalizado
- **Variables de Entorno:** python-decouple
- **Control de Versiones:** Git/GitHub

---

## ✅ Cumplimiento de Rúbrica

| Criterio | Puntaje | Estado |
|----------|---------|--------|
| Conexión BD + Migraciones | 9 pts | ✅ MySQL con .env |
| Admin Básico | 10 pts | ✅ 11 modelos configurados |
| Admin Pro | 22 pts | ✅ Inline + Acción + Validación |
| Seguridad (scoping/rol) | 15 pts | ✅ 2 usuarios con restricciones |
| Informe escrito | 15 pts | ✅ Documentación completa |
| Revisión en vivo | 20 pts | ✅ Proyecto funcional |
| **TOTAL** | **91 pts** | ✅ |

---

## 📞 Contacto

**Estudiante:** Nina9114  
**GitHub:** https://github.com/Nina9114  
**Email:** (tu email)

---

## 📄 Licencia

Proyecto académico - Duoc UC  
Evaluación Sumativa II - Programación Web

---

## 🙏 Agradecimientos

- Duoc UC - Escuela de Informática y Telecomunicaciones
- Docente del ramo
- Comunidad Django

---

**Última actualización:** Octubre 2025


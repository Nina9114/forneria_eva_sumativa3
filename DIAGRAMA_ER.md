# DIAGRAMA ER - SISTEMA FORNERÍA

## ENTIDADES Y RELACIONES

### TABLAS MAESTRAS (6):

1. **Direccion**
   - id: INT (PK, AUTO_INCREMENT)
   - calle: VARCHAR(100)
   - numero: VARCHAR(10)
   - depto: VARCHAR(10) NULL
   - comuna: VARCHAR(100)
   - region: VARCHAR(100)
   - codigo_postal: VARCHAR(45) NULL
   - created_at: TIMESTAMP
   - updated_at: TIMESTAMP
   - deleted_at: TIMESTAMP NULL

2. **Roles**
   - id: INT (PK, AUTO_INCREMENT)
   - nombre: VARCHAR(100)
   - descripcion: VARCHAR(200) NULL
   - created_at: TIMESTAMP
   - updated_at: TIMESTAMP
   - deleted_at: TIMESTAMP NULL

3. **Clientes**
   - id: INT (PK, AUTO_INCREMENT)
   - rut: VARCHAR(12) NULL (UNIQUE)
   - nombre: VARCHAR(150)
   - correo: VARCHAR(100) NULL
   - created_at: TIMESTAMP
   - updated_at: TIMESTAMP
   - deleted_at: TIMESTAMP NULL

4. **Categorias**
   - id: INT (PK, AUTO_INCREMENT)
   - nombre: VARCHAR(100)
   - descripcion: VARCHAR(200) NULL
   - created_at: TIMESTAMP
   - updated_at: TIMESTAMP
   - deleted_at: TIMESTAMP NULL

5. **Nutricional**
   - id: INT (PK, AUTO_INCREMENT)
   - calorias: DECIMAL(10,2) NULL
   - proteinas: DECIMAL(10,2) NULL
   - grasas: DECIMAL(10,2) NULL
   - carbohidratos: DECIMAL(10,2) NULL
   - azucares: DECIMAL(10,2) NULL
   - sodio: DECIMAL(10,2) NULL
   - created_at: TIMESTAMP
   - updated_at: TIMESTAMP
   - deleted_at: TIMESTAMP NULL

6. **Productos**
   - id: INT (PK, AUTO_INCREMENT)
   - nombre: VARCHAR(100)
   - descripcion: VARCHAR(300) NULL
   - marca: VARCHAR(100) NULL
   - precio: DECIMAL(10,2)
   - caducidad: DATE
   - elaboracion: DATE NULL
   - tipo: VARCHAR(100)
   - Categorias_id: INT (FK → Categorias.id)
   - stock_actual: INT NULL
   - stock_minimo: INT NULL
   - stock_maximo: INT NULL
   - presentacion: VARCHAR(100) NULL
   - formato: VARCHAR(100) NULL
   - Nutricional_id: INT (FK → Nutricional.id)
   - created_at: TIMESTAMP
   - updated_at: TIMESTAMP
   - deleted_at: TIMESTAMP NULL

### TABLAS OPERATIVAS (5):

7. **Ventas**
   - id: INT (PK, AUTO_INCREMENT)
   - fecha: TIMESTAMP
   - cliente_id: INT (FK → Clientes.id)
   - total_sin_iva: DECIMAL(10,2)
   - total_iva: DECIMAL(10,2)
   - descuento: DECIMAL(10,2)
   - total_con_iva: DECIMAL(10,2)
   - canal_venta: ENUM('Local', 'UberEats', 'Instagram', 'WhatsApp')
   - folio: VARCHAR(20) NULL
   - monto_pagado: DECIMAL(10,2) NULL
   - vuelto: DECIMAL(10,2) NULL
   - created_at: TIMESTAMP
   - updated_at: TIMESTAMP
   - deleted_at: TIMESTAMP NULL

8. **Detalle_Venta**
   - id: INT (PK, AUTO_INCREMENT)
   - venta_id: INT (FK → Ventas.id)
   - producto_id: INT (FK → Productos.id)
   - cantidad: INT
   - precio_unitario: DECIMAL(10,2)
   - descuento_pct: DECIMAL(5,2) NULL
   - created_at: TIMESTAMP
   - updated_at: TIMESTAMP
   - deleted_at: TIMESTAMP NULL

9. **Movimientos_Inventario**
   - id: INT (PK, AUTO_INCREMENT)
   - producto_id: INT (FK → Productos.id)
   - tipo_movimiento: ENUM('entrada', 'salida', 'ajuste')
   - cantidad: INT
   - fecha: TIMESTAMP
   - created_at: TIMESTAMP
   - updated_at: TIMESTAMP
   - deleted_at: TIMESTAMP NULL

10. **Alertas**
    - id: INT (PK, AUTO_INCREMENT)
    - producto_id: INT (FK → Productos.id)
    - tipo_alerta: ENUM('Stock bajo', 'Vencimiento próximo')
    - mensaje: VARCHAR(255)
    - fecha_generada: TIMESTAMP
    - estado: VARCHAR(20) DEFAULT 'pendiente'
    - created_at: TIMESTAMP
    - updated_at: TIMESTAMP
    - deleted_at: TIMESTAMP NULL

11. **Usuarios**
    - id: INT (PK, AUTO_INCREMENT)
    - nombres: VARCHAR(100)
    - paterno: VARCHAR(100)
    - materno: VARCHAR(100) NULL
    - run: VARCHAR(12) UNIQUE
    - correo: VARCHAR(100)
    - fono: VARCHAR(20) NULL
    - clave: VARCHAR(150) NULL
    - Direccion_id: INT (FK → Direccion.id)
    - Roles_id: INT (FK → Roles.id)
    - created_at: TIMESTAMP
    - updated_at: TIMESTAMP
    - deleted_at: TIMESTAMP NULL

## RELACIONES:

- Productos → Categorias (N:1)
- Productos → Nutricional (N:1)
- Ventas → Clientes (N:1)
- Detalle_Venta → Ventas (N:1)
- Detalle_Venta → Productos (N:1)
- Movimientos_Inventario → Productos (N:1)
- Alertas → Productos (N:1)
- Usuarios → Direccion (N:1)
- Usuarios → Roles (N:1)

## CARDINALIDADES:

- 1 Categoría → N Productos
- 1 Nutricional → N Productos
- 1 Cliente → N Ventas
- 1 Venta → N Detalle_Venta
- 1 Producto → N Detalle_Venta
- 1 Producto → N Movimientos_Inventario
- 1 Producto → N Alertas
- 1 Dirección → N Usuarios
- 1 Rol → N Usuarios

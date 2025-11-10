# Informe de avances – Proyecto Fornería

## Resumen general
- Se reforzó la autenticación con perfiles, cambio y recuperación de contraseña, página 404 personalizada y navegación dinámica según permisos.
- Se modernizó el CRUD de productos: formularios con validaciones, filtros avanzados, ordenamiento, exportación a Excel y eliminación segura vía POST.
- Se implementó un CRUD completo de ventas con formularios anidados, filtros, exportación a Excel y eliminación segura.
- Se mejoró la capa visual (SweetAlert + Bootstrap) y la consistencia de mensajes y permisos en las vistas.

## Cambios de autenticación y UX
- `login_view` ahora regenera la sesión y redirige según los grupos (`Administrador`, `Editor`, `Lector`).
- Formularios `UserForm`, `UserProfileForm`, `CustomPasswordChangeForm`, `CustomSetPasswordForm` habilitan edición de perfil y contraseñas con reglas de seguridad.
- Flujo completo de recuperación de contraseña (`CustomPasswordReset*`) con plantillas propias y mensajes neutros.
- Se añadió `UserProfile` (avatar, teléfono) y la página `profile_view` para que cada usuario edite sus datos.
- Página 404 temática (`shop/templates/404.html`) y ajustes de `settings.py` para leer `DEBUG`/`ALLOWED_HOSTS` desde `.env`.
- Navbar sensible a roles/permisos, con enlaces a secciones protegidas.

## CRUD de productos reforzado
- `ProductoForm` centraliza validaciones de negocio (precio, fechas, stock) y usa widgets Bootstrap.
- Vistas `productos_create/edit/delete/detail` dependen del formulario, gestionan mensajes y soportan redirecciones con `next`.
- Listado (`productos_list`) ofrece búsqueda, filtros por categoría/tipo, ordenamiento por columnas, tamaños de página persistentes y exportación a Excel (mediante `openpyxl`).
- Plantillas de crear/editar/detalle/listado muestran errores campo a campo y confirman la eliminación por POST con SweetAlert.

## CRUD de ventas implementado
- `VentaForm` y `DetalleVentaFormSet` permiten capturar ventas con múltiples productos, validando montos y descuentos.
- Vistas `ventas_list/create/edit/detail/delete` calculan totales, manejan formularios anidados y soportan redirecciones con `next`.
- El listado (`ventas_list`) incluye filtros por fecha, canal y buscador, paginación configurable, ordenamiento y exportación a Excel.
- Plantillas de ventas muestran errores campo a campo, resumen de pago, auto-completan precios/formato según el producto y utilizan SweetAlert para confirmaciones por POST.

## Dependencias y utilidades
- Se añadió `openpyxl==3.1.5` a `requirements.txt` y se instaló en el entorno virtual.
- Se mantuvieron verificaciones con `python manage.py check` tras los bloques de cambios.

## Próximos pasos sugeridos
- Replicar esta estrategia (formularios, filtros, exportación, eliminación por POST) en el CRUD de `Clientes`.
- Ajustar `seed_data.py` y pruebas manuales para cubrir perfiles nutricionales y nuevos roles (ventas ya actualizado).
- Planificar el despliegue (añadir `gunicorn`, configurar `collectstatic`, preparar scripts para AWS).

---
> Informe generado automáticamente por el asistente ({{"now"}}).

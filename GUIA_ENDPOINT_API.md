# Guía Completa: Crear un Endpoint API RESTful en Django - Explicación Paso a Paso

## ¿Qué es un Endpoint API?

Un **endpoint** es una URL especial que devuelve datos en formato JSON en lugar de una página web HTML. Es como una "puerta" que permite que otras aplicaciones o servicios obtengan información de tu servidor.

---

## Paso 1: Crear la Vista `info` en `shop/views.py`

### ¿Qué hicimos?
Agregamos una función que retorna datos en formato JSON.

### ¿Por qué?
- **Django necesita una función**: Para que Django sepa qué hacer cuando alguien visite la URL, necesitamos crear una función (vista) que maneje esa petición.
- **JsonResponse**: Es una clase especial de Django que convierte un diccionario de Python en formato JSON (el formato que las APIs usan).
- **No necesita base de datos**: Esta función es simple, solo retorna información estática, no consulta la base de datos.

### Código:
```python
from django.http import JsonResponse

def info(request):
    return JsonResponse({
        "proyecto": "EcoEnergy",
        "version": "1.0",
        "autor": "Magdalena Armstrong"
    })
```

### Explicación del código:
- `from django.http import JsonResponse`: Importamos la herramienta que convierte datos a JSON.
- `def info(request):`: Creamos una función llamada `info` que recibe la petición HTTP.
- `return JsonResponse({...})`: Retornamos un JSON con los datos que queremos mostrar.

---

## Paso 2: Configurar la URL en `shop/urls.py`

### ¿Qué hicimos?
Agregamos una ruta que conecta la URL `/api/info/` con la función `info`.

### ¿Por qué?
- **Django necesita saber qué función ejecutar**: Cuando alguien visita una URL, Django busca en el archivo `urls.py` para saber qué función debe ejecutar.
- **Sin esto, Django no sabría qué hacer**: Si no configuramos la ruta, Django devolvería un error 404 (página no encontrada).

### Código:
```python
from .views import info

urlpatterns = [
    # ... otras rutas ...
    path('api/info/', info, name='info'),
]
```

### Explicación:
- `from .views import info`: Importamos la función `info` que creamos antes.
- `path('api/info/', info, name='info')`: Le decimos a Django: "Cuando alguien visite `/api/info/`, ejecuta la función `info`".

---

## Paso 3: Verificar que DRF esté en `INSTALLED_APPS`

### ¿Qué hicimos?
Verificamos que `'rest_framework'` esté en la lista de `INSTALLED_APPS` en `settings.py`.

### ¿Por qué?
- **INSTALLED_APPS**: Es una lista donde Django registra todas las aplicaciones que debe usar.
- **Aunque no lo usemos directamente**: En este caso simple no necesitamos DRF, pero es buena práctica tenerlo instalado para futuras APIs más complejas.

### Ubicación:
```python
INSTALLED_APPS = [
    # ... otras apps ...
    'rest_framework',  # ← Esto debe estar aquí
    'shop',
]
```

---

## Paso 4: Instalar `djangorestframework`

### ¿Qué hicimos?
Ejecutamos `pip install djangorestframework` en PowerShell.

### ¿Por qué?
- **Error que apareció**: Aunque `rest_framework` estaba en `INSTALLED_APPS`, no estaba instalado en el entorno virtual.
- **Python no puede importar lo que no existe**: Si intentas usar algo que no está instalado, Python lanza un error `ModuleNotFoundError`.

### Comando:
```powershell
pip install djangorestframework
```

### Analogía:
Es como tener un libro en tu lista de lectura, pero no tenerlo físicamente en tu biblioteca. Necesitas comprarlo (instalarlo) primero.

---

## Paso 5: Agregar a `requirements.txt`

### ¿Qué hicimos?
Agregamos `djangorestframework` al archivo `requirements.txt`.

### ¿Por qué?
- **requirements.txt**: Es un archivo que lista todas las dependencias (paquetes) que tu proyecto necesita.
- **Para que otros puedan instalar lo mismo**: Si alguien más trabaja en tu proyecto, puede ejecutar `pip install -r requirements.txt` y tendrá todas las dependencias.
- **Para producción**: Cuando despliegues tu proyecto en un servidor, necesitarás instalar todas las dependencias.

### Archivo `requirements.txt`:
```
djangorestframework==3.14.0  # ← Agregamos esto
```

---

## Paso 6: Iniciar WampServer (MySQL)

### ¿Qué hicimos?
Iniciamos WampServer para que MySQL esté disponible.

### ¿Por qué?
- **Django necesita conectarse a la base de datos**: Aunque nuestro endpoint `/api/info/` no usa la base de datos, Django intenta conectarse a MySQL cuando inicia el servidor.
- **Si MySQL no está corriendo**: Django no puede iniciar y muestra un error de conexión.
- **WampServer incluye MySQL**: WampServer es un paquete que incluye Apache, MySQL y PHP para Windows.

### ¿Qué es WampServer?
- **W** = Windows
- **A** = Apache (servidor web)
- **M** = MySQL (base de datos)
- **P** = PHP (lenguaje de programación)

---

## Paso 7: Ejecutar el Servidor Django

### ¿Qué hicimos?
Ejecutamos `python manage.py runserver` en PowerShell.

### ¿Por qué?
- **Django necesita un servidor web**: Para que tu aplicación funcione, necesitas un servidor que "escuche" las peticiones HTTP.
- **runserver**: Es un servidor de desarrollo incluido en Django que es perfecto para probar tu aplicación localmente.
- **Sin esto, no hay servidor**: Si no ejecutas el servidor, nadie puede acceder a tu aplicación.

### Comando:
```powershell
python manage.py runserver
```

### Resultado esperado:
```
Starting development server at http://127.0.0.1:8000/
```

---

## Paso 8: Probar el Endpoint en Apidog

### ¿Qué hicimos?
Enviamos una petición GET a `http://localhost:8000/api/info/` desde Apidog.

### ¿Por qué?
- **Apidog es una herramienta para probar APIs**: Similar a Postman o Insomnia, te permite hacer peticiones HTTP sin escribir código.
- **Verificar que funciona**: Necesitas probar que tu endpoint realmente funciona y devuelve el JSON correcto.

### Configuración en Apidog:
- **Método**: GET
- **URL**: `http://localhost:8000/api/info/`

### Respuesta esperada:
```json
{
    "proyecto": "EcoEnergy",
    "version": "1.0",
    "autor": "Magdalena Armstrong"
}
```

---

## Resumen del Flujo Completo

1. **Cliente (Apidog)** → Hace una petición GET a `http://localhost:8000/api/info/`
2. **Django** → Recibe la petición y busca la ruta en `urls.py`
3. **Django** → Encuentra `path('api/info/', info)` y sabe que debe ejecutar la función `info`
4. **Django** → Ejecuta la función `info(request)`
5. **Función `info`** → Retorna `JsonResponse({...})`
6. **Django** → Envía el JSON de vuelta al cliente
7. **Cliente (Apidog)** → Muestra el JSON recibido

---

## Conceptos Clave Explicados

### Endpoint
Una URL que devuelve datos en lugar de una página web HTML. Es como una "puerta" de entrada a tu aplicación.

### JSON
Un formato de datos que es fácil de leer tanto para humanos como para máquinas. Es el formato estándar para APIs.

### Vista (View)
Una función en Django que maneja una petición HTTP y retorna una respuesta.

### URL Routing
El proceso de conectar URLs con funciones. Django usa `urls.py` para hacer esto.

### Servidor de Desarrollo
Un servidor web simple que Django incluye para que puedas probar tu aplicación en tu computadora local.

---

## Comandos Utilizados

```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Instalar djangorestframework
pip install djangorestframework

# Ejecutar servidor Django
python manage.py runserver
```

---

## Solución de Problemas

### Error: ModuleNotFoundError: No module named 'rest_framework'
**Solución**: Ejecuta `pip install djangorestframework`

### Error: Can't connect to MySQL server
**Solución**: Inicia WampServer y asegúrate de que MySQL esté corriendo (ícono verde)

### Error: 404 Not Found al probar el endpoint
**Solución**: Verifica que la ruta esté correctamente configurada en `shop/urls.py` y que el servidor esté corriendo

---

## Próximos Pasos

Una vez que domines este endpoint simple, puedes:
- Crear endpoints que consulten la base de datos
- Usar ModelSerializer de DRF para serializar modelos
- Implementar un CRUD completo (Create, Read, Update, Delete)
- Agregar autenticación a tus endpoints

---

**Autor**: Magdalena Armstrong  
**Fecha**: 2025  
**Proyecto**: Forneria - Actividad API REST


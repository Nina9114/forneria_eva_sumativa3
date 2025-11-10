# Guía de despliegue en AWS (EC2 + RDS)

> **Objetivo**: publicar `forneria_project` en producción usando una instancia EC2 (Debian 12 / Ubuntu 22) y base de datos MySQL en RDS. Esta guía asume dominio propio y que trabajas con HTTPS mediante Nginx.

---

## 1. Preparativos locales

1. **Revisar dependencias**
   ```bash
   pip freeze | grep -E "Django|gunicorn|whitenoise"
   ```
   Asegúrate de tener `gunicorn` y `whitenoise` instalados (ya declarados en `requirements.txt`).

2. **Variables de entorno (.env)**  
   Ajusta el archivo `.env` con los valores que usarás en producción:
   ```env
   DEBUG=False
   ALLOWED_HOSTS=tu_dominio.com,www.tu_dominio.com
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   CSRF_TRUSTED_ORIGINS=https://tu_dominio.com,https://www.tu_dominio.com
   SECURE_HSTS_SECONDS=31536000
   SECURE_HSTS_INCLUDE_SUBDOMAINS=True
   SECURE_HSTS_PRELOAD=True
   ```
   Más las credenciales de RDS (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`).

3. **Collectstatic local (opcional)**  
   Puedes probar que la configuración de estáticos funciona:
   ```bash
   python manage.py collectstatic --noinput
   ```

---

## 2. Provisionar infraestructura

1. **RDS MySQL**
   - Motor: MySQL 8.x
   - Zona horaria: UTC (se puede ajustar luego)
   - Seguridad: abrir puerto 3306 sólo para la instancia EC2 (grupo de seguridad compartido o regla específica).
   - Configurar usuario/contraseña y base de datos (por ejemplo `forneria_prod`).

2. **EC2**
   - AMI recomendada: Debian 12 o Ubuntu 22.04 LTS.
   - Tipo t3.small o superior según carga esperada.
   - Grupo de seguridad: abrir `22` (SSH) sólo para tu IP, `80` y `443` para público.
   - Asociar Elastic IP para tener dirección fija.

3. **Dominio**
   - Crear registros DNS `A`/`CNAME` apuntando a la Elastic IP.

---

## 3. Configuración de la instancia EC2

1. **Actualizar paquetes**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Instalar dependencias del sistema**
   ```bash
   sudo apt install -y python3 python3-venv python3-dev build-essential libmysqlclient-dev nginx git
   ```

3. **Crear usuario de despliegue (opcional)**
   ```bash
   sudo adduser --disabled-password deploy
   sudo usermod -aG sudo deploy
   ```
   Trabaja con `deploy` vía SSH (`sudo su - deploy`).

---

## 4. Desplegar el código

1. **Clonar repositorio**
   ```bash
   git clone https://github.com/tu_usuario/forneria_project.git
   cd forneria_project
   ```

2. **Crear entorno virtual**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configurar `.env` en el servidor**
   ```bash
   cp .env.example .env   # si existe, sino crear desde cero
   nano .env              # pegar valores definitivos
   ```
   No olvides agregar las claves de correo si usarás SMTP real.

4. **Migraciones y datos base**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```
   Si necesitas datos iniciales: `python manage.py seed_data` (previo backup de la BD).

---

## 5. Configurar gunicorn como servicio

1. **Probar gunicorn manualmente**
   ```bash
   gunicorn --bind 0.0.0.0:8000 forneria.wsgi:application
   ```
   Verifica que responde en `http://ip_publica:8000`. Ctrl+C para salir.

2. **Archivo unit de systemd** `/etc/systemd/system/forneria.service`
   ```ini
   [Unit]
   Description=Gunicorn Forneria
   After=network.target

   [Service]
   User=deploy
   Group=www-data
   WorkingDirectory=/home/deploy/forneria_project
   Environment="PATH=/home/deploy/forneria_project/venv/bin"
   EnvironmentFile=/home/deploy/forneria_project/.env
   ExecStart=/home/deploy/forneria_project/venv/bin/gunicorn forneria.wsgi:application --bind unix:/run/forneria.sock --workers 3 --timeout 120

   [Install]
   WantedBy=multi-user.target
   ```

3. **Crear directorio para socket**
   ```bash
   sudo mkdir -p /run
   sudo chown deploy:www-data /run
   ```

4. **Habilitar servicio**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable forneria
   sudo systemctl start forneria
   sudo systemctl status forneria
   ```
   El socket `/run/forneria.sock` debe existir y pertenecer a `deploy:www-data` (modo 660).

---

## 6. Configurar Nginx

1. **Bloque de servidor** `/etc/nginx/sites-available/forneria`
   ```nginx
   server {
       listen 80;
       server_name tu_dominio.com www.tu_dominio.com;

       location /.well-known/acme-challenge/ {
           root /var/www/certbot;
       }

       location /static/ {
           alias /home/deploy/forneria_project/staticfiles/;
           access_log off;
           add_header Cache-Control "public, max-age=31536000";
       }

       location /media/ {
           alias /home/deploy/forneria_project/media/;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/run/forneria.sock;
       }

       client_max_body_size 20M;
   }
   ```

2. **Activar sitio**
   ```bash
   sudo ln -s /etc/nginx/sites-available/forneria /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

3. **Certbot (HTTPS)**
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   sudo certbot --nginx -d tu_dominio.com -d www.tu_dominio.com
   ```
   Certbot crea un cron automatizado. Verifica con `systemctl status certbot.timer`.

4. **Refuerzo HTTPS**  
   Tras obtener certificado, Nginx actualizará el bloque a 443. Confirma que `SECURE_*` en `.env` corresponde.

---

## 7. Supervisión y mantenimiento

1. **Logs**
   - Gunicorn: `sudo journalctl -u forneria -f`
   - Nginx: `/var/log/nginx/access.log` y `error.log`

2. **Tareas periódicas**
   - `git pull` para traer nuevos cambios.
   - `pip install -r requirements.txt`
   - `python manage.py migrate`
   - `python manage.py collectstatic --noinput`
   - `sudo systemctl restart forneria`

3. **Respaldo de base de datos**
   - Considera snapshots de RDS o `mysqldump`:
     ```bash
     mysqldump -h rds_endpoint -u usuario -p forneria_prod > respaldo.sql
     ```

4. **Seguridad**
   - Regla de firewall para limitar SSH.
   - Actualizar paquetes regularmente.
   - Rotar contraseñas y claves SSH.

---

## 8. Checklist final

- [ ] `.env` con variables de producción y secretos seguros.
- [ ] Migraciones ejecutadas contra RDS.
- [ ] `collectstatic` realizado y archivos en `/staticfiles/`.
- [ ] Gunicorn activo (`systemctl status forneria`).
- [ ] Nginx sirviendo dominio y certificado válido.
- [ ] HTTPS forzado (`SECURE_*` activos y redirección en Nginx).
- [ ] Backups automáticos configurados (RDS snapshots).
- [ ] Documentar credenciales (vault seguro / gestor de contraseñas).

Con esto, el proyecto queda listo para la defensa: la app corre en AWS, maneja archivos estáticos/media correctamente y el pipeline de actualización queda documentado. Si necesitas automatizar despliegues posteriores (CI/CD), se puede extender con GitHub Actions + SSH o con Elastic Beanstalk.

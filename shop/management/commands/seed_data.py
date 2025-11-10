"""
Comando para cargar datos de prueba en la base de datos
Incluye: Direcciones, Roles, Categorías, Productos, Clientes, Ventas, etc.
También crea grupos y permisos para el rol Vendedor
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from shop.models import *
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Q


class Command(BaseCommand):
    help = 'Carga datos de prueba en la base de datos de Fornería'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('\n' + '='*60))
        self.stdout.write(self.style.WARNING('Iniciando carga de datos de prueba...'))
        self.stdout.write(self.style.WARNING('='*60 + '\n'))
        
        # 1. Direcciones
        self.stdout.write('📍 Creando direcciones...')
        dir1 = Direccion.objects.create(
            calle='Av. Libertador Bernardo O\'Higgins',
            numero='1234',
            comuna='Santiago',
            region='Región Metropolitana',
            codigo_postal='8320000'
        )
        dir2 = Direccion.objects.create(
            calle='Av. Providencia',
            numero='567',
            depto='301',
            comuna='Providencia',
            region='Región Metropolitana',
            codigo_postal='7500000'
        )
        dir3 = Direccion.objects.create(
            calle='Av. Vicuña Mackenna',
            numero='4860',
            comuna='Macul',
            region='Región Metropolitana',
            codigo_postal='7810000'
        )
        self.stdout.write(self.style.SUCCESS('   ✓ 3 direcciones creadas\n'))

        # 2. Roles (Solo Administrador y Vendedor)
        self.stdout.write('👥 Creando roles...')
        rol_admin = Roles.objects.create(
            nombre='Administrador',
            descripcion='Acceso completo al sistema'
        )
        rol_vendedor = Roles.objects.create(
            nombre='Vendedor',
            descripcion='Gestión de ventas y clientes'
        )
        self.stdout.write(self.style.SUCCESS('   ✓ 2 roles creados (Administrador, Vendedor)\n'))

        # 3. Categorías
        self.stdout.write('🏷️  Creando categorías...')
        cat_pan = Categorias.objects.create(
            nombre='Pan',
            descripcion='Panes artesanales y tradicionales'
        )
        cat_pasteles = Categorias.objects.create(
            nombre='Pasteles',
            descripcion='Tortas y pasteles'
        )
        cat_galletas = Categorias.objects.create(
            nombre='Galletas',
            descripcion='Galletas dulces y saladas'
        )
        cat_bebidas = Categorias.objects.create(
            nombre='Bebidas',
            descripcion='Bebidas frías y calientes'
        )
        cat_empanadas = Categorias.objects.create(
            nombre='Empanadas',
            descripcion='Empanadas horneadas'
        )
        cat_dulces = Categorias.objects.create(
            nombre='Dulces',
            descripcion='Productos dulces y postres'
        )
        self.stdout.write(self.style.SUCCESS('   ✓ 6 categorías creadas\n'))

        # 4. Información Nutricional
        self.stdout.write('🥗 Creando información nutricional...')
        nutri1 = Nutricional.objects.create(
            calorias=Decimal('250.00'), proteinas=Decimal('8.00'), 
            grasas=Decimal('3.00'), carbohidratos=Decimal('45.00'), 
            azucares=Decimal('2.00'), sodio=Decimal('400.00')
        )
        nutri2 = Nutricional.objects.create(
            calorias=Decimal('350.00'), proteinas=Decimal('5.00'), 
            grasas=Decimal('15.00'), carbohidratos=Decimal('50.00'), 
            azucares=Decimal('25.00'), sodio=Decimal('200.00')
        )
        nutri3 = Nutricional.objects.create(
            calorias=Decimal('180.00'), proteinas=Decimal('6.00'), 
            grasas=Decimal('2.00'), carbohidratos=Decimal('35.00'), 
            azucares=Decimal('8.00'), sodio=Decimal('300.00')
        )
        nutri4 = Nutricional.objects.create(
            calorias=Decimal('120.00'), proteinas=Decimal('3.00'), 
            grasas=Decimal('5.00'), carbohidratos=Decimal('18.00'), 
            azucares=Decimal('10.00'), sodio=Decimal('150.00')
        )
        nutri5 = Nutricional.objects.create(
            calorias=Decimal('0.00'), proteinas=Decimal('0.00'), 
            grasas=Decimal('0.00'), carbohidratos=Decimal('0.00'), 
            azucares=Decimal('0.00'), sodio=Decimal('10.00')
        )
        nutri6 = Nutricional.objects.create(
            calorias=Decimal('280.00'), proteinas=Decimal('4.00'), 
            grasas=Decimal('12.00'), carbohidratos=Decimal('38.00'), 
            azucares=Decimal('15.00'), sodio=Decimal('180.00')
        )
        self.stdout.write(self.style.SUCCESS('   ✓ 6 perfiles nutricionales creados\n'))

        # 5. Productos
        self.stdout.write('🍞 Creando productos...')
        hoy = datetime.now().date()
        
        productos = [
            Productos.objects.create(
                nombre='Marraqueta',
                descripcion='Pan tradicional chileno, crujiente por fuera y suave por dentro',
                marca='Fornería Artesanal',
                precio=Decimal('800'),
                caducidad=hoy + timedelta(days=2),
                elaboracion=hoy,
                tipo='propia',
                Categorias_id=cat_pan,
                stock_actual=50,
                stock_minimo=10,
                stock_maximo=100,
                presentacion='unidad',
                formato='1 unidad (aprox. 100g)',
                Nutricional_id=nutri1
            ),
            Productos.objects.create(
                nombre='Hallulla',
                descripcion='Pan redondo tradicional chileno',
                marca='Fornería Artesanal',
                precio=Decimal('600'),
                caducidad=hoy + timedelta(days=2),
                elaboracion=hoy,
                tipo='propia',
                Categorias_id=cat_pan,
                stock_actual=80,
                stock_minimo=15,
                stock_maximo=150,
                presentacion='unidad',
                formato='1 unidad (aprox. 80g)',
                Nutricional_id=nutri1
            ),
            Productos.objects.create(
                nombre='Pan Amasado',
                descripcion='Pan amasado tradicional hecho en horno de barro',
                marca='Fornería Artesanal',
                precio=Decimal('1000'),
                caducidad=hoy + timedelta(days=3),
                elaboracion=hoy,
                tipo='propia',
                Categorias_id=cat_pan,
                stock_actual=40,
                stock_minimo=10,
                stock_maximo=80,
                presentacion='unidad',
                formato='1 unidad (aprox. 120g)',
                Nutricional_id=nutri1
            ),
            Productos.objects.create(
                nombre='Torta de Chocolate',
                descripcion='Torta de chocolate con manjar y cobertura de chocolate',
                marca='Fornería Artesanal',
                precio=Decimal('12000'),
                caducidad=hoy + timedelta(days=5),
                elaboracion=hoy,
                tipo='propia',
                Categorias_id=cat_pasteles,
                stock_actual=3,
                stock_minimo=3,
                stock_maximo=15,
                presentacion='unidad',
                formato='1 kg (8-10 porciones)',
                Nutricional_id=nutri2
            ),
            Productos.objects.create(
                nombre='Torta Tres Leches',
                descripcion='Torta tradicional bañada en tres leches',
                marca='Fornería Artesanal',
                precio=Decimal('10000'),
                caducidad=hoy + timedelta(days=4),
                elaboracion=hoy,
                tipo='propia',
                Categorias_id=cat_pasteles,
                stock_actual=5,
                stock_minimo=2,
                stock_maximo=12,
                presentacion='unidad',
                formato='800g (6-8 porciones)',
                Nutricional_id=nutri2
            ),
            Productos.objects.create(
                nombre='Galletas de Avena',
                descripcion='Galletas caseras de avena con pasas y nueces',
                marca='Fornería Artesanal',
                precio=Decimal('3500'),
                caducidad=hoy + timedelta(days=15),
                elaboracion=hoy,
                tipo='propia',
                Categorias_id=cat_galletas,
                stock_actual=25,
                stock_minimo=5,
                stock_maximo=50,
                presentacion='bolsa',
                formato='250g (aprox. 12 unidades)',
                Nutricional_id=nutri4
            ),
            Productos.objects.create(
                nombre='Empanada de Pino',
                descripcion='Empanada tradicional chilena con carne, cebolla, huevo y aceituna',
                marca='Fornería Artesanal',
                precio=Decimal('1500'),
                caducidad=hoy + timedelta(days=1),
                elaboracion=hoy,
                tipo='propia',
                Categorias_id=cat_empanadas,
                stock_actual=30,
                stock_minimo=10,
                stock_maximo=80,
                presentacion='unidad',
                formato='1 unidad (aprox. 180g)',
                Nutricional_id=nutri3
            ),
            Productos.objects.create(
                nombre='Empanada de Queso',
                descripcion='Empanada horneada rellena de queso',
                marca='Fornería Artesanal',
                precio=Decimal('1300'),
                caducidad=hoy + timedelta(days=1),
                elaboracion=hoy,
                tipo='propia',
                Categorias_id=cat_empanadas,
                stock_actual=35,
                stock_minimo=10,
                stock_maximo=80,
                presentacion='unidad',
                formato='1 unidad (aprox. 150g)',
                Nutricional_id=nutri3
            ),
            Productos.objects.create(
                nombre='Jugo Natural de Naranja',
                descripcion='Jugo de naranja recién exprimido sin azúcar añadida',
                marca='Fornería Artesanal',
                precio=Decimal('2000'),
                caducidad=hoy + timedelta(days=1),
                tipo='propia',
                Categorias_id=cat_bebidas,
                stock_actual=15,
                stock_minimo=5,
                stock_maximo=30,
                presentacion='vaso',
                formato='500ml',
                Nutricional_id=nutri5
            ),
            Productos.objects.create(
                nombre='Café Latte',
                descripcion='Café espresso con leche vaporizada',
                marca='Fornería Artesanal',
                precio=Decimal('2500'),
                caducidad=hoy + timedelta(days=1),
                tipo='propia',
                Categorias_id=cat_bebidas,
                stock_actual=20,
                stock_minimo=8,
                stock_maximo=40,
                presentacion='taza',
                formato='350ml',
                Nutricional_id=nutri5
            ),
            Productos.objects.create(
                nombre='Alfajor de Manjar',
                descripcion='Alfajor relleno con manjar y cubierto con azúcar flor',
                marca='Fornería Artesanal',
                precio=Decimal('1200'),
                caducidad=hoy + timedelta(days=10),
                elaboracion=hoy,
                tipo='propia',
                Categorias_id=cat_dulces,
                stock_actual=45,
                stock_minimo=10,
                stock_maximo=100,
                presentacion='unidad',
                formato='1 unidad (80g)',
                Nutricional_id=nutri6
            ),
            Productos.objects.create(
                nombre='Kuchen de Manzana',
                descripcion='Kuchen tradicional alemán con manzanas frescas',
                marca='Fornería Artesanal',
                precio=Decimal('8000'),
                caducidad=hoy + timedelta(days=4),
                elaboracion=hoy,
                tipo='propia',
                Categorias_id=cat_pasteles,
                stock_actual=6,
                stock_minimo=2,
                stock_maximo=10,
                presentacion='unidad',
                formato='600g (6 porciones)',
                Nutricional_id=nutri2
            ),
        ]
        self.stdout.write(self.style.SUCCESS(f'   ✓ {len(productos)} productos creados\n'))

        # 6. Clientes
        self.stdout.write('👤 Creando clientes...')
        clientes = [
            Clientes.objects.get_or_create(
                rut='12345678-9',
                defaults={
                    'nombre': 'Juan Pérez García',
                    'correo': 'juan.perez@email.com'
                }
            )[0],
            Clientes.objects.get_or_create(
                rut='98765432-1',
                defaults={
                    'nombre': 'María González López',
                    'correo': 'maria.gonzalez@email.com'
                }
            )[0],
            Clientes.objects.get_or_create(
                rut='11223344-5',
                defaults={
                    'nombre': 'Pedro Rodríguez Silva',
                    'correo': 'pedro.rodriguez@email.com'
                }
            )[0],
            Clientes.objects.get_or_create(
                rut='55667788-9',
                defaults={
                    'nombre': 'Ana Martínez Fernández',
                    'correo': 'ana.martinez@email.com'
                }
            )[0],
            Clientes.objects.get_or_create(
                nombre='Cliente Genérico',
                defaults={
                    'correo': 'cliente@forneria.cl'
                }
            )[0],
        ]
        self.stdout.write(self.style.SUCCESS(f'   ✓ {len(clientes)} clientes creados\n'))

        # 7. Ventas con Detalle
        self.stdout.write('🛒 Creando ventas...')
        Ventas.objects.all().delete()
        Detalle_Venta.objects.all().delete()
        
        # Venta 1
        venta1 = Ventas.objects.create(
            cliente_id=clientes[0],
            total_sin_iva=Decimal('5000.00'),
            total_iva=Decimal('950.00'),
            descuento=Decimal('0.00'),
            total_con_iva=Decimal('5950.00'),
            canal_venta='Local',
            folio='F001-00001',
            monto_pagado=Decimal('6000.00'),
            vuelto=Decimal('50.00')
        )
        Detalle_Venta.objects.create(
            venta_id=venta1,
            producto_id=productos[0],  # Marraqueta
            cantidad=3,
            precio_unitario=productos[0].precio
        )
        Detalle_Venta.objects.create(
            venta_id=venta1,
            producto_id=productos[1],  # Hallulla
            cantidad=2,
            precio_unitario=productos[1].precio
        )
        Detalle_Venta.objects.create(
            venta_id=venta1,
            producto_id=productos[8],  # Jugo
            cantidad=1,
            precio_unitario=productos[8].precio
        )

        # Venta 2
        venta2 = Ventas.objects.create(
            cliente_id=clientes[1],
            total_sin_iva=Decimal('12000.00'),
            total_iva=Decimal('2280.00'),
            descuento=Decimal('500.00'),
            total_con_iva=Decimal('13780.00'),
            canal_venta='Instagram',
            folio='F001-00002'
        )
        Detalle_Venta.objects.create(
            venta_id=venta2,
            producto_id=productos[3],  # Torta chocolate
            cantidad=1,
            precio_unitario=productos[3].precio
        )

        # Venta 3
        venta3 = Ventas.objects.create(
            cliente_id=clientes[2],
            total_sin_iva=Decimal('6800.00'),
            total_iva=Decimal('1292.00'),
            descuento=Decimal('0.00'),
            total_con_iva=Decimal('8092.00'),
            canal_venta='WhatsApp',
            folio='F001-00003'
        )
        Detalle_Venta.objects.create(
            venta_id=venta3,
            producto_id=productos[6],  # Empanada pino
            cantidad=3,
            precio_unitario=productos[6].precio
        )
        Detalle_Venta.objects.create(
            venta_id=venta3,
            producto_id=productos[7],  # Empanada queso
            cantidad=2,
            precio_unitario=productos[7].precio
        )

        # Venta 4
        venta4 = Ventas.objects.create(
            cliente_id=clientes[3],
            total_sin_iva=Decimal('10000.00'),
            total_iva=Decimal('1900.00'),
            descuento=Decimal('0.00'),
            total_con_iva=Decimal('11900.00'),
            canal_venta='UberEats',
            folio='F001-00004'
        )
        Detalle_Venta.objects.create(
            venta_id=venta4,
            producto_id=productos[4],  # Torta tres leches
            cantidad=1,
            precio_unitario=productos[4].precio
        )

        # Venta 5
        venta5 = Ventas.objects.create(
            cliente_id=clientes[4],
            total_sin_iva=Decimal('4300.00'),
            total_iva=Decimal('817.00'),
            descuento=Decimal('200.00'),
            total_con_iva=Decimal('4917.00'),
            canal_venta='Local',
            folio='F001-00005',
            monto_pagado=Decimal('5000.00'),
            vuelto=Decimal('83.00')
        )
        Detalle_Venta.objects.create(
            venta_id=venta5,
            producto_id=productos[2],  # Pan amasado
            cantidad=2,
            precio_unitario=productos[2].precio
        )
        Detalle_Venta.objects.create(
            venta_id=venta5,
            producto_id=productos[10],  # Alfajor
            cantidad=2,
            precio_unitario=productos[10].precio
        )

        self.stdout.write(self.style.SUCCESS('   ✓ 5 ventas creadas con detalles\n'))

        # 8. Movimientos de Inventario
        self.stdout.write('📦 Creando movimientos de inventario...')
        Movimientos_Inventario.objects.create(
            producto_id=productos[0],
            tipo_movimiento='entrada',
            cantidad=100
        )
        Movimientos_Inventario.objects.create(
            producto_id=productos[0],
            tipo_movimiento='salida',
            cantidad=50
        )
        Movimientos_Inventario.objects.create(
            producto_id=productos[3],
            tipo_movimiento='entrada',
            cantidad=10
        )
        Movimientos_Inventario.objects.create(
            producto_id=productos[6],
            tipo_movimiento='salida',
            cantidad=20
        )
        self.stdout.write(self.style.SUCCESS('   ✓ 4 movimientos de inventario creados\n'))

        # 9. Alertas
        self.stdout.write('⚠️  Creando alertas...')
        Alertas.objects.all().delete()
        Alertas.objects.create(
            producto_id=productos[3],  # Torta chocolate (stock bajo)
            tipo_alerta='Stock bajo',
            mensaje=f'El stock de {productos[3].nombre} está en el mínimo ({productos[3].stock_actual} unidades)'
        )
        Alertas.objects.create(
            producto_id=productos[8],  # Jugo (vencimiento próximo)
            tipo_alerta='Vencimiento próximo',
            mensaje=f'{productos[8].nombre} vence mañana ({productos[8].caducidad})'
        )
        Alertas.objects.create(
            producto_id=productos[6],  # Empanada (vencimiento próximo)
            tipo_alerta='Vencimiento próximo',
            mensaje=f'{productos[6].nombre} vence mañana ({productos[6].caducidad})'
        )
        self.stdout.write(self.style.SUCCESS('   ✓ 3 alertas creadas\n'))

        # 10. Usuarios del sistema
        self.stdout.write('👨‍💼 Creando usuarios del sistema...')
        Usuarios.objects.update_or_create(
            run='15678234-5',
            defaults={
                'nombres': 'Carlos',
                'paterno': 'Muñoz',
                'materno': 'Soto',
                'correo': 'carlos.munoz@forneria.cl',
                'fono': '+56912345678',
                'Direccion_id': dir1,
                'Roles_id': rol_vendedor,
            }
        )
        Usuarios.objects.update_or_create(
            run='16789345-6',
            defaults={
                'nombres': 'Roberto',
                'paterno': 'Lagos',
                'materno': 'Escobar',
                'correo': 'roberto.lagos@forneria.cl',
                'fono': '+56987654321',
                'Direccion_id': dir2,
                'Roles_id': rol_admin,
            }
        )
        self.stdout.write(self.style.SUCCESS('   ✓ Usuarios del sistema listos\n'))
        # 11. Configurar grupos y permisos según la EVA
        self.stdout.write('🔐 Configurando permisos de seguridad...')

        for group_name in ['Administrador', 'Editor', 'Lector']:
            Group.objects.filter(name=group_name).delete()

        admin_group = Group.objects.create(name='Administrador')
        editor_group = Group.objects.create(name='Editor')
        lector_group = Group.objects.create(name='Lector')

        ct_productos = ContentType.objects.get_for_model(Productos)
        ct_clientes = ContentType.objects.get_for_model(Clientes)
        ct_ventas = ContentType.objects.get_for_model(Ventas)

        admin_perms = Permission.objects.filter(content_type__in=[ct_productos, ct_clientes, ct_ventas])
        admin_group.permissions.add(*admin_perms)

        editor_perms = Permission.objects.filter(
            Q(content_type=ct_productos, codename__in=['add_productos', 'change_productos', 'view_productos']) |
            Q(content_type=ct_ventas, codename__in=['add_ventas', 'change_ventas', 'view_ventas']) |
            Q(content_type=ct_clientes, codename='view_clientes')
        )
        editor_group.permissions.add(*editor_perms)

        lector_perms = Permission.objects.filter(
            Q(content_type=ct_productos, codename='view_productos') |
            Q(content_type=ct_clientes, codename='view_clientes') |
            Q(content_type=ct_ventas, codename='view_ventas')
        )
        lector_group.permissions.add(*lector_perms)

        self.stdout.write(self.style.SUCCESS('   ✓ Grupos Administrador, Editor y Lector configurados'))

        # 12. Usuarios demo para probar permisos
        editor_user, created = User.objects.get_or_create(
            username='editor_maria',
            defaults={
                'email': 'editor@forneria.cl',
                'first_name': 'María',
                'is_staff': True,
                'is_superuser': False,
            }
        )
        if created:
            editor_user.set_password('Editor123!')
            editor_user.save()
        editor_user.groups.set([editor_group])

        lector_user, created = User.objects.get_or_create(
            username='lector_pedro',
            defaults={
                'email': 'lector@forneria.cl',
                'first_name': 'Pedro',
                'is_staff': False,
                'is_superuser': False,
            }
        )
        if created:
            lector_user.set_password('Lector123!')
            lector_user.save()
        lector_user.groups.set([lector_group])

        self.stdout.write(self.style.SUCCESS('   ✓ Usuarios demo configurados: editor_maria (Editor), lector_pedro (Lector)'))

        # Resumen final (ajusta los textos como prefieras)
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('✅ ¡DATOS CARGADOS EXITOSAMENTE!'))
        self.stdout.write('='*60 + '\n')
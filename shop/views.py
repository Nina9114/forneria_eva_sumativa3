from datetime import datetime, time
from decimal import Decimal

from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from openpyxl import Workbook
from .decorators import permission_or_redirect, admin_required, groups_required
from .models import Productos, Clientes, Ventas, Detalle_Venta, Alertas, Categorias, UserProfile, Nutricional
from .forms import (
    UserForm,
    UserProfileForm,
    CustomPasswordChangeForm,
    CustomSetPasswordForm,
    ProductoForm,
    VentaForm,
    DetalleVentaFormSet,
)


def _get_productos_info():
    info = []
    for producto in Productos.objects.all():
        info.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'presentacion': producto.presentacion or '',
            'formato': producto.formato or '',
            'stock': producto.stock_actual or 0,
        })
    return info


# ============= AUTENTICACIÓN Y SESIONES =============

def login_view(request):
    """Vista de login personalizada"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Regenerar la clave de sesión para prevenir fijación
            request.session.cycle_key()

            # Configurar datos de sesión específicos
            request.session['forneria_user_id'] = user.id
            request.session['forneria_username'] = user.username
            request.session['forneria_login_time'] = timezone.now().isoformat()

            # Contador de visitas
            visitas = request.session.get('visitas_forneria', 0)
            request.session['visitas_forneria'] = visitas + 1

            messages.success(request, f'¡Bienvenido/a {user.first_name or user.username}!')

            if user.is_superuser or user.groups.filter(name='Administrador').exists():
                return redirect('forneria:dashboard_admin')
            if user.groups.filter(name='Editor').exists():
                return redirect('forneria:dashboard_vendedor')
            if user.groups.filter(name='Lector').exists():
                return redirect('forneria:productos_list')

            return redirect('forneria:dashboard_admin')

        messages.error(request, 'Credenciales incorrectas.')

    return render(request, 'shop/login.html')
def logout_view(request):
    """Vista de logout personalizada"""
    # Limpiar datos específicos
    request.session.pop('forneria_user_id', None)
    request.session.pop('forneria_username', None)
    request.session.pop('forneria_login_time', None)
    request.session.pop('carrito_forneria', None)
    
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('forneria:login')


@login_required
def dashboard_admin(request):
    """Dashboard para administradores"""
    total_productos = Productos.objects.count()
    total_clientes = Clientes.objects.count()
    ventas_hoy = Ventas.objects.filter(fecha__date=timezone.now().date()).count()
    alertas_pendientes = Alertas.objects.filter(estado='pendiente').count()
    
    context = {
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'ventas_hoy': ventas_hoy,
        'alertas_pendientes': alertas_pendientes,
    }
    
    return render(request, 'shop/dashboard_admin.html', context)


@login_required
def dashboard_vendedor(request):
    """Dashboard para vendedores"""
    total_productos = Productos.objects.count()
    ventas_hoy = Ventas.objects.filter(fecha__date=timezone.now().date()).count()
    
    context = {
        'total_productos': total_productos,
        'ventas_hoy': ventas_hoy,
    }
    
    return render(request, 'shop/dashboard_vendedor.html', context)


@login_required
def session_info(request):
    """Información de la sesión actual"""
    session_data = {
        'user_id': request.session.get('forneria_user_id'),
        'username': request.session.get('forneria_username'),
        'login_time': request.session.get('forneria_login_time'),
        'visitas': request.session.get('visitas_forneria', 0),
        'session_key': request.session.session_key,
    }
    
    return render(request, 'shop/session_info.html', {'session_data': session_data})


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('forneria:perfil')
        else:
            messages.error(request, 'Revisa los campos, algunos datos no son válidos.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
    }
    return render(request, 'shop/profile.html', context)


@login_required
def clear_session_data(request):
    """Limpiar datos temporales de la sesión"""
    request.session.pop('carrito_forneria', None)
    request.session.pop('visitas_forneria', None)
    
    messages.success(request, 'Datos temporales limpiados.')
    return redirect('forneria:session_info')


# ============= CRUD PRODUCTOS =============

@login_required
@permission_or_redirect('shop.view_productos', 'forneria:dashboard_vendedor', 'No puedes acceder al listado de productos.')
def productos_list(request):
    per_page_choices = [5, 15, 30]
    per_page_session_key = 'productos_per_page'
    per_page_param = request.GET.get('per_page')

    if per_page_param and per_page_param.isdigit():
        per_page_value = int(per_page_param)
        if per_page_value in per_page_choices:
            request.session[per_page_session_key] = per_page_value
            per_page = per_page_value
        else:
            per_page = request.session.get(per_page_session_key, per_page_choices[1])
    else:
        per_page = request.session.get(per_page_session_key, per_page_choices[1])

    search = (request.GET.get('search') or '').strip()
    categoria_id = request.GET.get('categoria')
    tipo = (request.GET.get('tipo') or '').strip()
    order_param = request.GET.get('order', '-creado')

    allowed_orders = {
        'nombre': 'nombre',
        '-nombre': '-nombre',
        'precio': 'precio',
        '-precio': '-precio',
        'stock_actual': 'stock_actual',
        '-stock_actual': '-stock_actual',
        'creado': 'creado',
        '-creado': '-creado',
    }
    if order_param not in allowed_orders:
        order_param = '-creado'
    order_by = allowed_orders[order_param]

    productos_qs = Productos.objects.select_related('Categorias_id').all()

    if search:
        productos_qs = productos_qs.filter(
            Q(nombre__icontains=search)
            | Q(marca__icontains=search)
            | Q(descripcion__icontains=search)
            | Q(Categorias_id__nombre__icontains=search)
        )

    if categoria_id and categoria_id.isdigit():
        productos_qs = productos_qs.filter(Categorias_id_id=int(categoria_id))

    if tipo:
        productos_qs = productos_qs.filter(tipo__iexact=tipo)

    productos_qs = productos_qs.order_by(order_by)

    if request.GET.get('export') == 'xlsx':
        return _export_productos_excel(productos_qs)

    paginator = Paginator(productos_qs, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)
    querystring = query_params.urlencode()

    query_params_no_order = query_params.copy()
    query_params_no_order.pop('order', None)
    base_query = query_params_no_order.urlencode()

    def _next_order(field):
        if order_param == field:
            return f'-{field}'
        if order_param == f'-{field}':
            return field
        return field

    sortable_fields = ['nombre', 'precio', 'stock_actual', 'creado']
    next_orders = {field: _next_order(field) for field in sortable_fields}

    order_states = {}
    for field in sortable_fields:
        if order_param == field:
            order_states[field] = 'asc'
        elif order_param == f'-{field}':
            order_states[field] = 'desc'
        else:
            order_states[field] = None

    export_params = query_params.copy()
    export_params['export'] = 'xlsx'
    export_url = f"?{export_params.urlencode()}" if export_params else '?export=xlsx'

    categorias = Categorias.objects.all().order_by('nombre')
    tipos_disponibles = list(
        Productos.objects.order_by('tipo')
        .values_list('tipo', flat=True)
        .distinct()
    )
    tipos_disponibles = [t for t in tipos_disponibles if t]

    context = {
        'page_obj': page_obj,
        'total_resultados': paginator.count,
        'search': search,
        'categoria_selected': int(categoria_id) if categoria_id and categoria_id.isdigit() else None,
        'tipo_selected': tipo,
        'categorias': categorias,
        'tipos': tipos_disponibles,
        'per_page': per_page,
        'per_page_choices': per_page_choices,
        'order_param': order_param,
        'next_orders': next_orders,
        'order_states': order_states,
        'querystring': querystring,
        'base_query': base_query,
        'export_url': export_url,
        'user_can_add': request.user.has_perm('shop.add_productos'),
        'user_can_change': request.user.has_perm('shop.change_productos'),
        'user_can_delete': request.user.has_perm('shop.delete_productos'),
    }

    return render(request, 'shop/productos_list.html', context)
@login_required
@permission_or_redirect('shop.add_productos', 'forneria:productos_list', "No puedes crear productos.")
def productos_create(request):
    form = ProductoForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            producto = form.save(commit=False)
            if not producto.Nutricional_id_id:
                nutricional = Nutricional.objects.first()
                if nutricional is None:
                    messages.error(request, 'Debes crear al menos un perfil nutricional antes de registrar productos.')
                    return render(request, 'shop/productos_create.html', {
                        'form': form,
                        'title': 'Crear nuevo producto',
                        'submit_label': 'Crear producto',
                    })
                producto.Nutricional_id = nutricional
            producto.save()
            messages.success(request, mark_safe(f'Producto "{producto.nombre}" creado correctamente.'))
            return redirect('forneria:productos_detail', producto.id)
        messages.error(request, 'Revisa los campos, hay información no válida.')

    context = {
        'form': form,
        'title': 'Crear nuevo producto',
        'submit_label': 'Crear producto',
    }
    return render(request, 'shop/productos_create.html', context)


@login_required
@permission_or_redirect('shop.change_productos', 'forneria:productos_list', "No puedes editar productos.")
def productos_edit(request, producto_id):
    producto = get_object_or_404(Productos, id=producto_id)
    form = ProductoForm(request.POST or None, instance=producto)

    if request.method == 'POST':
        if form.is_valid():
            producto = form.save()
            messages.success(request, mark_safe(f'Producto "{producto.nombre}" actualizado correctamente.'))
            return redirect('forneria:productos_detail', producto.id)
        messages.error(request, 'Revisa los campos, hay información no válida.')

    context = {
        'form': form,
        'producto': producto,
        'title': f'Editar producto: {producto.nombre}',
        'submit_label': 'Actualizar producto',
    }
    return render(request, 'shop/productos_edit.html', context)


@login_required
@permission_or_redirect('shop.delete_productos', 'forneria:productos_list', "No puedes eliminar productos.")
def productos_delete(request, producto_id):
    producto = get_object_or_404(Productos, id=producto_id)

    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, mark_safe(f'Producto "{nombre}" eliminado correctamente.'))
    else:
        messages.warning(request, 'La eliminación debe confirmarse desde los botones correspondientes.')

    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('forneria:productos_list')


@login_required
def productos_detail(request, producto_id):
    """
    Ver detalles de un producto
    """
    producto = get_object_or_404(Productos, id=producto_id)
    
    context = {
        'producto': producto,
        'user_can_change': request.user.has_perm('shop.change_productos'),
        'user_can_delete': request.user.has_perm('shop.delete_productos'),
        'user_can_add': request.user.has_perm('shop.add_productos'),
    }
    
    return render(request, 'shop/productos_detail.html', context)



def _export_productos_excel(queryset):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Productos'

    headers = [
        'Nombre',
        'Categoría',
        'Tipo',
        'Precio',
        'Stock actual',
        'Stock mínimo',
        'Stock máximo',
        'Fecha caducidad',
        'Fecha elaboración',
        'Fecha creación',
    ]
    worksheet.append(headers)

    for producto in queryset:
        if timezone.is_aware(producto.creado):
            created_display = timezone.localtime(producto.creado).strftime('%Y-%m-%d %H:%M')
        else:
            created_display = producto.creado.strftime('%Y-%m-%d %H:%M')

        worksheet.append([
            producto.nombre,
            producto.Categorias_id.nombre if getattr(producto, 'Categorias_id', None) else '',
            producto.tipo or '',
            float(producto.precio),
            producto.stock_actual if producto.stock_actual is not None else 0,
            producto.stock_minimo if producto.stock_minimo is not None else 0,
            producto.stock_maximo if producto.stock_maximo is not None else 0,
            producto.caducidad.strftime('%Y-%m-%d') if producto.caducidad else '',
            producto.elaboracion.strftime('%Y-%m-%d') if producto.elaboracion else '',
            created_display,
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"productos_{timezone.now().strftime('%Y%m%d_%H%M%S')}"
    response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
    workbook.save(response)
    return response


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('forneria:password_change_done')

    def form_valid(self, form):
        messages.success(self.request, 'Tu contraseña se actualizó correctamente.')
        return super().form_valid(form)


class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('forneria:password_reset_done')

    def form_valid(self, form):
        messages.info(self.request, 'Si el correo existe, recibirás un enlace para restablecer tu contraseña.')
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['email'].widget.attrs.setdefault('class', 'form-control')
        return form


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('forneria:password_reset_complete')

    def form_valid(self, form):
        messages.success(self.request, 'Tu nueva contraseña ha sido creada correctamente.')
        return super().form_valid(form)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
# ============= CRUD VENTAS =============

@login_required
@permission_or_redirect('shop.view_ventas', 'forneria:dashboard_vendedor', 'No puedes acceder al listado de ventas.')
def ventas_list(request):
    per_page_choices = [5, 15, 30]
    per_page_session_key = 'ventas_per_page'
    per_page_param = request.GET.get('per_page')

    if per_page_param and per_page_param.isdigit():
        per_page_value = int(per_page_param)
        if per_page_value in per_page_choices:
            request.session[per_page_session_key] = per_page_value
            per_page = per_page_value
        else:
            per_page = request.session.get(per_page_session_key, per_page_choices[1])
    else:
        per_page = request.session.get(per_page_session_key, per_page_choices[1])

    search = (request.GET.get('search') or '').strip()
    canal = (request.GET.get('canal') or '').strip()
    order_param = request.GET.get('order', '-fecha')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    allowed_orders = {
        'fecha': 'fecha',
        '-fecha': '-fecha',
        'total_con_iva': 'total_con_iva',
        '-total_con_iva': '-total_con_iva',
    }
    if order_param not in allowed_orders:
        order_param = '-fecha'
    order_by = allowed_orders[order_param]

    ventas_qs = Ventas.objects.select_related('cliente_id').prefetch_related('detalles__producto_id').all()

    if search:
        ventas_qs = ventas_qs.filter(
            Q(folio__icontains=search)
            | Q(cliente_id__nombre__icontains=search)
            | Q(cliente_id__correo__icontains=search)
        )

    if canal:
        ventas_qs = ventas_qs.filter(canal_venta=canal)

    def _parse_fecha(value):
        if not value:
            return None
        value = value.strip()
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y'):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        return None

    fecha_inicio_dt = _parse_fecha(fecha_inicio)
    fecha_fin_dt = _parse_fecha(fecha_fin)
    tz = timezone.get_current_timezone()

    if fecha_inicio_dt:
        inicio_dt = datetime.combine(fecha_inicio_dt, time.min)
        if timezone.is_naive(inicio_dt):
            inicio_dt = timezone.make_aware(inicio_dt, tz)
        ventas_qs = ventas_qs.filter(fecha__gte=inicio_dt)
    elif fecha_inicio:
        messages.warning(request, 'Fecha de inicio inválida, se omitió el filtro.')

    if fecha_fin_dt:
        fin_dt = datetime.combine(fecha_fin_dt, time.max)
        if timezone.is_naive(fin_dt):
            fin_dt = timezone.make_aware(fin_dt, tz)
        ventas_qs = ventas_qs.filter(fecha__lte=fin_dt)
    elif fecha_fin:
        messages.warning(request, 'Fecha de término inválida, se omitió el filtro.')

    fecha_inicio_value = fecha_inicio_dt.strftime('%Y-%m-%d') if fecha_inicio_dt else (fecha_inicio or '')
    fecha_fin_value = fecha_fin_dt.strftime('%Y-%m-%d') if fecha_fin_dt else (fecha_fin or '')

    ventas_qs = ventas_qs.order_by(order_by)

    if request.GET.get('export') == 'xlsx':
        return _export_ventas_excel(ventas_qs)

    paginator = Paginator(ventas_qs, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)
    querystring = query_params.urlencode()

    query_params_no_order = query_params.copy()
    query_params_no_order.pop('order', None)
    base_query = query_params_no_order.urlencode()

    def _next_order(field):
        if order_param == field:
            return f'-{field}'
        if order_param == f'-{field}':
            return field
        return field

    sortable_fields = ['fecha', 'total_con_iva']
    next_orders = {field: _next_order(field) for field in sortable_fields}

    order_states = {}
    for field in sortable_fields:
        if order_param == field:
            order_states[field] = 'asc'
        elif order_param == f'-{field}':
            order_states[field] = 'desc'
        else:
            order_states[field] = None

    export_params = query_params.copy()
    export_params['export'] = 'xlsx'
    export_url = f"?{export_params.urlencode()}" if export_params else '?export=xlsx'

    context = {
        'page_obj': page_obj,
        'total_resultados': paginator.count,
        'search': search,
        'canal_selected': canal,
        'canal_choices': Ventas.CANAL_CHOICES,
        'fecha_inicio': fecha_inicio_value,
        'fecha_fin': fecha_fin_value,
        'per_page': per_page,
        'per_page_choices': per_page_choices,
        'order_param': order_param,
        'next_orders': next_orders,
        'order_states': order_states,
        'querystring': querystring,
        'base_query': base_query,
        'export_url': export_url,
        'user_can_add': request.user.has_perm('shop.add_ventas'),
        'user_can_change': request.user.has_perm('shop.change_ventas'),
        'user_can_delete': request.user.has_perm('shop.delete_ventas'),
    }

    return render(request, 'shop/ventas_list.html', context)


def _calcular_totales(venta, detalles):
    subtotal = Decimal('0.00')
    for detalle in detalles:
        if detalle.cantidad and detalle.precio_unitario:
            linea = Decimal(detalle.cantidad) * detalle.precio_unitario
            descuento_pct = detalle.descuento_pct or Decimal('0')
            linea = linea * (Decimal('1') - descuento_pct / Decimal('100'))
            subtotal += linea
    subtotal = subtotal.quantize(Decimal('0.01'))
    iva = (subtotal * Decimal('0.19')).quantize(Decimal('0.01'))
    descuento = venta.descuento or Decimal('0.00')
    total_con_iva = (subtotal + iva - descuento).quantize(Decimal('0.01'))
    if total_con_iva < Decimal('0.00'):
        total_con_iva = Decimal('0.00')
    return subtotal, iva, total_con_iva


@login_required
@permission_or_redirect('shop.add_ventas', 'forneria:ventas_list', 'No puedes crear ventas.')
def ventas_create(request):
    venta = Ventas()
    form = VentaForm(request.POST or None, instance=venta)
    formset = DetalleVentaFormSet(request.POST or None, instance=venta, prefix='detalles')

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            return _guardar_venta(request, form, formset, venta, 'Venta registrada correctamente.')
        messages.error(request, 'Revisa los campos del formulario de venta y sus detalles.')

    context = {
        'form': form,
        'formset': formset,
        'title': 'Registrar venta',
        'submit_label': 'Guardar venta',
        'productos_info': _get_productos_info(),
    }
    return render(request, 'shop/ventas_form.html', context)


@login_required
@permission_or_redirect('shop.change_ventas', 'forneria:ventas_list', 'No puedes editar ventas.')
def ventas_edit(request, venta_id):
    venta = get_object_or_404(Ventas, id=venta_id)
    form = VentaForm(request.POST or None, instance=venta)
    formset = DetalleVentaFormSet(request.POST or None, instance=venta, prefix='detalles')

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            return _guardar_venta(request, form, formset, venta, 'Venta actualizada correctamente.')
        messages.error(request, 'Revisa los campos del formulario de venta y sus detalles.')

    context = {
        'form': form,
        'formset': formset,
        'venta': venta,
        'title': f'Editar venta #{venta.id}',
        'submit_label': 'Actualizar venta',
        'productos_info': _get_productos_info(),
    }
    return render(request, 'shop/ventas_form.html', context)


@login_required
@permission_or_redirect('shop.delete_ventas', 'forneria:ventas_list', 'No puedes eliminar ventas.')
def ventas_delete(request, venta_id):
    venta = get_object_or_404(Ventas, id=venta_id)

    if request.method == 'POST':
        folio = venta.folio or venta.id
        venta.delete()
        messages.success(request, f'Venta "{folio}" eliminada correctamente.')
    else:
        messages.warning(request, 'La eliminación debe confirmarse desde los botones correspondientes.')

    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('forneria:ventas_list')


@login_required
@permission_or_redirect('shop.view_ventas', 'forneria:ventas_list', 'No puedes ver los detalles de ventas.')
def ventas_detail(request, venta_id):
    venta = get_object_or_404(Ventas.objects.select_related('cliente_id'), id=venta_id)
    detalles = venta.detalles.select_related('producto_id').all()

    detalles_info = []
    for detalle in detalles:
        subtotal = Decimal(detalle.cantidad) * detalle.precio_unitario
        descuento_pct = detalle.descuento_pct or Decimal('0')
        subtotal = subtotal * (Decimal('1') - descuento_pct / Decimal('100'))
        subtotal = subtotal.quantize(Decimal('0.01'))
        detalles_info.append({'registro': detalle, 'subtotal': subtotal})

    context = {
        'venta': venta,
        'detalles_info': detalles_info,
        'user_can_change': request.user.has_perm('shop.change_ventas'),
        'user_can_delete': request.user.has_perm('shop.delete_ventas'),
        'user_can_add': request.user.has_perm('shop.add_ventas'),
    }
    return render(request, 'shop/ventas_detail.html', context)


def _guardar_venta(request, form, formset, venta, success_message):
    with transaction.atomic():
        venta = form.save(commit=False)
        descuento = form.cleaned_data.get('descuento') or Decimal('0.00')
        venta.descuento = descuento

        # Valores por defecto para evitar columnas NOT NULL en el primer guardado
        if venta.total_sin_iva is None:
            venta.total_sin_iva = Decimal('0.00')
        if venta.total_iva is None:
            venta.total_iva = Decimal('0.00')
        if venta.total_con_iva is None:
            venta.total_con_iva = Decimal('0.00')
        if venta.monto_pagado is None:
            venta.monto_pagado = Decimal('0.00')
        if venta.vuelto is None:
            venta.vuelto = Decimal('0.00')

        venta.save()

        detalles = formset.save(commit=False)
        for detalle in formset.deleted_objects:
            detalle.delete()

        for detalle in detalles:
            detalle.venta_id = venta
            detalle.save()

        subtotal, iva, total_con_iva = _calcular_totales(venta, venta.detalles.all())
        venta.total_sin_iva = subtotal
        venta.total_iva = iva
        venta.total_con_iva = total_con_iva

        monto_pagado = form.cleaned_data.get('monto_pagado')
        if monto_pagado is None:
            monto_pagado = total_con_iva
        venta.monto_pagado = Decimal(monto_pagado).quantize(Decimal('0.01'))
        venta.vuelto = (venta.monto_pagado - total_con_iva).quantize(Decimal('0.01'))
        if venta.vuelto < Decimal('0.00'):
            venta.vuelto = Decimal('0.00')

        venta.save()

        if not venta.folio:
            venta.folio = f"VENT-{venta.id:05d}"
            venta.save(update_fields=['folio'])

    messages.success(request, success_message)
    return redirect('forneria:ventas_detail', venta.id)


def _export_ventas_excel(queryset):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Ventas'

    headers = [
        'ID',
        'Folio',
        'Fecha',
        'Cliente',
        'Canal',
        'Total sin IVA',
        'IVA',
        'Descuento',
        'Total con IVA',
        'Monto pagado',
        'Vuelto',
    ]
    worksheet.append(headers)

    for venta in queryset:
        fecha = timezone.localtime(venta.fecha) if timezone.is_aware(venta.fecha) else venta.fecha
        worksheet.append([
            venta.id,
            venta.folio or '',
            fecha.strftime('%Y-%m-%d %H:%M'),
            venta.cliente_id.nombre if venta.cliente_id else '',
            venta.get_canal_venta_display(),
            float(venta.total_sin_iva or 0),
            float(venta.total_iva or 0),
            float(venta.descuento or 0),
            float(venta.total_con_iva or 0),
            float(venta.monto_pagado or 0),
            float(venta.vuelto or 0),
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"ventas_{timezone.now().strftime('%Y%m%d_%H%M%S')}"
    response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
    workbook.save(response)
    return response

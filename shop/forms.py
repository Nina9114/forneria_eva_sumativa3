import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.utils import timezone

from .models import (
    UserProfile,
    Productos,
    Ventas,
    Detalle_Venta,
    Clientes,
    Categorias,
    Nutricional,
)


class UserForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombre', max_length=150, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Apellido', max_length=150, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Correo electrónico', required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserProfileForm(forms.ModelForm):
    phone = forms.CharField(label='Teléfono', max_length=20, required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(label='Avatar', required=False,
                              widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ('phone', 'avatar')


class PasswordRulesMixin:
    def _validate_password_strength(self, password):
        errors = []
        if len(password) < 8:
            errors.append('La contraseña debe tener al menos 8 caracteres.')
        if not re.search(r'[A-Z]', password):
            errors.append('La contraseña debe incluir al menos una letra mayúscula.')
        if not re.search(r'\d', password):
            errors.append('La contraseña debe incluir al menos un número.')
        if errors:
            raise ValidationError(errors)


class CustomPasswordChangeForm(PasswordRulesMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def clean_new_password2(self):
        password2 = super().clean_new_password2()
        self._validate_password_strength(password2)
        return password2


class CustomSetPasswordForm(PasswordRulesMixin, SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def clean_new_password2(self):
        password2 = super().clean_new_password2()
        self._validate_password_strength(password2)
        return password2


class ProductoForm(forms.ModelForm):
    TIPO_CHOICES = [
        ('propia', 'Preparación propia'),
        ('envasado', 'Producto envasado'),
    ]

    tipo = forms.ChoiceField(choices=TIPO_CHOICES, label='Tipo',
                             widget=forms.Select(attrs={'class': 'form-select'}))
    caducidad = forms.DateField(label='Fecha de caducidad',
                                widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    elaboracion = forms.DateField(label='Fecha de elaboración', required=False,
                                  widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Productos
        fields = [
            'nombre', 'marca', 'descripcion', 'precio', 'Categorias_id', 'tipo',
            'caducidad', 'elaboracion', 'stock_actual', 'stock_minimo', 'stock_maximo',
            'presentacion', 'formato'
        ]
        labels = {
            'Categorias_id': 'Categoría',
            'stock_actual': 'Stock actual',
            'stock_minimo': 'Stock mínimo',
            'stock_maximo': 'Stock máximo',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'Categorias_id': forms.Select(attrs={'class': 'form-select'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'stock_maximo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'presentacion': forms.TextInput(attrs={'class': 'form-control'}),
            'formato': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise ValidationError('El precio debe ser mayor a 0.')
        return precio

    def clean(self):
        cleaned = super().clean()
        caducidad = cleaned.get('caducidad')
        elaboracion = cleaned.get('elaboracion')
        stock_minimo = cleaned.get('stock_minimo')
        stock_maximo = cleaned.get('stock_maximo')
        stock_actual = cleaned.get('stock_actual')

        if caducidad and elaboracion and caducidad <= elaboracion:
            self.add_error('caducidad', 'La fecha de caducidad debe ser posterior a la elaboración.')

        if stock_minimo is not None and stock_maximo is not None and stock_minimo >= stock_maximo:
            self.add_error('stock_minimo', 'El stock mínimo debe ser menor que el stock máximo.')

        if stock_actual is not None and stock_actual < 0:
            self.add_error('stock_actual', 'El stock actual no puede ser negativo.')

        return cleaned


class VentaForm(forms.ModelForm):
    fecha = forms.DateTimeField(
        label='Fecha de venta',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    cliente_id = forms.ModelChoiceField(
        queryset=Clientes.objects.all(),
        label='Cliente',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    canal_venta = forms.ChoiceField(
        choices=Ventas.CANAL_CHOICES,
        label='Canal de venta',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    descuento = forms.DecimalField(
        label='Descuento',
        required=False,
        min_value=0,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    monto_pagado = forms.DecimalField(
        label='Monto pagado',
        required=False,
        min_value=0,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )

    class Meta:
        model = Ventas
        fields = ['cliente_id', 'fecha', 'canal_venta', 'folio', 'descuento', 'monto_pagado']
        widgets = {
            'folio': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['folio'].required = False
        if self.instance.pk and self.instance.fecha and not self.data:
            self.initial['fecha'] = timezone.localtime(self.instance.fecha).strftime('%Y-%m-%dT%H:%M')
        elif not self.instance.pk and not self.data and 'fecha' not in self.initial:
            self.initial['fecha'] = timezone.now().strftime('%Y-%m-%dT%H:%M')

    def clean_folio(self):
        folio = self.cleaned_data.get('folio')
        if not folio:
            return folio
        qs = Ventas.objects.filter(folio=folio)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Ya existe una venta con este folio.')
        return folio


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = Detalle_Venta
        fields = ['producto_id', 'cantidad', 'precio_unitario', 'descuento_pct']
        labels = {
            'producto_id': 'Producto',
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio unitario',
            'descuento_pct': 'Descuento (%)',
        }
        widgets = {
            'producto_id': forms.Select(attrs={'class': 'form-select js-producto-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control js-cantidad-input', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control js-precio-input', 'step': '0.01', 'min': '0'}),
            'descuento_pct': forms.NumberInput(attrs={'class': 'form-control js-descuento-input', 'step': '0.01', 'min': '0', 'max': '100'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['precio_unitario'].required = False

    def clean(self):
        cleaned = super().clean()
        producto = cleaned.get('producto_id')
        cantidad = cleaned.get('cantidad')
        precio = cleaned.get('precio_unitario')
        descuento = cleaned.get('descuento_pct')

        if cantidad is not None and cantidad <= 0:
            self.add_error('cantidad', 'La cantidad debe ser mayor a 0.')

        if precio in (None, '') and producto is not None:
            cleaned['precio_unitario'] = producto.precio
            precio = producto.precio

        if precio is None or precio <= 0:
            self.add_error('precio_unitario', 'El precio unitario debe ser mayor a 0.')

        if descuento is not None and (descuento < 0 or descuento > 100):
            self.add_error('descuento_pct', 'El descuento debe estar entre 0 y 100%.')

        return cleaned


DetalleVentaFormSet = inlineformset_factory(
    Ventas,
    Detalle_Venta,
    form=DetalleVentaForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)

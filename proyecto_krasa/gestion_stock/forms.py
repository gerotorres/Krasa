from django import forms
from .models import Producto, Venta
from gestion_stock.models import Cliente, Proveedor, Marca, Categoria, Subcategoria, FormaPago, Venta

class ProductoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        empty_label="Selecciona una categoría",
        required=False
    )
    
    subcategoria = forms.ModelChoiceField(
        queryset=Subcategoria.objects.all(),
        empty_label="Selecciona una subcategoría",
        required=False
    )
    
    marca = forms.ModelChoiceField(
        queryset=Marca.objects.all(),
        empty_label="Selecciona una marca",
        required=False
    )

    proveedor = forms.ModelChoiceField(  
        queryset=Proveedor.objects.all(),
        empty_label="Selecciona un proveedor",
        required=False
    )

    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'precio', 'stock', 
            'categoria', 'subcategoria', 'codigo_barras', 
            'ubicacion_deposito', 'marca', 'proveedor'
        ]

# 📌 Formulario para Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'direccion', 'telefono', 'email', 'localidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'localidad': forms.Select(attrs={'class': 'form-control'}),
        }

# 📌 Formulario para Proveedor
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'direccion', 'telefono', 'email', 'localidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'localidad': forms.Select(attrs={'class': 'form-control'}),
        }

# 📌 Formulario para Marca
class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la Marca'}),
        }

# 📌 Formulario para Categoría
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la Categoría'}),
        }

# 📌 Formulario para Subcategoría
class SubcategoriaForm(forms.ModelForm):
    class Meta:
        model = Subcategoria
        fields = ['nombre', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la Subcategoría'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

# 📌 Formulario para Venta
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'total']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total'}),
        }

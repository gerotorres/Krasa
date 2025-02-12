from django.contrib import admin
from .models import (
    Categoria, Subcategoria, Producto, Cliente, Proveedor, Venta, Compra,
    DetalleVenta, DetalleCompra, Pais, Provincia, Localidad, Empleado
)

# Registramos todos los modelos en el admin de Django
admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(Venta)
admin.site.register(Compra)
admin.site.register(DetalleVenta)
admin.site.register(DetalleCompra)
admin.site.register(Pais)
admin.site.register(Provincia)
admin.site.register(Localidad)
admin.site.register(Empleado)

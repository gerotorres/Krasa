from django.urls import path
from django.views.generic import TemplateView
from gestion_stock.views.cliente_view import ClienteListaView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView
from gestion_stock.views.proveedor_view import ProveedorListaView, ProveedorCreateView, ProveedorUpdateView, ProveedorDeleteView, agregar_proveedor
from gestion_stock.views.producto_view import ProductoListaView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView 
from gestion_stock.views.marca_view import MarcaListaView, MarcaCreateView, MarcaUpdateView, MarcaDeleteView, agregar_marca
from gestion_stock.views.categoria_view import CategoriaListaView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView, agregar_categoria, agregar_subcategoria
from gestion_stock.views.subcategoria_view import SubcategoriaListaView, SubcategoriaCreateView, SubcategoriaUpdateView, SubcategoriaDeleteView
from gestion_stock.views.venta_views import VentaListaView, VentaCreateView, VentaUpdateView, VentaDeleteView
from gestion_stock.views.localidad_view import listar_localidades
from gestion_stock.views.codigo_barras import verificar_codigo_barras


urlpatterns = [
    # 📌 URLs para Clientes
    path('clientes/', ClienteListaView.as_view(), name='cliente_lista'),
    path('clientes/crear/', ClienteCreateView.as_view(), name='cliente_crear'),
    path('clientes/editar/<int:id>/', ClienteUpdateView.as_view(), name='cliente_editar'),
    path('clientes/eliminar/<int:id>/', ClienteDeleteView.as_view(), name='cliente_eliminar'),

    # 📌 URLs para Proveedores
    path('proveedores/', ProveedorListaView.as_view(), name='proveedor_lista'),
    path('proveedores/crear/', ProveedorCreateView.as_view(), name='proveedor_crear'),
    path('proveedores/editar/<int:id>/', ProveedorUpdateView.as_view(), name='proveedor_editar'),
    path('proveedores/eliminar/<int:id>/', ProveedorDeleteView.as_view(), name='proveedor_eliminar'),
    path('agregar_proveedor/', agregar_proveedor, name= 'agregar_proveedor'),

    # 📌 URLs para Productos
    path('productos/', ProductoListaView.as_view(), name='producto_lista'),
    path('productos/crear/', ProductoCreateView.as_view(), name='producto_crear'),
    path('productos/editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto_editar'),
    path('productos/eliminar/<int:id>/', ProductoDeleteView.as_view(), name='producto_eliminar'),

    # 📌 URLs para Marcas
    path('marcas/', MarcaListaView.as_view(), name='marca_lista'),
    path('marcas/crear/', MarcaCreateView.as_view(), name='marca_crear'),
    path('marcas/editar/<int:id>/', MarcaUpdateView.as_view(), name='marca_editar'),
    path('marcas/eliminar/<int:id>/', MarcaDeleteView.as_view(), name='marca_eliminar'),
    path("agregar_marca/", agregar_marca, name="agregar_marca"),

    # 📌 URLs para Categorías
    path('categorias/', CategoriaListaView.as_view(), name='categoria_list'),
    path('categorias/crear/', CategoriaCreateView.as_view(), name='categoria_crear'),
    path('categorias/editar/<int:id>/', CategoriaUpdateView.as_view(), name='categoria_editar'),
    path('categorias/eliminar/<int:id>/', CategoriaDeleteView.as_view(), name='categoria_eliminar'),
    path("agregar_categoria/", agregar_categoria, name="agregar_categoria"),
    

    # 📌 URLs para Subcategorías
    path('subcategorias/', SubcategoriaListaView.as_view(), name='subcategoria_lista'),
    path('subcategorias/crear/', SubcategoriaCreateView.as_view(), name='subcategoria_crear'),
    path('subcategorias/editar/<int:id>/', SubcategoriaUpdateView.as_view(), name='subcategoria_editar'),
    path('subcategorias/eliminar/<int:id>/', SubcategoriaDeleteView.as_view(), name='subcategoria_eliminar'),
    path('subcategoria/agregar/', agregar_subcategoria, name='agregar_subcategoria'),

    # 📌 URLs para Ventas
    path('ventas/', VentaListaView.as_view(), name='venta_lista'),
    path('ventas/crear/', VentaCreateView.as_view(), name='venta_crear'),
    path('ventas/editar/<int:id>/', VentaUpdateView.as_view(), name='venta_editar'),
    path('ventas/eliminar/<int:id>/', VentaDeleteView.as_view(), name='venta_eliminar'),

    path("listar_localidades/", listar_localidades, name="listar_localidades"),
    path('verificar_codigo_barras/', verificar_codigo_barras, name='verificar_codigo_barras'),

    # 📌 URL para la página principal (Index)
    path('', TemplateView.as_view(template_name='home/index.html'), name='index'),
]

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from datetime import datetime
from django.db.models import Q

from gestion_stock.forms import ProductoForm  # Corregido
from gestion_stock.models import Producto, Categoria, Subcategoria, Marca  # Corregido
from gestion_stock.repositories.producto import ProductoRepository
from gestion_stock.repositories.categoria import CategoriaRepository
from gestion_stock.repositories.subcategoria import SubcategoriaRepository
from gestion_stock.repositories.marca import MarcaRepository

producto_repo = ProductoRepository()
categoria_repo = CategoriaRepository()
subcategoria_repo = SubcategoriaRepository()
marca_repo = MarcaRepository()

class ProductoListaView(View):
    def get(self, request):
        categoria_id = request.GET.get('categoria')
        query = request.GET.get('q')  # Captura el término de búsqueda

        if categoria_id:
            productos = producto_repo.get_by_categoria(categoria_id)
        else:
            productos = producto_repo.get_all()

        if query:  # Si hay una búsqueda, filtra los productos
            productos = producto_repo.search(query)

        categorias = categoria_repo.get_all()
        productos_mas_vendidos = producto_repo.get_mas_vendidos_semana(limit=5)
        productos_stock_bajo = producto_repo.get_stock_bajo(threshold=3)

        return render(
            request,
            'productos/list.html',
            {
                'productos': productos,
                'categorias': categorias,
                'productos_mas_vendidos': productos_mas_vendidos,
                'productos_stock_bajo': productos_stock_bajo,
                'current_time': datetime.now().strftime('%H:%M:%S'),
            }
        )

class ProductoDeleteView(View):
    def get(self, request, id):
        producto = producto_repo.get_by_id(id=id)
        if producto:
            producto_repo.delete(producto=producto)
        return redirect('producto_lista')

class ProductoCreateView(View):
    def get(self, request):
        form = ProductoForm()
        categorias = categoria_repo.get_all()
        subcategorias = subcategoria_repo.get_all()
        marcas = marca_repo.get_all()

        return render(
            request,
            'productos/create.html',
            {
                'form': form,
                'categorias': categorias,
                'subcategorias': subcategorias,
                'marcas': marcas,
            }
        )

    def post(self, request, *args, **kwargs):
        form = ProductoForm(request.POST)  # Define form antes de usarlo
        categorias = categoria_repo.get_all()
        subcategorias = subcategoria_repo.get_all()
        marcas = marca_repo.get_all()

        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            descripcion = form.cleaned_data["descripcion"]
            precio = form.cleaned_data["precio"]
            stock = form.cleaned_data["stock"]
            categoria_id = form.cleaned_data["categoria"].id if form.cleaned_data["categoria"] else None
            subcategoria_id = form.cleaned_data["subcategoria"].id if form.cleaned_data["subcategoria"] else None
            codigo_barras = form.cleaned_data["codigo_barras"]
            ubicacion_deposito = form.cleaned_data["ubicacion_deposito"]
            marca_id = form.cleaned_data["marca"].id if form.cleaned_data["marca"] else None

            categoria = Categoria.objects.get(id=categoria_id) if categoria_id else None
            subcategoria = Subcategoria.objects.get(id=subcategoria_id) if subcategoria_id else None
            marca = Marca.objects.get(id=marca_id) if marca_id else None

            Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                stock=stock,
                categoria=categoria,
                subcategoria=subcategoria,
                codigo_barras=codigo_barras,
                ubicacion_deposito=ubicacion_deposito,
                marca=marca,
            )

            return redirect("producto_lista")  

        return render(
            request,
            "productos/create.html",
            {
                "form": form,
                "categorias": categorias,
                "subcategorias": subcategorias,
                "marcas": marcas,
            }
        )

@method_decorator(login_required(login_url='login'), name='dispatch')
class ProductoUpdateView(View):
    def get(self, request, id):
        producto = producto_repo.get_by_id(id)  # Corregido
        if not producto:
            return redirect('producto_lista')  # Evitar error si no existe

        form = ProductoForm(instance=producto)

        categorias = categoria_repo.get_all()
        subcategorias = subcategoria_repo.get_all()
        marcas = marca_repo.get_all()

        return render(
            request,
            'productos/update.html',
            {
                'form': form,
                'categorias': categorias,
                'subcategorias': subcategorias,
                'marcas': marcas,
            }
        )

    def post(self, request, id):
        producto = producto_repo.get_by_id(id)  # Corregido
        if not producto:
            return redirect('producto_lista')

        form = ProductoForm(request.POST, instance=producto)

        if form.is_valid():
            producto_repo.update(
                producto=producto,
                nombre=form.cleaned_data['nombre'],
                descripcion=form.cleaned_data['descripcion'],
                precio=form.cleaned_data['precio'],
                stock=form.cleaned_data['stock'],
                categoria=form.cleaned_data['categoria'],
                subcategoria=form.cleaned_data['subcategoria'],
                codigo_barras=form.cleaned_data['codigo_barras'],
                ubicacion_deposito=form.cleaned_data['ubicacion_deposito'],
                marca=form.cleaned_data['marca'],
            )
            return redirect('producto_lista')

        categorias = categoria_repo.get_all()
        subcategorias = subcategoria_repo.get_all()
        marcas = marca_repo.get_all()

        return render(
            request,
            'productos/update.html',
            {
                'form': form,
                'categorias': categorias,
                'subcategorias': subcategorias,
                'marcas': marcas,
            }
        )

class ProductoComentariosView(View):
    def get(self, request, id):
        producto = producto_repo.get_by_id(id)
        if not producto:
            return redirect('producto_lista')

        comentarios = producto.comentarios.all() if hasattr(producto, 'comentarios') else []

        return render(
            request,
            'productos/comentarios.html',
            {
                'producto': producto,
                'comentarios': comentarios
            }
        )

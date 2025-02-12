from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from datetime import datetime

from gestion_stock.forms import ProductoForm  # Corregido
from gestion_stock.models import Producto  # Corregido
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

        if categoria_id:
            productos = producto_repo.get_by_categoria(categoria_id)
        else:
            productos = producto_repo.get_all()

        categorias = categoria_repo.get_all()

        return render(
            request,
            'productos/list.html',
            {
                'productos': productos,
                'categorias': categorias,
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

    def post(self, request):
        form = ProductoForm(request.POST)
        if form.is_valid():
            categoria = categoria_repo.get_by_id(form.cleaned_data['categoria'])
            subcategoria = subcategoria_repo.get_by_id(form.cleaned_data['subcategoria'])
            marca = marca_repo.get_by_id(form.cleaned_data['marca'])

            producto_repo.create(
                nombre=form.cleaned_data['nombre'],
                descripcion=form.cleaned_data['descripcion'],
                precio=form.cleaned_data['precio'],
                stock=form.cleaned_data['stock'],
                categoria=categoria,
                subcategoria=subcategoria,
                codigo_barras=form.cleaned_data['codigo_barras'],
                ubicacion_deposito=form.cleaned_data['ubicacion_deposito'],
                marca=marca,
            )
            return redirect('producto_lista')

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

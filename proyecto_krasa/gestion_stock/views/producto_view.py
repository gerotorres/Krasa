from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from datetime import datetime
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from gestion_stock.forms import ProductoForm  # Corregido
from gestion_stock.models import Producto, Categoria, Subcategoria, Marca, Proveedor
from gestion_stock.repositories.producto import ProductoRepository
from gestion_stock.repositories.categoria import CategoriaRepository
from gestion_stock.repositories.subcategoria import SubcategoriaRepository
from gestion_stock.repositories.marca import MarcaRepository
from gestion_stock.repositories.proveedor import ProveedorRepository

producto_repo = ProductoRepository()
categoria_repo = CategoriaRepository()
subcategoria_repo = SubcategoriaRepository()
marca_repo = MarcaRepository()
proveedor_repo = ProveedorRepository()

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
    def post(self, request, id):
        producto = get_object_or_404(Producto, id=id)  # Obtiene el producto o lanza un error 404
        producto.delete()  # Elimina el producto
        messages.success(request, "El producto ha sido eliminado correctamente.")  # Mensaje de éxito
        return redirect('producto_lista')  # Redirige a la lista de productos

class ProductoCreateView(View):
    def get(self, request):
        form = ProductoForm()
        categorias = categoria_repo.get_all()
        subcategorias = subcategoria_repo.get_all()
        marcas = marca_repo.get_all()
        proveedores =proveedor_repo.get_all()


        return render(
            request,
            'productos/create.html',
            {
                'form': form,
                'categorias': categorias,
                'subcategorias': subcategorias,
                'marcas': marcas,
                'proveedores': proveedores,
            }
        )

    def post(self, request, *args, **kwargs):
        form = ProductoForm(request.POST)
        categorias = categoria_repo.get_all()
        subcategorias = subcategoria_repo.get_all()
        marcas = marca_repo.get_all()
        proveedores =proveedor_repo.get_all()

        if form.is_valid():
            codigo_barras = form.cleaned_data["codigo_barras"]

            # Verificar si ya existe un producto con ese código de barras
            if Producto.objects.filter(codigo_barras=codigo_barras).exists():
                messages.error(request, "⚠️ El producto con este código de barras ya existe.")
            else:
                producto = form.save(commit=False)  # No guardar aún para asignar relaciones
                producto.categoria = Categoria.objects.get(id=form.cleaned_data["categoria"].id) if form.cleaned_data["categoria"] else None
                producto.subcategoria = Subcategoria.objects.get(id=form.cleaned_data["subcategoria"].id) if form.cleaned_data["subcategoria"] else None
                producto.marca = Marca.objects.get(id=form.cleaned_data["marca"].id) if form.cleaned_data["marca"] else None
                producto.proveedores = Proveedor.objects.get(id=form.cleaned_data["proveedor"].id) if form.cleaned_data["proveedor"] else None
                
                producto.save()
                messages.success(request, "✅ Producto agregado correctamente.")
                return redirect("producto_lista")  

        return render(
            request,
            "productos/create.html",
            {
                "form": form,
                "categorias": categorias,
                "subcategorias": subcategorias,
                "marcas": marcas,
                'proveedores':  proveedores,
            }
        )

@method_decorator(login_required(login_url='login'), name='dispatch')
class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/update.html"
    success_url = reverse_lazy("producto_lista")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = categoria_repo.get_all()
        context["subcategorias"] = subcategoria_repo.get_all()
        context["marcas"] = marca_repo.get_all()
        context["proveedores"] = proveedor_repo.get_all()
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Asegurar que los valores iniciales se establezcan correctamente
        form.fields["nombre"].initial = self.object.nombre
        form.fields["descripcion"].initial = self.object.descripcion
        form.fields["precio"].initial = self.object.precio
        form.fields["categoria"].initial = self.object.categoria
        form.fields["subcategoria"].initial = self.object.subcategoria
        form.fields["codigo_barras"].initial = self.object.codigo_barras
        form.fields["ubicacion_deposito"].initial = self.object.ubicacion_deposito
        form.fields["marca"].initial = self.object.marca
        form.fields["proveedor"].initial = self.object.proveedor
        return form

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        stock_original = self.object.stock  # Mantener el stock original
        
        form = self.get_form()
        if form.is_valid():
            producto_actualizado = form.save(commit=False)
            
            # Llamar al repositorio asegurando que 'stock' no cambie
            producto_repo.update(
                producto_actualizado.id,
                producto_actualizado.nombre,
                producto_actualizado.descripcion,
                producto_actualizado.precio,
                producto_actualizado.categoria,
                producto_actualizado.subcategoria,
                producto_actualizado.codigo_barras,
                producto_actualizado.ubicacion_deposito,
                producto_actualizado.marca,
                stock_original,
                producto_actualizado.proveedor
            )

            messages.success(request, "¡Producto actualizado correctamente!")
            return redirect(self.success_url)

        messages.error(request, "Error al actualizar el producto.")
        return self.form_invalid(form)

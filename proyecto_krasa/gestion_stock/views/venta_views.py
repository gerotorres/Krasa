from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from gestion_stock.forms import VentaForm  # Asegúrate de que este formulario exista
from gestion_stock.repositories.venta import VentaRepository
from gestion_stock.repositories.cliente import ClienteRepository
from gestion_stock.repositories.producto import ProductoRepository

venta_repo = VentaRepository()
cliente_repo = ClienteRepository()
producto_repo = ProductoRepository()

class VentaListaView(View):
    def get(self, request):
        ventas = venta_repo.get_all()
        return render(request, 'ventas/venta_list.html', {'ventas': ventas})

class VentaCreateView(View):
    def get(self, request):
        form = VentaForm()
        clientes = cliente_repo.get_all()
        productos = producto_repo.get_all()
        return render(request, 'ventas/venta_create.html', {
            'form': form,
            'clientes': clientes,
            'productos': productos,
        })

    def post(self, request):
        form = VentaForm(request.POST)
        if form.is_valid():
            cliente = cliente_repo.get_by_id(form.cleaned_data['cliente'].id)
            producto = producto_repo.get_by_id(form.cleaned_data['producto'].id)
            cantidad = form.cleaned_data['cantidad']
            total = form.cleaned_data['total']

            venta_repo.create(cliente=cliente, producto=producto, cantidad=cantidad, total=total)
            return redirect('venta_lista')

        clientes = cliente_repo.get_all()
        productos = producto_repo.get_all()
        return render(request, 'ventas/venta_create.html', {
            'form': form,
            'clientes': clientes,
            'productos': productos,
        })

class VentaUpdateView(View):
    def get(self, request, id):
        venta = get_object_or_404(venta_repo.get_all(), id=id)
        form = VentaForm(instance=venta)
        clientes = cliente_repo.get_all()
        productos = producto_repo.get_all()
        return render(request, 'ventas/venta_update.html', {
            'form': form,
            'clientes': clientes,
            'productos': productos,
        })

    def post(self, request, id):
        venta = get_object_or_404(venta_repo.get_all(), id=id)
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            venta_repo.update(
                venta=venta,
                cliente=form.cleaned_data['cliente'],
                producto=form.cleaned_data['producto'],
                cantidad=form.cleaned_data['cantidad'],
                total=form.cleaned_data['total'],
            )
            return redirect('venta_lista')

        clientes = cliente_repo.get_all()
        productos = producto_repo.get_all()
        return render(request, 'ventas/venta_update.html', {
            'form': form,
            'clientes': clientes,
            'productos': productos,
        })

class VentaDeleteView(View):
    def get(self, request, id):
        venta = venta_repo.get_by_id(id)
        if venta:
            venta_repo.delete(venta)
        return redirect('venta_lista')

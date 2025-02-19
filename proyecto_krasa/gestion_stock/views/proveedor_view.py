from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from gestion_stock.repositories.proveedor import ProveedorRepository
from gestion_stock.forms import ProveedorForm
from gestion_stock.models import Proveedor, Localidad
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

repo = ProveedorRepository()

@csrf_exempt
def agregar_proveedor(request):
    if request.method == "POST":
        data = json.loads(request.body)
        proveedor = Proveedor.objects.create(
            nombre=data.get("nombre"),
            direccion=data.get("direccion", ""),
            telefono=data.get("telefono", ""),
            email=data.get("email", ""),
            localidad=Localidad.objects.get(id=data["localidad"]) if data.get("localidad") else None
        )
        return JsonResponse({"id": proveedor.id, "nombre": proveedor.nombre})
    return JsonResponse({"error": "Método no permitido"}, status=405)
        
class ProveedorListaView(View):
    def get(self, request):
        proveedores = repo.get_all()
        return render(
            request,
            'proveedores/proveedor_list.html',
            {'proveedores': proveedores}
        )

class ProveedorCreateView(View):
    def get(self, request):
        form = ProveedorForm()
        return render(
            request,
            'proveedores/proveedor_create.html',
            {'form': form}
        )

    def post(self, request):
        form = ProveedorForm(request.POST)
        if form.is_valid():
            repo.create(
                nombre=form.cleaned_data['nombre'],
                direccion=form.cleaned_data['direccion'],
                telefono=form.cleaned_data['telefono'],
                email=form.cleaned_data['email'],
                localidad=form.cleaned_data['localidad'],
            )
            return redirect('proveedor_lista')

        return render(
            request,
            'proveedores/proveedor_create.html',
            {'form': form}
        )

class ProveedorUpdateView(View):
    def get(self, request, id):
        proveedor = get_object_or_404(repo.get_all(), id=id)
        form = ProveedorForm(instance=proveedor)
        return render(
            request,
            'proveedores/proveedor_update.html',
            {'form': form}
        )

    def post(self, request, id):
        proveedor = get_object_or_404(repo.get_all(), id=id)
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            repo.update(
                proveedor=proveedor,
                nombre=form.cleaned_data['nombre'],
                direccion=form.cleaned_data['direccion'],
                telefono=form.cleaned_data['telefono'],
                email=form.cleaned_data['email'],
                localidad=form.cleaned_data['localidad'],
            )
            return redirect('proveedor_lista')

        return render(
            request,
            'proveedores/proveedor_update.html',
            {'form': form}
        )

class ProveedorDeleteView(View):
    def get(self, request, id):
        proveedor = repo.get_by_id(id=id)
        if proveedor:
            repo.delete(proveedor=proveedor)
        return redirect('proveedor_lista')

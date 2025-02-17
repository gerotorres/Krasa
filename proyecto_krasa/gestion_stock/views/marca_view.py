from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from gestion_stock.forms import MarcaForm  # Asegúrate de que este formulario exista
from gestion_stock.repositories.marca import MarcaRepository
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gestion_stock.models import Marca
import json

repo = MarcaRepository()

@csrf_exempt
def agregar_marca(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nombre = data.get("nombre")

            if not nombre:
                return JsonResponse({"error": "El nombre de la marca es obligatorio"}, status=400)

            if Marca.objects.filter(nombre=nombre).exists():
                return JsonResponse({"error": "Esta marca ya existe"}, status=400)

            nueva_marca = Marca.objects.create(nombre=nombre)
            return JsonResponse({"id": nueva_marca.id, "nombre": nueva_marca.nombre})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)
class MarcaListaView(View):
    def get(self, request):
        marcas = repo.get_all()
        return render(request, 'productos/marca_list.html', {'marcas': marcas})

class MarcaCreateView(View):
    def get(self, request):
        form = MarcaForm()
        return render(request, 'productos/marca_create.html', {'form': form})

    def post(self, request):
        form = MarcaForm(request.POST)
        if form.is_valid():
            repo.create(nombre=form.cleaned_data['nombre'])
            return redirect('marca_lista')
        return render(request, 'productos/marca_create.html', {'form': form})

class MarcaUpdateView(View):
    def get(self, request, id):
        marca = get_object_or_404(repo.get_all(), id=id)
        form = MarcaForm(instance=marca)
        return render(request, 'productos/marca_update.html', {'form': form})

    def post(self, request, id):
        marca = get_object_or_404(repo.get_all(), id=id)
        form = MarcaForm(request.POST, instance=marca)
        if form.is_valid():
            repo.update(marca=marca, nombre=form.cleaned_data['nombre'])
            return redirect('marca_lista')
        return render(request, 'productos/marca_update.html', {'form': form})

class MarcaDeleteView(View):
    def get(self, request, id):
        marca = repo.get_by_id(id)
        if marca:
            repo.delete(marca)
        return redirect('marca_lista')

class IndexView(View):
    def get(self, request):
        return render(request, 'index/index.html')

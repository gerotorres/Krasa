from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from gestion_stock.repositories.categoria import CategoriaRepository
from gestion_stock.forms import CategoriaForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gestion_stock.models import Categoria, Subcategoria
import json
from django.urls import reverse
from django.http import HttpResponseForbidden

repo = CategoriaRepository()

def agregar_categoria(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Cargar JSON enviado desde el frontend
            nombre = data.get("nombre")
            if nombre:
                categoria, created = Categoria.objects.get_or_create(nombre=nombre)
                return JsonResponse({"id": categoria.id, "nombre": categoria.nombre})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def agregar_subcategoria(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nombre = data.get("nombre")
            categoria_id = data.get("categoria")

            if not nombre or not categoria_id:
                return JsonResponse({"error": "Faltan datos"}, status=400)

            categoria = Categoria.objects.filter(id=categoria_id).first()
            if not categoria:
                return JsonResponse({"error": "Categoría no encontrada"}, status=404)

            subcategoria, created = Subcategoria.objects.get_or_create(nombre=nombre, categoria=categoria)
            return JsonResponse({"id": subcategoria.id, "nombre": subcategoria.nombre, "categoria": categoria.nombre})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)

class CategoriaListaView(View):
    def get(self, request):
        categorias = repo.get_all()
        return render(
            request,
            'categorias/list.html',
            
            {'categorias': categorias}
        )

class CategoriaCreateView(View):
    def get(self, request):
        form = CategoriaForm()
        categorias = repo.get_all()  # Obtener las categorías
        return render(
            request,
            'categorias/list.html',
            {'form': form, 'categorias': categorias}  # Pasar las categorías al template
        )

    def post(self, request):
        form = CategoriaForm(request.POST)
        categorias = repo.get_all()  # Obtener las categorías también en POST
        if form.is_valid():
            repo.create(nombre=form.cleaned_data['nombre'])
            return redirect('categoria_list')

        return render(
            request,
            'categorias/list.html',
            {'form': form, 'categorias': categorias}  # Asegurar que se pasen las categorías
        )

class CategoriaUpdateView(View):
    def get(self, request, id):
        categoria = get_object_or_404(repo.get_all(), id=id)
        form = CategoriaForm(instance=categoria)
        return render(
            request,
            'categorias/update.html',
            {'form': form}
        )

    def post(self, request, id):
        categoria = get_object_or_404(repo.get_all(), id=id)
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            repo.update(categoria=categoria, nombre=form.cleaned_data['nombre'])
            return redirect('categoria_list')

        return render(
            request,
            'categorias/update.html',
            {'form': form}
        )


class CategoriaDeleteView(View):
    def post(self, request, id):
        categoria = repo.get_by_id(id=id)  
        if categoria:
            repo.delete(categoria=categoria)  
        return redirect(reverse('categoria_list')) 

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from gestion_stock.forms import MarcaForm  # Asegúrate de que este formulario exista
from gestion_stock.repositories.marca import MarcaRepository

repo = MarcaRepository()

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

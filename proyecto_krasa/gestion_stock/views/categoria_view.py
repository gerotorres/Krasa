from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from gestion_stock.repositories.categoria import CategoriaRepository
from gestion_stock.forms import CategoriaForm

repo = CategoriaRepository()

class CategoriaListaView(View):
    def get(self, request):
        categorias = repo.get_all()
        return render(
            request,
            'categorias/categoria_list.html',
            {'categorias': categorias}
        )

class CategoriaCreateView(View):
    def get(self, request):
        form = CategoriaForm()
        return render(
            request,
            'categorias/categoria_create.html',
            {'form': form}
        )

    def post(self, request):
        form = CategoriaForm(request.POST)
        if form.is_valid():
            repo.create(nombre=form.cleaned_data['nombre'])
            return redirect('categoria_lista')

        return render(
            request,
            'categorias/categoria_create.html',
            {'form': form}
        )

class CategoriaUpdateView(View):
    def get(self, request, id):
        categoria = get_object_or_404(repo.get_all(), id=id)
        form = CategoriaForm(instance=categoria)
        return render(
            request,
            'categorias/categoria_update.html',
            {'form': form}
        )

    def post(self, request, id):
        categoria = get_object_or_404(repo.get_all(), id=id)
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            repo.update(categoria=categoria, nombre=form.cleaned_data['nombre'])
            return redirect('categoria_lista')

        return render(
            request,
            'categorias/categoria_update.html',
            {'form': form}
        )

class CategoriaDeleteView(View):
    def get(self, request, id):
        categoria = repo.get_by_id(id=id)
        if categoria:
            repo.delete(categoria=categoria)
        return redirect('categoria_lista')

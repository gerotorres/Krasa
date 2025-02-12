from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from gestion_stock.repositories.subcategoria import SubcategoriaRepository
from gestion_stock.forms import SubcategoriaForm
from gestion_stock.repositories.categoria import CategoriaRepository

repo = SubcategoriaRepository()
categoria_repo = CategoriaRepository()

class SubcategoriaListaView(View):
    def get(self, request):
        subcategorias = repo.get_all()
        return render(
            request,
            'subcategorias/subcategoria_list.html',
            {'subcategorias': subcategorias}
        )

class SubcategoriaCreateView(View):
    def get(self, request):
        form = SubcategoriaForm()
        categorias = categoria_repo.get_all()
        return render(
            request,
            'subcategorias/subcategoria_create.html',
            {'form': form, 'categorias': categorias}
        )

    def post(self, request):
        form = SubcategoriaForm(request.POST)
        if form.is_valid():
            categoria = categoria_repo.get_by_id(form.cleaned_data['categoria'].id)
            repo.create(nombre=form.cleaned_data['nombre'], categoria=categoria)
            return redirect('subcategoria_lista')

        categorias = categoria_repo.get_all()
        return render(
            request,
            'subcategorias/subcategoria_create.html',
            {'form': form, 'categorias': categorias}
        )

class SubcategoriaUpdateView(View):
    def get(self, request, id):
        subcategoria = get_object_or_404(repo.get_all(), id=id)
        form = SubcategoriaForm(instance=subcategoria)
        categorias = categoria_repo.get_all()
        return render(
            request,
            'subcategorias/subcategoria_update.html',
            {'form': form, 'categorias': categorias}
        )

    def post(self, request, id):
        subcategoria = get_object_or_404(repo.get_all(), id=id)
        form = SubcategoriaForm(request.POST, instance=subcategoria)
        if form.is_valid():
            categoria = categoria_repo.get_by_id(form.cleaned_data['categoria'].id)
            repo.update(subcategoria=subcategoria, nombre=form.cleaned_data['nombre'], categoria=categoria)
            return redirect('subcategoria_lista')

        categorias = categoria_repo.get_all()
        return render(
            request,
            'subcategorias/subcategoria_update.html',
            {'form': form, 'categorias': categorias}
        )

class SubcategoriaDeleteView(View):
    def get(self, request, id):
        subcategoria = repo.get_by_id(id=id)
        if subcategoria:
            repo.delete(subcategoria=subcategoria)
        return redirect('subcategoria_lista')

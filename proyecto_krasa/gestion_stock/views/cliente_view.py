from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from gestion_stock.repositories.cliente import ClienteRepository
from gestion_stock.forms import ClienteForm

repo = ClienteRepository()

class ClienteListaView(View):
    def get(self, request):
        clientes = repo.get_all()
        return render(
            request,
            'clientes/cliente_list.html',
            {'clientes': clientes}
        )

class ClienteCreateView(View):
    def get(self, request):
        form = ClienteForm()
        return render(
            request,
            'clientes/cliente_create.html',
            {'form': form}
        )

    def post(self, request):
        form = ClienteForm(request.POST)
        if form.is_valid():
            repo.create(
                nombre=form.cleaned_data['nombre'],
                direccion=form.cleaned_data['direccion'],
                telefono=form.cleaned_data['telefono'],
                email=form.cleaned_data['email'],
                localidad=form.cleaned_data['localidad'],
            )
            return redirect('cliente_lista')

        return render(
            request,
            'clientes/cliente_create.html',
            {'form': form}
        )

class ClienteUpdateView(View):
    def get(self, request, id):
        cliente = get_object_or_404(repo.get_all(), id=id)
        form = ClienteForm(instance=cliente)
        return render(
            request,
            'clientes/cliente_update.html',
            {'form': form}
        )

    def post(self, request, id):
        cliente = get_object_or_404(repo.get_all(), id=id)
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            repo.update(
                cliente=cliente,
                nombre=form.cleaned_data['nombre'],
                direccion=form.cleaned_data['direccion'],
                telefono=form.cleaned_data['telefono'],
                email=form.cleaned_data['email'],
                localidad=form.cleaned_data['localidad'],
            )
            return redirect('cliente_lista')

        return render(
            request,
            'clientes/cliente_update.html',
            {'form': form}
        )

class ClienteDeleteView(View):
    def get(self, request, id):
        cliente = repo.get_by_id(id=id)
        if cliente:
            repo.delete(cliente=cliente)
        return redirect('cliente_lista')

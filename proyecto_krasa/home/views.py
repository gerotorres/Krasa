from django.shortcuts import render

# Create your views here.
from django.contrib.auth import (
    authenticate,
    login, 
    logout,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views import View

from usuarios.forms import UserRegisterForm
from django.contrib import messages 
 
from django.db.models import Count
from gestion_stock.models import Producto, Venta
class LoginView(View):
    def get(self, request):
        return render(request, 'home/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                messages.warning(request, 'Nombre de usuario o contraseña incorrectos.')

        return render(request, 'home/login.html')
    



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class RegisterView(View):
    form_class = UserRegisterForm
    template_name = 'home/register.html'

    def get(self, request):
        form = self.form_class()
        return render(
            request,
            self.template_name,
            dict(
                form=form
            )
        )
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')

        return render(
            request,
            self.template_name,
            dict(
                form=form
            )
        )

def home_view(request):
    # productos_mas_vendidos = (
    #     Venta.objects.values('producto__nombre')
    #     .annotate(ventas_semana=Count('id'))
    #     .order_by('-ventas_semana')[:5]
    # )

    productos_stock_bajo = Producto.objects.filter(stock__lt=3)
    print(productos_stock_bajo)  # Verifica si hay productos con stock bajo

    return render(request, 'home/index.html', {
        # 'productos_mas_vendidos': productos_mas_vendidos,
        'productos_stock_bajo': productos_stock_bajo,
    })

from django.http import JsonResponse
from gestion_stock.models import Producto

def verificar_codigo_barras(request):
    codigo_barras = request.GET.get('codigo_barras', None)
    existe = Producto.objects.filter(codigo_barras=codigo_barras).exists()
    return JsonResponse({'existe': existe})

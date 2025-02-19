from django.http import JsonResponse
from gestion_stock.models import Localidad

def listar_localidades(request):
    localidades = Localidad.objects.all().values("id", "nombre")
    return JsonResponse(list(localidades), safe=False)

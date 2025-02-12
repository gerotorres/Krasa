from typing import List, Optional
from gestion_stock.models import Marca

class MarcaRepository:

    def get_all(self) -> List[Marca]:
        return Marca.objects.all()

    def get_by_id(self, id: int) -> Optional[Marca]:
        try:
            marca = Marca.objects.get(id=id)
        except Marca.DoesNotExist:
            marca = None
        return marca

    def filter_by_nombre(self, nombre: str) -> List[Marca]:
        return Marca.objects.filter(nombre__icontains=nombre)

    def create(self, nombre: str) -> Marca:
        return Marca.objects.create(nombre=nombre)

    def update(self, marca: Marca, nombre: str) -> Marca:
        marca.nombre = nombre
        marca.save()
        return marca

    def delete(self, marca: Marca):
        return marca.delete()

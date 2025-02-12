from typing import List, Optional
from gestion_stock.models import Categoria

class CategoriaRepository:

    def get_all(self) -> List[Categoria]:
        return Categoria.objects.all()

    def get_by_id(self, id: int) -> Optional[Categoria]:
        try:
            categoria = Categoria.objects.get(id=id)
        except Categoria.DoesNotExist:
            categoria = None
        return categoria

    def filter_by_nombre(self, nombre: str) -> List[Categoria]:
        return Categoria.objects.filter(nombre__icontains=nombre)

    def create(self, nombre: str) -> Categoria:
        return Categoria.objects.create(nombre=nombre)

    def update(self, categoria: Categoria, nombre: str) -> Categoria:
        categoria.nombre = nombre
        categoria.save()
        return categoria

    def delete(self, categoria: Categoria):
        return categoria.delete()

from typing import List, Optional
from gestion_stock.models import Subcategoria, Categoria

class SubcategoriaRepository:

    def get_all(self) -> List[Subcategoria]:
        return Subcategoria.objects.all()

    def get_by_id(self, id: int) -> Optional[Subcategoria]:
        try:
            subcategoria = Subcategoria.objects.get(id=id)
        except Subcategoria.DoesNotExist:
            subcategoria = None
        return subcategoria

    def filter_by_nombre(self, nombre: str) -> List[Subcategoria]:
        return Subcategoria.objects.filter(nombre__icontains=nombre)

    def filter_by_categoria(self, categoria: Categoria) -> List[Subcategoria]:
        return Subcategoria.objects.filter(categoria=categoria)

    def create(self, nombre: str, categoria: Categoria) -> Subcategoria:
        return Subcategoria.objects.create(nombre=nombre, categoria=categoria)

    def update(self, subcategoria: Subcategoria, nombre: str, categoria: Categoria) -> Subcategoria:
        subcategoria.nombre = nombre
        subcategoria.categoria = categoria
        subcategoria.save()
        return subcategoria

    def delete(self, subcategoria: Subcategoria):
        return subcategoria.delete()

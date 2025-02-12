from typing import List, Optional
from gestion_stock.models import Proveedor, Localidad

class ProveedorRepository:

    def get_all(self) -> List[Proveedor]:
        return Proveedor.objects.all()

    def get_by_id(self, id: int) -> Optional[Proveedor]:
        try:
            proveedor = Proveedor.objects.get(id=id)
        except Proveedor.DoesNotExist:
            proveedor = None
        return proveedor

    def filter_by_nombre(self, nombre: str) -> List[Proveedor]:
        return Proveedor.objects.filter(nombre__icontains=nombre)

    def filter_by_localidad(self, localidad: Localidad) -> List[Proveedor]:
        return Proveedor.objects.filter(localidad=localidad)

    def create(
        self, 
        nombre: str, 
        direccion: Optional[str] = None, 
        telefono: Optional[str] = None, 
        email: Optional[str] = None, 
        localidad: Optional[Localidad] = None
    ) -> Proveedor:
        return Proveedor.objects.create(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            email=email,
            localidad=localidad
        )

    def update(
        self, 
        proveedor: Proveedor, 
        nombre: str, 
        direccion: Optional[str] = None, 
        telefono: Optional[str] = None, 
        email: Optional[str] = None, 
        localidad: Optional[Localidad] = None
    ) -> Proveedor:
        proveedor.nombre = nombre
        proveedor.direccion = direccion
        proveedor.telefono = telefono
        proveedor.email = email
        proveedor.localidad = localidad
        proveedor.save()
        return proveedor

    def delete(self, proveedor: Proveedor):
        return proveedor.delete()

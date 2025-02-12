from typing import List, Optional
from gestion_stock.models import Cliente, Localidad

class ClienteRepository:
    
    def get_all(self) -> List[Cliente]:
        return Cliente.objects.all()

    def get_by_id(self, id: int) -> Optional[Cliente]:
        try:
            cliente = Cliente.objects.get(id=id)
        except Cliente.DoesNotExist:
            cliente = None
        return cliente

    def filter_by_nombre(self, nombre: str) -> List[Cliente]:
        return Cliente.objects.filter(nombre__icontains=nombre)

    def filter_by_localidad(self, localidad: Localidad) -> List[Cliente]:
        return Cliente.objects.filter(localidad=localidad)

    def create(
        self,
        nombre: str,
        direccion: Optional[str] = None,
        telefono: Optional[str] = None,
        email: Optional[str] = None,
        localidad: Optional[Localidad] = None,
    ) -> Cliente:
        return Cliente.objects.create(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            email=email,
            localidad=localidad,
        )

    def update(
        self,
        cliente: Cliente,
        nombre: str,
        direccion: Optional[str] = None,
        telefono: Optional[str] = None,
        email: Optional[str] = None,
        localidad: Optional[Localidad] = None,
    ) -> Cliente:
        cliente.nombre = nombre
        cliente.direccion = direccion
        cliente.telefono = telefono
        cliente.email = email
        cliente.localidad = localidad
        cliente.save()
        return cliente

    def delete(self, cliente: Cliente):
        return cliente.delete()

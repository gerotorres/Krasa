from typing import List, Optional
from gestion_stock.models import Empleado, Usuario

class EmpleadoRepository:

    def get_all(self) -> List[Empleado]:
        return Empleado.objects.all()

    def get_by_id(self, id: int) -> Optional[Empleado]:
        try:
            empleado = Empleado.objects.get(id=id)
        except Empleado.DoesNotExist:
            empleado = None
        return empleado

    def filter_by_nombre(self, nombre: str) -> List[Empleado]:
        return Empleado.objects.filter(nombre__icontains=nombre)

    def filter_by_apellido(self, apellido: str) -> List[Empleado]:
        return Empleado.objects.filter(apellido__icontains=apellido)

    def filter_by_usuario(self, usuario: Usuario) -> Optional[Empleado]:
        try:
            return Empleado.objects.get(usuario=usuario)
        except Empleado.DoesNotExist:
            return None

    def create(
        self, 
        nombre: str, 
        apellido: str, 
        direccion: Optional[str] = None, 
        telefono: Optional[str] = None, 
        email: Optional[str] = None, 
        usuario: Optional[Usuario] = None
    ) -> Empleado:
        return Empleado.objects.create(
            nombre=nombre,
            apellido=apellido,
            direccion=direccion,
            telefono=telefono,
            email=email,
            usuario=usuario
        )

    def update(
        self, 
        empleado: Empleado, 
        nombre: str, 
        apellido: str, 
        direccion: Optional[str] = None, 
        telefono: Optional[str] = None, 
        email: Optional[str] = None, 
        usuario: Optional[Usuario] = None
    ) -> Empleado:
        empleado.nombre = nombre
        empleado.apellido = apellido
        empleado.direccion = direccion
        empleado.telefono = telefono
        empleado.email = email
        empleado.usuario = usuario
        empleado.save()
        return empleado

    def delete(self, empleado: Empleado):
        return empleado.delete()

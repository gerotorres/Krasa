from typing import List, Optional
from gestion_stock.models import Venta, Cliente, FormaPago

class VentaRepository:

    def get_all(self) -> List[Venta]:
        return Venta.objects.all()

    def get_by_id(self, id: int) -> Optional[Venta]:
        try:
            venta = Venta.objects.get(id=id)
        except Venta.DoesNotExist:
            venta = None
        return venta

    def filter_by_cliente(self, cliente: Cliente) -> List[Venta]:
        return Venta.objects.filter(cliente=cliente)

    def filter_by_forma_pago(self, forma_pago: FormaPago) -> List[Venta]:
        return Venta.objects.filter(forma_pago=forma_pago)

    def filter_by_fecha(self, fecha: str) -> List[Venta]:
        return Venta.objects.filter(fecha__date=fecha)

    def create(
        self,
        cliente: Optional[Cliente],
        total: float,
        forma_pago: Optional[FormaPago] = None
    ) -> Venta:
        return Venta.objects.create(
            cliente=cliente,
            total=total,
            forma_pago=forma_pago
        )

    def update(
        self,
        venta: Venta,
        cliente: Optional[Cliente],
        total: float,
        forma_pago: Optional[FormaPago] = None
    ) -> Venta:
        venta.cliente = cliente
        venta.total = total
        venta.forma_pago = forma_pago
        venta.save()
        return venta

    def delete(self, venta: Venta):
        return venta.delete()

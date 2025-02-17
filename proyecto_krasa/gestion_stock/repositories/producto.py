from typing import List, Optional
from gestion_stock.models import Producto, Categoria, Subcategoria, Marca, DetalleVenta
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum, Q

class ProductoRepository:

    def get_all(self) -> List[Producto]:
        return Producto.objects.all()

    def filter_by_id(self, id: int) -> Optional[Producto]:
        return Producto.objects.filter(id=id).first()
    
    def get_by_id(self, id: int) -> Optional[Producto]:
        try:
            return Producto.objects.get(id=id)
        except Producto.DoesNotExist:
            return None

    def get_productos_in_price_range(self, min_price: float, max_price: float) -> List[Producto]:
        return Producto.objects.filter(precio__range=(min_price, max_price))


    def get_mas_vendidos_semana(self, limit=5):
        semana_pasada = now() - timedelta(days=7)
        productos_mas_vendidos = (
            DetalleVenta.objects
            .filter(venta__fecha__gte=semana_pasada)
            .values('producto__id', 'producto__nombre')
            .annotate(ventas_semana=Sum('cantidad'))
            .order_by('-ventas_semana')[:limit]
        )
        return productos_mas_vendidos

    def search_by_name_or_category(self, query):
        return Producto.objects.filter(
            Q(nombre__icontains=query) | Q(categoria__nombre__icontains=query)
        )
    def search(self, query):
        return Producto.objects.filter(
            Q(nombre__icontains=query) | 
            Q(descripcion__icontains=query) |
            Q(codigo_barras__icontains=query)
        )
        
    def get_stock_bajo(self, threshold=3):
        return Producto.objects.filter(stock__lt=threshold).order_by('stock')

    def create(
        self,
        nombre: str,
        descripcion: Optional[str],
        precio: float,
        stock: int,
        categoria: Optional[Categoria] = None,
        subcategoria: Optional[Subcategoria] = None,
        marca: Optional[Marca] = None,
        codigo_barras: Optional[str] = None,
        ubicacion_deposito: Optional[str] = None,
    ) -> Producto:
        return Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            categoria=categoria,
            subcategoria=subcategoria,
            marca=marca,
            codigo_barras=codigo_barras,
            ubicacion_deposito=ubicacion_deposito,
        )

    def filter_by_marca(self, marca: Marca) -> List[Producto]:
        return Producto.objects.filter(marca=marca)
    
    def get_by_marca(self, marca_id: int) -> List[Producto]:
        return Producto.objects.filter(marca_id=marca_id)

    def filter_by_categoria(self, categoria: Categoria) -> List[Producto]:
        
        return Producto.objects.filter(categoria=categoria)
    
    def get_by_categoria(self, categoria_id: int) -> List[Producto]:
        return Producto.objects.filter(categoria_id=categoria_id)

    def delete(self, producto: Producto):
        return producto.delete()
        
    @staticmethod
    def update(id, nombre, descripcion, precio, categoria, subcategoria, codigo_barras, ubicacion_deposito, marca, stock):
        producto = Producto.objects.get(id=id)
        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.precio = precio
        producto.categoria = categoria
        producto.subcategoria = subcategoria
        producto.codigo_barras = codigo_barras
        producto.ubicacion_deposito = ubicacion_deposito
        producto.marca = marca
        producto.stock = stock  # Asegurar que el stock no se modifique
        producto.save()
        return producto

from typing import List, Optional
from gestion_stock.models import Producto, Categoria, Subcategoria, Marca

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

    def update(
        self,
        producto: Producto,
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
        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.precio = precio
        producto.stock = stock
        producto.categoria = categoria
        producto.subcategoria = subcategoria
        producto.marca = marca
        producto.codigo_barras = codigo_barras
        producto.ubicacion_deposito = ubicacion_deposito
        
        producto.save()
        return producto

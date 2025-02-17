from django.db import models

from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = "categoria"
    
    def __str__(self):
        return self.nombre

class Subcategoria(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        db_table = "subcategoria"
    
    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    
    class Meta:
        db_table = "marca"
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200, null=False)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    stock = models.IntegerField(null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, null=True, blank=True)
    codigo_barras = models.CharField(max_length=20, unique=True, null=True, blank=True)
    ubicacion_deposito = models.CharField(max_length=255, blank=True, null=True)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True, blank=True)
    

    class Meta:
        db_table = "producto"
    
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=200, null=False)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    localidad = models.ForeignKey('Localidad', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = "cliente"
    
    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=200, null=False)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    localidad = models.ForeignKey('Localidad', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = "proveedor"
    
    def __str__(self):
        return self.nombre

class FormaPago(models.Model):
    tipo_pago = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "forma_pago"

    def __str__(self):
        return self.tipo_pago

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    forma_pago = models.ForeignKey(FormaPago, on_delete=models.SET_NULL, null=True) 

    class Meta:
        db_table = "venta"

    def __str__(self):
        return f"Venta {self.id} - Cliente: {self.cliente.nombre if self.cliente else 'Sin cliente'} - Pago: {self.forma_pago.descripcion if self.forma_pago else 'No especificado'}"

class Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    
    class Meta:
        db_table = "compra"
    
    def __str__(self):
        return f"Compra {self.id} - Proveedor: {self.proveedor.nombre if self.proveedor else 'Sin proveedor'}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    
    class Meta:
        db_table = "detalle_venta"
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} - Venta {self.venta.id}"

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    
    class Meta:
        db_table = "detalle_compra"
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} - Compra {self.compra.id}"

class Pais(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    
    class Meta:
        db_table = "pais"
    
    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "provincia"
    
    def __str__(self):
        return self.nombre

class Localidad(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "localidad"
    
    def __str__(self):
        return self.nombre


class Empleado(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    apellido = models.CharField(max_length=100, null=False)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = "empleado"
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

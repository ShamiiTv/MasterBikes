from django.db import models
from django.contrib.auth.models import User

class FormaPago(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Bicicleta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.FloatField()
    precio_dolar = models.FloatField(default=0.0)
    precio_arriendo = models.FloatField(default=0.0)
    src_imagen = models.CharField(default="./Images/Productos/", max_length=300)

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name="items", on_delete=models.CASCADE)
    bicicleta = models.ForeignKey(Bicicleta, on_delete=models.CASCADE, default=1)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.bicicleta.nombre}"

class Arriendo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    bicicleta = models.ForeignKey(Bicicleta, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    deposito_garantia = models.FloatField()
    forma_pago = models.ForeignKey(FormaPago, on_delete=models.CASCADE)

    def __str__(self):
        return f"Arriendo de {self.bicicleta.nombre} por {self.usuario.username}"

class Reparacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    bicicleta = models.CharField(max_length=100)  
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_programada = models.DateTimeField()
    descripcion_problema = models.TextField()
    estado = models.CharField(max_length=50, default='Pendiente')

    def __str__(self):
        return f"Reparación de {self.bicicleta} para {self.usuario.username}"

class Despacho(models.Model):
    bicicleta = models.ForeignKey(Bicicleta, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_despacho = models.DateTimeField()
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=50, default='En camino')

    def __str__(self):
        return f"Despacho de {self.bicicleta.nombre} para {self.usuario.username}"

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class PedidoProveedor(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    bicicleta = models.ForeignKey(Bicicleta, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField()

    def __str__(self):
        return f"Pedido a {self.proveedor.nombre} de {self.cantidad} x {self.bicicleta.nombre}"

class HistorialMantencion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    bicicleta = models.ForeignKey(Bicicleta, on_delete=models.CASCADE)
    fecha_mantencion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()

    def __str__(self):
        return f"Mantención de {self.bicicleta.nombre} para {self.usuario.username}"

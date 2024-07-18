from django.contrib import admin
from .models import Bicicleta,Carrito,ItemCarrito,Arriendo,Reparacion,Despacho,Proveedor,PedidoProveedor,HistorialMantencion,FormaPago
# Register your models here.


admin.site.register(Bicicleta)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(Arriendo)
admin.site.register(Reparacion)
admin.site.register(Despacho)
admin.site.register(Proveedor)
admin.site.register(PedidoProveedor)
admin.site.register(HistorialMantencion)
admin.site.register(FormaPago)


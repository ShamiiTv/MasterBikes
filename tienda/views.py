from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import get_object_or_404
from .forms import *
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.formats import localize
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import date

@login_required
def profile(request):
    return render(request, 'tienda/profile.html')

def registro(request):
    if request.method == "POST":
        registro = registroForm(request.POST)
        if registro.is_valid():
            registro.save()
            return render(request, 'tienda/index.html')
    else:
        registro = registroForm()

    return render(request, 'tienda/registro.html', {"form":registro})

def index(request):
    return render(request, 'tienda/index.html',)


def bicicletas(request):
    bicicletas_list = Bicicleta.objects.all()
    return render(request, 'tienda/bicicletas.html',{'bicicletas':bicicletas_list})

def arriendoBicicletas(request):
    return render(request, 'tienda/arriendoBicicletas.html',)

def contacto(request):
    return render(request, 'tienda/contacto.html')

def sobrenosotros(request):
    return render(request, 'tienda/sobrenosotros.html')

@login_required
def carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    total_clp = sum(item.producto.precio * item.cantidad for item in items)
    total_usd = sum(item.producto.precioDolar * item.cantidad for item in items)
    return render(request, 'tienda/carrito.html', {'items': items, 'total_clp': total_clp, 'total_usd': total_usd})

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Bicicleta, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    item, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        item.cantidad += 1
    item.save()
    return redirect('carrito')

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    item.delete()
    return redirect('carrito')

@login_required
def limpiar_carrito(request):
    carrito = Carrito.objects.get(usuario=request.user)
    carrito.items.all().delete()
    return redirect('carrito')
def format_clp(total_clp):
    total_clp = int(total_clp)

    formatted = f"{total_clp:,}"
    formatted = formatted.replace(',', '.')
    return formatted

@login_required
def actualizar_cantidad(request, item_id, cantidad):
    item = get_object_or_404(ItemCarrito, id=item_id)
    carrito = item.carrito

    try:
        cantidad = int(cantidad)
    except ValueError:
        return JsonResponse({'error': 'Cantidad no válida'}, status=400)

    nueva_cantidad = item.cantidad + cantidad
    if nueva_cantidad < 1:
        item.delete()
        cantidad_actualizada = 0
    else:
        item.cantidad = nueva_cantidad
        item.save()
        cantidad_actualizada = item.cantidad

    items = carrito.items.all()
    total_clp = sum(i.producto.precio * i.cantidad for i in items)
    total_usd = sum(i.producto.precioDolar * i.cantidad for i in items)
    total_clp_formatted = f"Total CLP : ${format_clp(total_clp)}"
    total_usd_formatted = f"Total USD : ${localize(total_usd)}"

    return JsonResponse({
        'mensaje': f'Cantidad actualizada a {cantidad_actualizada}',
        'cantidad_actualizada': cantidad_actualizada,
        'total_clp': total_clp_formatted,
        'total_usd': total_usd_formatted
    })




@require_http_methods(["GET"])
@login_required
def obtener_cantidad_carrito(request):
    carrito_usuario = Carrito.objects.get(usuario=request.user)
    cantidad_carrito = carrito_usuario.items.count()

    return JsonResponse({'cantidad_carrito': cantidad_carrito})



@login_required
def arriendoBicicletas(request, bicicleta_id):
    bicicleta = get_object_or_404(Bicicleta, id=bicicleta_id)
    
    if request.method == "POST":
        form = arriendoForm(request.POST)
        if form.is_valid():
            arriendo = form.save(commit=False)
            arriendo.usuario = request.user
            arriendo.bicicleta = bicicleta
            arriendo.save()
            return redirect('index') 
    else:
        form = arriendoForm()

    return render(request, 'tienda/arriendoBicicletas.html', {"form": form, "bicicleta": bicicleta})

@login_required
def historial_arriendos(request):
    arriendos_en_curso = Arriendo.objects.filter(usuario=request.user, fecha_fin__gte=date.today()).order_by('-fecha_inicio')
    arriendos_pasados = Arriendo.objects.filter(usuario=request.user, fecha_fin__lt=date.today()).order_by('-fecha_inicio')
    context = {
        'arriendos_en_curso': arriendos_en_curso,
        'arriendos_pasados': arriendos_pasados
    }
    return render(request, 'tienda/historial_arriendos.html', context)

@login_required
def reparaciones(request):
    if request.method == "POST":
        form = ReparacionForm(request.POST)
        if form.is_valid():
            reparacion = form.save(commit=False)
            reparacion.usuario = request.user
            reparacion.save()
            return redirect('index') 
    else:
        form = ReparacionForm()

    usuario = request.user
    ahora = timezone.now()
    reparaciones_en_curso = Reparacion.objects.filter(usuario=usuario, fecha_programada__gte=ahora)
    historial_reparaciones = Reparacion.objects.filter(usuario=usuario, fecha_programada__lt=ahora)

    context = {
        'form': form,
        'reparaciones_en_curso': reparaciones_en_curso,
        'historial_reparaciones': historial_reparaciones,
    }
    
    return render(request, 'tienda/reparaciones.html', context)


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Arriendo, FormaPago, Reparacion

class registroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(attrs={"class":"form-control"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "Nombre de usuario",
            "password1": "Contraseña",
            "password2": "Confirmar contraseña"
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de usuario"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Correo electrónico"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })

class arriendoForm(forms.ModelForm):
    forma_pago = forms.ModelChoiceField(
        queryset=FormaPago.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Arriendo
        fields = ["fecha_inicio", "fecha_fin", "deposito_garantia", "forma_pago"]
        labels = {
            "fecha_inicio": "Fecha de inicio",
            "fecha_fin": "Fecha de término",
            "deposito_garantia": "Depósito de garantía",
            "forma_pago": "Forma de pago"
        }
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "deposito_garantia": forms.NumberInput(attrs={"class": "form-control"}),
        }

class ReparacionForm(forms.ModelForm):
    bicicleta = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Modelo de la bicicleta"})
    )
    fecha_programada = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"})
    )
    descripcion_problema = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Describa el problema con su bicicleta"})
    )
    
    class Meta:
        model = Reparacion
        fields = ["bicicleta", "fecha_programada", "descripcion_problema"]
        labels = {
            "bicicleta": "Modelo de la bicicleta",
            "fecha_programada": "Fecha programada",
            "descripcion_problema": "Descripción del problema"
        }
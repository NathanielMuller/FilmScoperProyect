from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import PerfilUsuario, Reseña, Categoria

class RegistroForm(UserCreationForm):
    """Formulario de registro con validación híbrida"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com',
            'autocomplete': 'email'
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu apellido'
        })
    )
    
    fecha_nacimiento = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'max': '2018-12-31'  # Edad mínima 6 años
        })
    )
    
    generos_favoritos = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    
    foto_perfil = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases CSS a los campos de contraseña
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })
    
    def clean_email(self):
        """Validación personalizada para email único"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email ya está registrado.")
        return email
    
    def clean_fecha_nacimiento(self):
        """Validación de edad mínima"""
        from datetime import date
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        today = date.today()
        age = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        
        if age < 6:
            raise ValidationError("Debes tener al menos 6 años para registrarte.")
        
        return fecha_nacimiento
    
    def save(self, commit=True):
        """Guardar usuario y crear perfil extendido"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            
            # Crear perfil extendido
            perfil = PerfilUsuario.objects.create(
                user=user,
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                foto_perfil=self.cleaned_data.get('foto_perfil')
            )
            
            # Agregar géneros favoritos
            if self.cleaned_data['generos_favoritos']:
                perfil.generos_favoritos.set(self.cleaned_data['generos_favoritos'])
        
        return user

class LoginForm(forms.Form):
    """Formulario de inicio de sesión"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario o email',
            'autocomplete': 'username'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'autocomplete': 'current-password'
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

class ReseñaForm(forms.ModelForm):
    """Formulario para reseñas de películas"""
    class Meta:
        model = Reseña
        fields = ['calificacion', 'comentario']
        widgets = {
            'calificacion': forms.RadioSelect(choices=[
                (1, '1 ⭐'), (2, '2 ⭐⭐'), (3, '3 ⭐⭐⭐'), 
                (4, '4 ⭐⭐⭐⭐'), (5, '5 ⭐⭐⭐⭐⭐')
            ], attrs={'class': 'form-check-input'}),
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Comparte tu opinión sobre esta película...',
                'maxlength': 1000
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.pelicula = kwargs.pop('pelicula', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        """Guardar reseña con usuario y película"""
        reseña = super().save(commit=False)
        if self.user:
            reseña.usuario = self.user
        if self.pelicula:
            reseña.pelicula = self.pelicula
        
        if commit:
            reseña.save()
        
        return reseña

class PerfilForm(forms.ModelForm):
    """Formulario para editar perfil de usuario"""
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = PerfilUsuario
        fields = ['fecha_nacimiento', 'foto_perfil', 'biografia', 'generos_favoritos', 
                 'recibir_notificaciones', 'perfil_publico']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'foto_perfil': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'biografia': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'maxlength': 500
            }),
            'generos_favoritos': forms.CheckboxSelectMultiple,
            'recibir_notificaciones': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'perfil_publico': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
    
    def clean_email(self):
        """Validar email único (excluyendo el usuario actual)"""
        email = self.cleaned_data['email']
        if self.user and User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise ValidationError("Este email ya está en uso por otro usuario.")
        return email
    
    def save(self, commit=True):
        """Actualizar usuario y perfil"""
        perfil = super().save(commit=False)
        
        if self.user:
            # Actualizar campos del usuario
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        
        if commit:
            perfil.save()
            self.save_m2m()  # Para guardar many-to-many relationships
        
        return perfil
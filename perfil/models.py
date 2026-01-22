from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.utils import timezone

# ===============================
# DATOS PERSONALES
# ===============================
class DatosPersonales(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    descripcionperfil = models.CharField(max_length=50)
    perfilactivo = models.IntegerField(default=1)

    apellidos = models.CharField(max_length=60)
    nombres = models.CharField(max_length=60)
    foto_url = models.URLField(blank=True, null=True)
    nacionalidad = models.CharField(max_length=20)
    lugarnacimiento = models.CharField(max_length=60)
    fechanacimiento = models.DateField(null=True, blank=True)

    numerocedula = models.CharField(max_length=10, unique=True)

    sexo = models.CharField(
        max_length=1,
        choices=[('H', 'Hombre'), ('M', 'Mujer')]
    )

    estadocivil = models.CharField(max_length=50)
    licenciaconducir = models.CharField(max_length=6)

    telefonoconvencional = models.CharField(max_length=15, blank=True)
    telefonofijo = models.CharField(max_length=15, blank=True)

    direcciontrabajo = models.CharField(max_length=50, blank=True)
    direcciondomiciliaria = models.CharField(max_length=50)

    sitioweb = models.URLField(max_length=60, blank=True)

    def clean(self):
        super().clean()
        hoy = timezone.localdate()

        # ❌ No permitir fecha de nacimiento futura
        if self.fechanacimiento and self.fechanacimiento > hoy:
            raise ValidationError({
                "fechanacimiento": "La fecha de nacimiento no puede ser futura."
            })

    def save(self, *args, **kwargs):
        # Esto hace que la validación funcione también desde el admin
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


# ===============================
# EXPERIENCIA LABORAL
# ===============================
class ExperienciaLaboral(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)

    cargodesempenado = models.CharField(max_length=100)
    nombrempresa = models.CharField(max_length=50)
    lugarempresa = models.CharField(max_length=50, blank=True)

    emailempresa = models.EmailField(max_length=100, blank=True)
    sitiowebempresa = models.URLField(max_length=100, blank=True)

    nombrecontactoempresarial = models.CharField(max_length=100, blank=True)
    telefonocontactoempresarial = models.CharField(max_length=60, blank=True)

    fechainiciogestion = models.DateField()
    fechafingestion = models.DateField(null=True, blank=True)

    descripcionfunciones = models.CharField(max_length=100, blank=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.CharField(max_length=120, blank=True)

    def clean(self):
        super().clean()
        hoy = timezone.localdate()

        # ❌ No permitir fecha de inicio futura
        if self.fechainiciogestion and self.fechainiciogestion > hoy:
            raise ValidationError({
                "fechainiciogestion": "La fecha de inicio no puede ser futura."
            })

        # ❌ No permitir fecha de fin futura
        if self.fechafingestion and self.fechafingestion > hoy:
            raise ValidationError({
                "fechafingestion": "La fecha de fin no puede ser futura."
            })

        # ❌ No permitir fecha fin menor que inicio
        if self.fechainiciogestion and self.fechafingestion:
            if self.fechafingestion < self.fechainiciogestion:
                raise ValidationError({
                    "fechafingestion": "La fecha de fin no puede ser menor que la fecha de inicio."
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.cargodesempenado


# ===============================
# RECONOCIMIENTOS
# ===============================
class Reconocimiento(models.Model):
    TIPO_RECONOCIMIENTO = [
        ('Académico', 'Académico'),
        ('Público', 'Público'),
        ('Privado', 'Privado'),
    ]

    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)

    tiporeconocimiento = models.CharField(
        max_length=100,
        choices=TIPO_RECONOCIMIENTO
    )

    fechareconocimiento = models.DateField()
    descripcionreconocimiento = models.CharField(max_length=100, blank=True)

    entidadpatrocinadora = models.CharField(max_length=100, blank=True)
    nombrecontactoauspicia = models.CharField(max_length=100, blank=True)
    telefonocontactoauspicia = models.CharField(max_length=60, blank=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.CharField(max_length=120, blank=True)

    def clean(self):
        super().clean()
        hoy = timezone.localdate()

        # ❌ No permitir fecha futura
        if self.fechareconocimiento and self.fechareconocimiento > hoy:
            raise ValidationError({
                "fechareconocimiento": "La fecha de reconocimiento no puede ser futura."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.tiporeconocimiento


# ===============================
# CURSOS REALIZADOS
# ===============================
class CursoRealizado(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombrecurso = models.CharField(max_length=100)
    fechainicio = models.DateField()
    fechafin = models.DateField(null=True, blank=True)
    totalhoras = models.IntegerField()
    descripcioncurso = models.CharField(max_length=100, blank=True)
    entidadpatrocinadora = models.CharField(max_length=100, blank=True)
    nombrecontactoauspicia = models.CharField(max_length=100, blank=True)
    telefonocontactoauspicia = models.CharField(max_length=60, blank=True)
    emailempresapatrocinadora = models.EmailField(max_length=60, blank=True)

    # ✅ Solo URL del certificado
    rutacertificado = models.URLField(max_length=200, blank=True, null=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    def clean(self):
        super().clean()
        hoy = timezone.localdate()

        # ❌ No permitir fecha de inicio futura
        if self.fechainicio and self.fechainicio > hoy:
            raise ValidationError({
                "fechainicio": "La fecha de inicio no puede ser futura."
            })

        # ❌ No permitir fecha fin futura
        if self.fechafin and self.fechafin > hoy:
            raise ValidationError({
                "fechafin": "La fecha de fin no puede ser futura."
            })

        # ❌ No permitir fecha fin menor que inicio
        if self.fechainicio and self.fechafin:
            if self.fechafin < self.fechainicio:
                raise ValidationError({
                    "fechafin": "La fecha de fin no puede ser menor que la fecha de inicio."
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nombrecurso


# ===============================
# PRODUCTOS ACADÉMICOS
# ===============================
class ProductoAcademico(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)

    nombrerecurso = models.CharField(max_length=100)
    clasificador = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, blank=True)
    # 👉 URL de Cloudinary
    url_recurso = models.URLField(
        blank=True,
        null=True,
        verbose_name='URL del recurso (Cloudinary)'
    )

    activarparaqueseveaenfront = models.BooleanField(default=True)

    def __str__(self):
        return self.nombrerecurso


# ===============================
# PRODUCTOS LABORALES
# ===============================
class ProductoLaboral(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)

    nombreproducto = models.CharField(max_length=100)
    fechaproducto = models.DateField()
    descripcion = models.CharField(max_length=100, blank=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    def clean(self):
        super().clean()
        hoy = timezone.localdate()

        # ❌ No permitir fecha futura
        if self.fechaproducto and self.fechaproducto > hoy:
            raise ValidationError({
                "fechaproducto": "La fecha del producto no puede ser futura."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nombreproducto


# ===============================
# VENTA GARAGE
# ===============================
class VentaGarage(models.Model):
    ESTADO_PRODUCTO = [
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
    ]

    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)

    nombreproducto = models.CharField(max_length=100)
    estadoproducto = models.CharField(
        max_length=40,
        choices=ESTADO_PRODUCTO
    )

    descripcion = models.CharField(max_length=100, blank=True)
    valordelbien = models.DecimalField(max_digits=5, decimal_places=2)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    def __str__(self):
        return self.nombreproducto

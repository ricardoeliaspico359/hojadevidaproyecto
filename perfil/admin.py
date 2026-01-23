from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    Reconocimiento,
    CursoRealizado,
    ProductoAcademico,
    ProductoLaboral,
    VentaGarage
)

# =========================
# DATOS PERSONALES
# =========================
@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'numerocedula')
    fields = (
        'user',
        'descripcionperfil',
        'perfilactivo',
        'apellidos',
        'nombres',
        'foto_url',   # 👈 AQUÍ
        'nacionalidad',
        'lugarnacimiento',
        'fechanacimiento',
        'numerocedula',
        'sexo',
        'estadocivil',
        'licenciaconducir',
        'telefonoconvencional',
        'telefonofijo',
        'direcciontrabajo',
        'direcciondomiciliaria',
        'sitioweb',
    )
# =========================
# EXPERIENCIA LABORAL
# =========================
@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = (
        'perfil',
        'cargodesempenado',
        'nombrempresa',
        'fechainiciogestion',
        'fechafingestion',
        'activarparaqueseveaenfront'
    )

    fields = (
        'perfil',
        'cargodesempenado',
        'nombrempresa',
        'lugarempresa',
        'fechainiciogestion',
        'fechafingestion',
        'descripcionfunciones',
        'emailempresa',
        'sitiowebempresa',
        'nombrecontactoempresarial',
        'telefonocontactoempresarial',
        'rutacertificado',   # 👈 AQUÍ
        'activarparaqueseveaenfront'
    )

# =========================
# RECONOCIMIENTOS
# =========================
@admin.register(Reconocimiento)
class ReconocimientoAdmin(admin.ModelAdmin):
    list_display = (
        'perfil',
        'tiporeconocimiento',
        'fechareconocimiento',
        'entidadpatrocinadora',
        'activarparaqueseveaenfront'
    )

    list_filter = (
        'tiporeconocimiento',
        'activarparaqueseveaenfront'
    )

    search_fields = (
        'tiporeconocimiento',
        'entidadpatrocinadora'
    )


# =========================
# CURSOS REALIZADOS
# =========================
@admin.register(CursoRealizado)
class CursoRealizadoAdmin(admin.ModelAdmin):
    list_display = (
        'perfil',
        'nombrecurso',
        'fechainicio',
        'totalhoras',
        'activarparaqueseveaenfront',
        'ver_certificado'
    )

    readonly_fields = ('preview_certificado',)

    fields = (
        'perfil',
        'nombrecurso',
        'fechainicio',
        'fechafin',
        'totalhoras',
        'descripcioncurso',
        'entidadpatrocinadora',
        'nombrecontactoauspicia',
        'telefonocontactoauspicia',
        'emailempresapatrocinadora',
        'rutacertificado',       # 👈 aquí pegas el URL de Cloudinary
        'preview_certificado',
        'activarparaqueseveaenfront',
    )

    def ver_certificado(self, obj):
        return "Sí" if obj.rutacertificado else "No"
    ver_certificado.short_description = "Certificado"

    def preview_certificado(self, obj):
        if obj.rutacertificado:
            return mark_safe(
                f'<img src="{obj.rutacertificado}" style="max-width:200px; border:1px solid #ccc;" />'
            )
        return "No cargado"
    preview_certificado.short_description = "Vista previa"
# =========================
# PRODUCTOS ACADÉMICOS
# =========================
@admin.register(ProductoAcademico)
class ProductoAcademicoAdmin(admin.ModelAdmin):
    list_display = (
        'nombrerecurso',
        'clasificador',
        'url_recurso',
        'activarparaqueseveaenfront'
    )

    list_filter = (
        'clasificador',
        'activarparaqueseveaenfront'
    )

    search_fields = (
        'nombrerecurso',
        'clasificador'
    )

    fieldsets = (
        (None, {
            'fields': (
                'perfil',
                'nombrerecurso',
                'descripcion',
                'clasificador',
                'url_recurso',
                'activarparaqueseveaenfront',
            )
        }),
    )

# =========================
# PRODUCTOS LABORALES
# =========================
@admin.register(ProductoLaboral)
class ProductoLaboralAdmin(admin.ModelAdmin):
    list_display = (
        'perfil',
        'nombreproducto',
        'fechaproducto',
        'activarparaqueseveaenfront'
    )

    list_filter = (
        'activarparaqueseveaenfront',
    )

    search_fields = (
        'nombreproducto',
    )


# =========================
# VENTA GARAGE
# =========================
@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = (
        'perfil',
        'nombreproducto',
        'estadoproducto',
        'valordelbien',
        'fechapublicacion',
        'activarparaqueseveaenfront',
        'ver_foto'
    )

    list_filter = (
        'estadoproducto',
        'activarparaqueseveaenfront',
        'fechapublicacion'
    )

    search_fields = (
        'nombreproducto',
    )

    readonly_fields = ('preview_foto',)

    fields = (
        'perfil',
        'nombreproducto',
        'estadoproducto',
        'descripcion',
        'valordelbien',
        'fechapublicacion',
        'foto_producto',
        'preview_foto',
        'activarparaqueseveaenfront',
    )

    def ver_foto(self, obj):
        return "Sí" if obj.foto_producto else "No"
    ver_foto.short_description = "Foto"

    def preview_foto(self, obj):
        if obj.foto_producto:
            return mark_safe(
                f'<img src="{obj.foto_producto.url}" style="max-width:200px; border:1px solid #ccc; border-radius:8px;" />'
            )
        return "No cargada"
    preview_foto.short_description = "Vista previa"

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    CursoRealizado,
    Reconocimiento,
    ProductoAcademico,
    ProductoLaboral,
    VentaGarage
)


# ======================
# PERFIL ACTIVO (UTILIDAD)
# ======================
def obtener_perfil_activo():
    return DatosPersonales.objects.filter(perfilactivo=1).first()


# ======================
# GENERAR PDF
# ======================
def generar_pdf(request):
    perfil = obtener_perfil_activo()

    if not perfil:
        return HttpResponse("No hay perfil activo", status=404)

    template = get_template('perfil/pdf_hoja_vida.html')

    context = {
        'datos': perfil,
        'experiencias': ExperienciaLaboral.objects.filter(perfil=perfil),
        'cursos': CursoRealizado.objects.filter(perfil=perfil),
        'reconocimientos': Reconocimiento.objects.filter(perfil=perfil),
        'prod_academicos': ProductoAcademico.objects.filter(perfil=perfil),
        'prod_laborales': ProductoLaboral.objects.filter(perfil=perfil),
        'ventas': VentaGarage.objects.filter(perfil=perfil),
    }

    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="hoja_vida.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response


# ======================
# DASHBOARD
# ======================
def dashboard(request):
    perfil = obtener_perfil_activo()
    return render(request, 'perfil/dashboard.html', {'perfil': perfil})


# ======================
# DATOS PERSONALES
# ======================
def datos_personales(request):
    perfil = obtener_perfil_activo()

    if request.method == "POST" and perfil:
        foto = request.POST.get("foto_url")
        if foto:
            perfil.foto_url = foto
            perfil.save()

    return render(request, 'perfil/datos_personales.html', {'perfil': perfil})


# ======================
# EXPERIENCIA LABORAL
# ======================
def experiencia_laboral(request):
    perfil = obtener_perfil_activo()

    experiencias = ExperienciaLaboral.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    ).order_by('-fechainiciogestion')

    return render(request, 'perfil/experiencia_laboral.html', {
        'perfil': perfil,
        'experiencias': experiencias
    })


def eliminar_experiencia(request, id):
    experiencia = get_object_or_404(ExperienciaLaboral, id=id)
    experiencia.delete()
    return redirect('experiencia_laboral')


# ======================
# CURSOS REALIZADOS
# ======================
def cursos(request):
    perfil = obtener_perfil_activo()
    
    # Lógica para procesar la actualización del certificado
    if request.method == "POST" and perfil:
        curso_id = request.POST.get("curso_id")
        nueva_ruta = request.POST.get("rutacertificado")
        
        if curso_id and nueva_ruta:
            try:
                # Buscamos el curso que pertenezca al perfil activo
                curso = CursoRealizado.objects.get(id=curso_id, perfil=perfil)
                curso.rutacertificado = nueva_ruta
                curso.save()
            except CursoRealizado.DoesNotExist:
                pass # El curso no existe o no pertenece al perfil

    # Obtener la lista de cursos para mostrar
    cursos_listado = CursoRealizado.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    ).order_by('-fechainicio')

    return render(request, 'perfil/cursos.html', {
        'perfil': perfil,
        'cursos': cursos_listado
    })

# ======================
# RECONOCIMIENTOS
# ======================
def reconocimientos(request):
    perfil = obtener_perfil_activo()

    reconocimientos = Reconocimiento.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    ).order_by('-fechareconocimiento')

    return render(request, 'perfil/reconocimientos.html', {
        'perfil': perfil,
        'reconocimientos': reconocimientos
    })


# ======================
# PRODUCTOS ACADÉMICOS
# ======================
def productos_academicos(request):
    perfil = obtener_perfil_activo()

    productos = ProductoAcademico.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    )

    return render(request, 'perfil/productos_academicos.html', {
        'perfil': perfil,
        'productos': productos
    })


# ======================
# PRODUCTOS LABORALES
# ======================
def productos_laborales(request):
    perfil = obtener_perfil_activo()

    productos = ProductoLaboral.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    ).order_by('-fechaproducto')

    return render(request, 'perfil/productos_laborales.html', {
        'perfil': perfil,
        'productos': productos
    })


# ======================
# VENTA GARAGE
# ======================
def venta_garage(request):
    perfil = obtener_perfil_activo()

    productos = VentaGarage.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    )

    return render(request, 'perfil/venta_garage.html', {
        'perfil': perfil,
        'productos': productos
    })

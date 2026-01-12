from django import forms
from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    CursoRealizado,
    Reconocimiento,
    ProductoAcademico,
    ProductoLaboral,
    VentaGarage
)

class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = DatosPersonales
        fields = '__all__'

class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        fields = '__all__'

class CursoForm(forms.ModelForm):
    class Meta:
        model = CursoRealizado
        fields = '__all__'

class ReconocimientoForm(forms.ModelForm):
    class Meta:
        model = Reconocimiento
        fields = '__all__'

class ProductoAcademicoForm(forms.ModelForm):
    class Meta:
        model = ProductoAcademico
        fields = '__all__'

class ProductoLaboralForm(forms.ModelForm):
    class Meta:
        model = ProductoLaboral
        fields = '__all__'

class VentaGarageForm(forms.ModelForm):
    class Meta:
        model = VentaGarage
        fields = '__all__'

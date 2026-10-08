from django import forms
from .models import Alerta, Parada


class AlertaForm(forms.ModelForm):
    class Meta:
        model = Alerta
        fields = ["maquina", "descripcion"]

    def clean_descripcion(self):
        descripcion = self.cleaned_data["descripcion"].strip()

        if not descripcion:
            raise forms.ValidationError("La descripción no puede estar vacía.")

        return descripcion


class ParadaForm(forms.ModelForm):
    class Meta:
        model = Parada
        fields = ["maquina", "fecha", "hora_inicio", "hora_finalizacion", "motivo"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "hora_inicio": forms.TimeInput(attrs={"type": "time"}),
            "hora_finalizacion": forms.TimeInput(attrs={"type": "time"}),
        }

    def clean_motivo(self):
        motivo = self.cleaned_data["motivo"].strip()

        if not motivo:
            raise forms.ValidationError("El motivo no puede estar vacío.")

        return motivo

    def clean(self):
        cleaned_data = super().clean()

        inicio = cleaned_data.get("hora_inicio")
        final = cleaned_data.get("hora_finalizacion")

        if inicio and final and inicio == final:
            raise forms.ValidationError(
                "La hora de finalización no puede ser igual a la hora de inicio."
            )

        return cleaned_data
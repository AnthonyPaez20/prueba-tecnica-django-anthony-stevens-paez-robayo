from django.contrib.auth.models import User
from django.db import models


class Alerta(models.Model):
    maquina = models.CharField(max_length=100)
    descripcion = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.maquina} - {self.fecha}"


class Parada(models.Model):
    maquina = models.CharField(max_length=100)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_finalizacion = models.TimeField()
    motivo = models.TextField()
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="paradas_registradas"
    )

    cancelada = models.BooleanField(default=False)
    cancelada_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="paradas_canceladas"
    )
    fecha_cancelacion = models.DateTimeField(null=True, blank=True)
    motivo_cancelacion = models.TextField(blank=True)

    def duracion_minutos(self):
        from datetime import datetime, timedelta

        inicio = datetime.combine(self.fecha, self.hora_inicio)
        final = datetime.combine(self.fecha, self.hora_finalizacion)

        # Si termina después de medianoche, corresponde al día siguiente.
        if final <= inicio:
            final += timedelta(days=1)

        return int((final - inicio).total_seconds() / 60)

    def __str__(self):
        return f"{self.maquina} - {self.fecha} - {self.hora_inicio}"
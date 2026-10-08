from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AlertaForm, ParadaForm
from .models import Alerta, Parada


def tiene_rol(usuario, rol):
    return usuario.groups.filter(name=rol).exists()


def login_view(request):
    if request.user.is_authenticated:
        return redirect("inicio")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:
            login(request, usuario)
            return redirect("inicio")

        messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "maquinas/login.html")


@login_required
def inicio(request):
    alertas = Alerta.objects.all().order_by("-fecha")
    paradas = Parada.objects.all().order_by("-fecha", "-hora_inicio")

    if tiene_rol(request.user, "Operario"):
        alertas = alertas.filter(usuario=request.user)

    return render(
        request,
        "maquinas/inicio.html",
        {
            "alertas": alertas,
            "paradas": paradas,
            "es_operario": tiene_rol(request.user, "Operario"),
            "es_supervisor": tiene_rol(request.user, "Supervisor"),
            "es_jefe": tiene_rol(request.user, "Jefe"),
        }
    )


@login_required
def crear_alerta(request):
    if not tiene_rol(request.user, "Operario"):
        messages.error(
            request,
            "No tiene permiso para registrar alertas."
        )
        return redirect("inicio")

    if request.method == "POST":
        form = AlertaForm(request.POST)

        if form.is_valid():
            alerta = form.save(commit=False)
            alerta.usuario = request.user
            alerta.save()

            messages.success(
                request,
                "Alerta registrada correctamente."
            )
            return redirect("inicio")
    else:
        form = AlertaForm()

    return render(
        request,
        "maquinas/inicio.html",
        {
            "form_alerta": form,
            "alertas": Alerta.objects.filter(
                usuario=request.user
            ).order_by("-fecha"),
            "paradas": Parada.objects.all().order_by(
                "-fecha",
                "-hora_inicio"
            ),
            "es_operario": True,
        }
    )


@login_required
def editar_alerta(request, alerta_id):
    if not tiene_rol(request.user, "Supervisor"):
        messages.error(
            request,
            "No tiene permiso para editar alertas."
        )
        return redirect("inicio")

    alerta = get_object_or_404(Alerta, id=alerta_id)

    if request.method == "POST":
        form = AlertaForm(request.POST, instance=alerta)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Alerta actualizada correctamente."
            )
            return redirect("inicio")
    else:
        form = AlertaForm(instance=alerta)

    return render(
        request,
        "maquinas/editar_alerta.html",
        {
            "form": form,
            "alerta": alerta,
        }
    )


@login_required
def crear_parada(request):
    if not tiene_rol(request.user, "Supervisor"):
        messages.error(
            request,
            "No tiene permiso para registrar paradas."
        )
        return redirect("inicio")

    if request.method == "POST":
        form = ParadaForm(request.POST)

        if form.is_valid():
            parada = form.save(commit=False)
            parada.usuario = request.user
            parada.save()

            messages.success(
                request,
                "Parada registrada correctamente."
            )
            return redirect("inicio")
    else:
        form = ParadaForm()

    return render(
        request,
        "maquinas/crear_parada.html",
        {
            "form": form,
        }
    )


@login_required
def cancelar_parada(request, parada_id):
    if not tiene_rol(request.user, "Jefe"):
        messages.error(
            request,
            "No tiene permiso para cancelar paradas."
        )
        return redirect("inicio")

    parada = get_object_or_404(Parada, id=parada_id)

    if parada.cancelada:
        messages.warning(
            request,
            "La parada ya fue cancelada anteriormente."
        )
        return redirect("inicio")

    if request.method == "POST":
        motivo = request.POST.get("motivo_cancelacion", "").strip()

        if not motivo:
            messages.error(
                request,
                "Debe indicar el motivo de la cancelación."
            )
            return redirect("inicio")

        from django.utils import timezone

        parada.cancelada = True
        parada.cancelada_por = request.user
        parada.fecha_cancelacion = timezone.now()
        parada.motivo_cancelacion = motivo
        parada.save()

        messages.success(
            request,
            "Parada cancelada correctamente."
        )

    return redirect("inicio")


def logout_view(request):
    logout(request)
    return redirect("login")
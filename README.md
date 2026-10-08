# Prueba técnica Django - Gestión de máquinas

Aplicación web desarrollada en Python y Django para registrar alertas y paradas de máquinas, aplicando autenticación y permisos según el rol del usuario.

## Tecnologías

* Python 3.12.5
* Django 6.1.2
* SQLite
* HTML
* Git / GitHub

## Estructura principal

* `config/`: configuración del proyecto Django.
* `maquinas/`: aplicación principal.
* `maquinas/models.py`: modelos de alertas y paradas.
* `maquinas/forms.py`: formularios y validaciones.
* `maquinas/views.py`: lógica, autenticación y permisos.
* `maquinas/templates/`: interfaz HTML.
* `db.sqlite3`: base de datos SQLite.
* `requirements.txt`: dependencias del proyecto.

## Instalación y ejecución

1. Crear y activar un entorno virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

3. Aplicar las migraciones:

```powershell
python manage.py migrate
```

4. Ejecutar el servidor:

```powershell
python manage.py runserver
```

5. Abrir en el navegador:

```text
http://127.0.0.1:8000/
```

## Usuarios de demostración

Todos utilizan la contraseña:

```text
Colfrance123!
```

| Usuario           | Rol        |
| ----------------- | ---------- |
| `operario_demo`   | Operario   |
| `supervisor_demo` | Supervisor |
| `jefe_demo`       | Jefe       |

## Funcionalidades y permisos

### Operario

* Registrar alertas.
* Consultar únicamente las alertas que él mismo registró.
* No puede editar alertas.
* No puede registrar paradas.
* No puede cancelar paradas.

### Supervisor

* Consultar alertas.
* Editar alertas.
* Registrar paradas.
* Consultar paradas.
* No puede cancelar paradas.

### Jefe

* Consultar alertas.
* Consultar paradas.
* Cancelar paradas indicando un motivo.
* No puede editar alertas.
* No puede registrar paradas.

Los permisos se validan en el backend mediante los grupos de Django y no únicamente mediante la interfaz.

## Validaciones realizadas

### Descripción y motivo obligatorios

Se validó que una alerta sin descripción y una parada sin motivo no sean almacenadas.

### Duración de parada

Se probó una parada:

```text
Inicio: 23:50
Finalización: 00:20
```

Resultado:

```text
30 minutos
```

Cuando la hora de finalización es anterior a la hora de inicio, se interpreta como una finalización al día siguiente. Una hora de finalización igual a la hora de inicio es rechazada.

### Protección de edición

Un usuario que no tenga rol Supervisor no puede editar una alerta aunque intente acceder directamente a la URL de edición.

### Doble cancelación

Se canceló una parada y posteriormente se intentó cancelar nuevamente mediante la URL.

Resultado:

```text
La parada ya fue cancelada anteriormente.
```

El registro original se conserva y no se duplica ni se modifican los datos de la primera cancelación.

## Pruebas realizadas

| Prueba                               | Resultado               |
| ------------------------------------ | ----------------------- |
| Inicio de sesión por rol             | Correcta                |
| Registro de alerta por Operario      | Correcta                |
| Consulta de alertas propias          | Correcta                |
| Edición de alerta por Supervisor     | Correcta                |
| Registro de parada por Supervisor    | Correcta                |
| Cálculo 23:50 - 00:20                | Correcta: 30 minutos    |
| Consulta de información por Jefe     | Correcta                |
| Cancelación de parada                | Correcta                |
| Segunda cancelación                  | Rechazada correctamente |
| Protección mediante permisos backend | Correcta                |
| Protección CSRF                      | Implementada            |

## Resultados y fallas encontradas

Durante las pruebas funcionales no se presentaron fallas que impidieran completar el flujo principal.

Se verificaron los permisos accediendo tanto desde la interfaz como mediante URLs directas para comprobar que las restricciones estuvieran implementadas en el backend.

## Registro de tiempo

El proyecto fue iniciado durante la realización de la prueba técnica.

Se realizó un primer commit del proyecto base antes del desarrollo funcional:

```text
a45df02 - Inicio del proyecto Django
```

El desarrollo funcional, pruebas y documentación se realizaron dentro del tiempo establecido para la prueba.

## Uso de inteligencia artificial

Se utilizó inteligencia artificial como apoyo durante el desarrollo para orientación sobre estructura de Django, validaciones, permisos, manejo de formularios, documentación y resolución de problemas.

El código utilizado fue revisado y probado durante la ejecución de la aplicación, y se comprende su funcionamiento general.

## Integración en un monolito Django existente

La aplicación puede incorporarse como una app Django independiente dentro del proyecto existente, reutilizando el sistema de usuarios y autenticación actual. Los modelos `Alerta` y `Parada` pueden mantenerse como parte del dominio de gestión de máquinas. Los grupos y permisos pueden adaptarse a los roles ya existentes en el sistema.

## Troubleshooting

### Caso 1: La aplicación deja de registrar paradas durante alta producción

La primera acción sería informar al supervisor y verificar de forma segura si existe una falla en la aplicación, base de datos o infraestructura, evitando realizar cambios directamente en producción sin diagnóstico. Mantendría la comunicación con el equipo y solicitaría apoyo técnico si es necesario.

### Caso 2: Ocurre una caída mientras solicitan un reporte urgente y otro usuario no puede iniciar sesión

Priorizaría la atención según el impacto del incidente, informaría al responsable del reporte sobre el estado y tiempo estimado, y delegaría la revisión del problema de inicio de sesión si existe otro integrante disponible.

### Caso 3: Un cambio propio genera errores para varios usuarios

Informaría inmediatamente al equipo, evaluaría revertir el cambio si es la alternativa segura y evitaría modificar producción directamente sin revisión. Después verificaría la solución en un entorno controlado antes de volver a desplegarla.

## Estado de la entrega

Proyecto funcional, documentado y publicado en GitHub.

Repositorio:
https://github.com/AnthonyPaez20/prueba-tecnica-django-anthony-stevens-paez-robayo
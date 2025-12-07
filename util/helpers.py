"""
Helpers del sistema
Funciones auxiliares
"""

from datetime import datetime


def formatear_fecha(fecha):
    """
    Convierte 'YYYY-MM-DD' a 'DD/MM/YYYY'.
    Si viene None o no es válida, se devuelve tal cual.
    """
    if not fecha:
        return ""

    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
        return fecha_obj.strftime('%d/%m/%Y')
    except (ValueError, TypeError):
        return fecha


def obtener_fecha_actual():
    """Devuelve la fecha de hoy en formato 'YYYY-MM-DD'."""
    return datetime.now().strftime('%Y-%m-%d')


def obtener_hora_actual():
    """Devuelve la hora actual en formato 'HH:MM'."""
    return datetime.now().strftime('%H:%M')


def calcular_duracion(hora_inicio, hora_fin):
    """
    Calcula duración en minutos entre dos horas 'HH:MM'.
    Si hay error o el fin es anterior al inicio, devuelve 0.
    """
    try:
        inicio = datetime.strptime(hora_inicio, '%H:%M')
        fin = datetime.strptime(hora_fin, '%H:%M')
        duracion = (fin - inicio).total_seconds() / 60
        return max(0, int(duracion))
    except (ValueError, TypeError):
        return 0


def formatear_cuota(cuota):
    """
    Convierte un número a '€XX.XX'.
    Si viene None, devuelve '€0.00'.
    """
    try:
        return f"€{float(cuota):.2f}"
    except (ValueError, TypeError):
        return "€0.00"

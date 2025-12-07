"""
Helpers del sistema
Funciones auxiliares
"""

from datetime import datetime, timedelta


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
        return str(fecha)


def obtener_fecha_actual():
    """Devuelve la fecha actual en formato 'YYYY-MM-DD'."""
    return datetime.now().strftime('%Y-%m-%d')


def obtener_hora_actual():
    """Devuelve la hora actual en formato 'HH:MM'."""
    return datetime.now().strftime('%H:%M')


def calcular_duracion(hora_inicio, hora_fin):
    """
    Calcula la duración en minutos entre dos horas.
    Devuelve None si hay error.
    """
    try:
        inicio = datetime.strptime(hora_inicio, '%H:%M')
        fin = datetime.strptime(hora_fin, '%H:%M')
        return int((fin - inicio).total_seconds() / 60)
    except (ValueError, TypeError):
        return None


def formatear_cuota(cuota):
    """
    Convierte un número a '€XX.XX'.
    Si viene None, devuelve '€0.00'.
    """
    try:
        return f"€{float(cuota):.2f}"
    except (ValueError, TypeError):
        return "€0.00"


def calcular_hora_fin(hora_inicio):
    """
    Calcula la hora de fin sumando 30 minutos a la hora de inicio.
    Formato: HH:MM
    """
    if not hora_inicio:
        return ""
    
    try:
        inicio = datetime.strptime(hora_inicio, '%H:%M')
        fin = inicio + timedelta(minutes=30)
        return fin.strftime('%H:%M')
    except (ValueError, TypeError):
        return ""

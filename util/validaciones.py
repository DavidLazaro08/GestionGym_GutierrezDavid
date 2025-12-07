"""
Módulo de validaciones
Funciones para validar datos de entrada
"""

import re


def validar_dni(dni):
    """
    Valida un DNI español real:
    - Formato correcto 8 dígitos + letra
    - Letra calculada correctamente
    """
    if not dni:
        return False

    dni = dni.upper().strip()
    patron = r'^\d{8}[A-Z]$'

    if not re.match(patron, dni):
        return False

    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    numero = int(dni[:-1])
    letra_correcta = letras[numero % 23]

    return dni[-1] == letra_correcta


def validar_email(email):
    """Valida email básico."""
    if not email:
        return False
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, email.strip()))


def validar_telefono(telefono):
    """
    Valida teléfono español:
    - 9 dígitos
    - Empieza por 6, 7, 8 o 9
    """
    if not telefono:
        return False
    patron = r'^[6789]\d{8}$'
    return bool(re.match(patron, telefono.strip()))


def validar_fecha(fecha):
    """Valida formato YYYY-MM-DD."""
    if not fecha:
        return False
    patron = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(patron, fecha.strip()))


def validar_hora(hora):
    """Valida formato HH:MM (00:00 a 23:59)."""
    if not hora:
        return False
    patron = r'^([01]\d|2[0-3]):[0-5]\d$'
    return bool(re.match(patron, hora.strip()))


def validar_cuota(cuota):
    """Valida que la cuota sea un número positivo."""
    try:
        valor = float(str(cuota).strip())
        return valor > 0
    except (ValueError, TypeError):
        return False

"""
Módulo de vistas
Contiene las interfaces gráficas del sistema
"""

from .main_view import MainView
from .cliente_view import ClienteView
from .aparato_view import AparatoView
from .reserva_view import ReservaView
from .pago_view import PagoView

__all__ = ['MainView', 'ClienteView', 'AparatoView', 'ReservaView', 'PagoView']

"""
Módulo de colores y estilos
Paleta de colores moderna para la interfaz (Tema Oscuro Neon)
"""

# ============================================================
#   PALETA DE COLORES MODERNA (TEMA OSCURO)
# ============================================================

# Colores principales (Fondo general)
COLOR_FONDO = "#0e1217"           # Oscuro casi negro (Main BG)
COLOR_FONDO_CARD = "#1b2430"      # Gris azulado oscuro (Card Containers)
COLOR_FONDO_HOVER = "#2d3a4f"     # Hover suave

# Colores de acento
COLOR_SECUNDARIO = "#00d4aa"      # Turquesa brillante (Primary Action / Focus)
COLOR_ACENTO = "#8b5cf6"          # Morado neón (Secondary Action)

# Inputs
COLOR_INPUT_BG = "#0f1620"        # Fondo de inputs (casi negro)
COLOR_INPUT_BORDER = "#2d3a4f"    # Borde normal de inputs
COLOR_INPUT_FOCUS = "#00d4aa"     # Borde focus de inputs
COLOR_INPUT_TEXT = "#ffffff"      # Texto en inputs

# Textos
COLOR_TEXTO_PRINCIPAL = "#ffffff"     # Blanco puro
COLOR_TEXTO_SECUNDARIO = "#a0aec0"    # Gris claro (Labels, subtitles)
COLOR_TEXTO_CLARO = "#d1d5db"         # Gris muy claro
COLOR_TEXTO_DARK = "#0f1419"          # Para texto sobre botones claros

# Colores de estado (Botones y alertas)
COLOR_EXITO = "#00d4aa"           # Turquesa (Nuevo, Guardar) - Mismo que secundario
COLOR_ADVERTENCIA = "#f59e0b"     # Naranja
COLOR_PELIGRO = "#ef4444"         # Rojo elegante
COLOR_INFO = "#3b82f6"            # Azul brillante
COLOR_NEUTRAL = "#4b5563"         # Gris medio

# Alias para compatibilidad
COLOR_PRIMARIO = "#0e1217"        # Alias para fondo principal
COLOR_ERROR = COLOR_PELIGRO
COLOR_PENDIENTE = COLOR_ADVERTENCIA
COLOR_DISPONIBLE = COLOR_EXITO
COLOR_OCUPADO = COLOR_PELIGRO

# Sidebar
COLOR_SIDEBAR_BG = "#161b22"      # Ligeramente más claro que el fondo
COLOR_SIDEBAR_HOVER = "#1f2937"
COLOR_SIDEBAR_ACTIVE = COLOR_SECUNDARIO
COLOR_SIDEBAR_TEXT = "#e2e8f0"

# ============================================================
#   TIPOGRAFÍA
# ============================================================

FUENTE_PRINCIPAL = "Segoe UI"
FUENTE_TITULO = ("Segoe UI", 24, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 16)
FUENTE_NORMAL = ("Segoe UI", 11)
FUENTE_BOTON = ("Segoe UI", 10, "bold")
FUENTE_LABEL = ("Segoe UI", 10, "bold")

# ============================================================
#   DIMENSIONES
# ============================================================

ANCHO_SIDEBAR = 240 # Un poco más ancho para elegancia

# ============================================================
#   RUTAS DE RECURSOS
# ============================================================

import os

RUTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_PROYECTO = os.path.dirname(RUTA_BASE)
RUTA_IMG = os.path.join(RUTA_BASE, "img")

# Logos
LOGO_ICONO = os.path.join(RUTA_IMG, "GF.png")
LOGO_TEXTO = os.path.join(RUTA_IMG, "GFTM.png")
LOGO_COMPLETO = os.path.join(RUTA_IMG, "Logo_GFTM.png")

# ============================================================
#   ESTILOS DE BOTONES (DICCIONARIOS)
# ============================================================

ESTILO_BOTON_BASE = {
    "font": FUENTE_BOTON,
    "relief": "flat",
    "cursor": "hand2",
    "bd": 0
}

ESTILO_BOTON_EXITO = {
    **ESTILO_BOTON_BASE,
    "bg": COLOR_EXITO,
    "fg": "#0f1419", # Texto oscuro sobre turquesa
    "activebackground": "#00b894",
    "activeforeground": "#ffffff"
}

ESTILO_BOTON_INFO = {
    **ESTILO_BOTON_BASE,
    "bg": COLOR_INFO,
    "fg": "#ffffff",
    "activebackground": "#2563eb",
    "activeforeground": "#ffffff"
}

ESTILO_BOTON_ADVERTENCIA = {
    **ESTILO_BOTON_BASE,
    "bg": COLOR_ADVERTENCIA, # Naranja
    "fg": "#ffffff",
    "activebackground": "#d97706",
    "activeforeground": "#ffffff"
}

ESTILO_BOTON_PELIGRO = {
    **ESTILO_BOTON_BASE,
    "bg": COLOR_PELIGRO,
    "fg": "#ffffff",
    "activebackground": "#dc2626",
    "activeforeground": "#ffffff"
}

ESTILO_BOTON_NEUTRAL = {
    **ESTILO_BOTON_BASE,
    "bg": COLOR_NEUTRAL,
    "fg": "#ffffff",
    "activebackground": "#374151",
    "activeforeground": "#ffffff"
}

ESTILO_BOTON_SECUNDARIO = { # Turquesa pero estilo secundario
    **ESTILO_BOTON_BASE,
    "bg": "#1f2937", # Fondo oscuro
    "fg": COLOR_SECUNDARIO, # Texto turquesa
    "activebackground": COLOR_SECUNDARIO,
    "activeforeground": "#0f1419"
}

ESTILO_BOTON_ACENTO = {
    **ESTILO_BOTON_BASE,
    "bg": COLOR_ACENTO, # Morado
    "fg": "#ffffff",
    "activebackground": "#7c3aed",
    "activeforeground": "#ffffff"
}

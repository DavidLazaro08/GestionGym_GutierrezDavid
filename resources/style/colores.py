"""
Módulo de colores y estilos
Paleta de colores moderna para la interfaz
"""

# ============================================================
#   PALETA DE COLORES MODERNA
# ============================================================

# Colores principales
COLOR_PRIMARIO = "#1a2332"        # Azul oscuro (sidebar, headers)
COLOR_SECUNDARIO = "#00d4aa"      # Verde agua (acentos, highlights)
COLOR_ACENTO = "#8b5cf6"          # Morado (elementos especiales)

# Colores de fondo
COLOR_FONDO = "#f5f7fa"           # Gris muy claro (fondo principal)
COLOR_FONDO_CARD = "#ffffff"      # Blanco (tarjetas, formularios)
COLOR_FONDO_HOVER = "#e8edf3"     # Hover en elementos
COLOR_FONDO_CLARO = "#ecf0f1"     # Gris claro (compatibilidad)
COLOR_FONDO_OSCURO = "#2d3a4f"    # Azul oscuro secundario

# Colores de texto
COLOR_TEXTO_PRINCIPAL = "#2d3748"  # Gris oscuro
COLOR_TEXTO_SECUNDARIO = "#718096" # Gris medio
COLOR_TEXTO_CLARO = "#a0aec0"      # Gris claro
COLOR_TEXTO_BLANCO = "#ffffff"     # Blanco
COLOR_TEXTO_OSCURO = "#2c3e50"     # Negro azulado (compatibilidad)

# Colores de estado (botones y acciones)
COLOR_EXITO = "#10b981"           # Verde (Guardar, Nuevo, Éxito)
COLOR_ADVERTENCIA = "#f59e0b"     # Naranja (Modificar, Advertencia)
COLOR_PELIGRO = "#ef4444"         # Rojo (Eliminar, Error)
COLOR_INFO = "#3b82f6"            # Azul (Información, Acciones generales)
COLOR_NEUTRAL = "#6b7280"         # Gris (Cancelar, Limpiar)

# Alias para compatibilidad con código existente
COLOR_ERROR = COLOR_PELIGRO
COLOR_PENDIENTE = COLOR_ADVERTENCIA
COLOR_DISPONIBLE = COLOR_EXITO
COLOR_OCUPADO = COLOR_PELIGRO

# Colores de sidebar
COLOR_SIDEBAR_BG = COLOR_PRIMARIO
COLOR_SIDEBAR_HOVER = "#2d3a4f"
COLOR_SIDEBAR_ACTIVE = COLOR_SECUNDARIO
COLOR_SIDEBAR_TEXT = COLOR_TEXTO_BLANCO

# ============================================================
#   TIPOGRAFÍA
# ============================================================

FUENTE_PRINCIPAL = "Segoe UI"
FUENTE_TITULO = ("Segoe UI", 20, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 14, "bold")
FUENTE_NORMAL = ("Segoe UI", 10)
FUENTE_BOTON = ("Segoe UI", 10, "bold")
FUENTE_LABEL = ("Segoe UI", 9)

# ============================================================
#   DIMENSIONES
# ============================================================

ANCHO_SIDEBAR = 220

# ============================================================
#   RUTAS DE RECURSOS
# ============================================================

import os

# Obtener ruta base del proyecto (desde resources/style/ subimos 2 niveles)
RUTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# RUTA_BASE ahora apunta a: .../GestionGym_GutierrezDavid/resources/
# Necesitamos subir un nivel más para llegar a la raíz del proyecto
RUTA_PROYECTO = os.path.dirname(RUTA_BASE)
RUTA_IMG = os.path.join(RUTA_BASE, "img")

# Logos
LOGO_ICONO = os.path.join(RUTA_IMG, "GF.png")              # Solo icono
LOGO_TEXTO = os.path.join(RUTA_IMG, "GFTM.png")            # Solo texto
LOGO_COMPLETO = os.path.join(RUTA_IMG, "Logo_GFTM.png")    # Icono + texto

# ============================================================
#   ESTILOS DE BOTONES (DICCIONARIOS)
# ============================================================

ESTILO_BOTON_EXITO = {
    "bg": COLOR_EXITO,
    "fg": COLOR_TEXTO_BLANCO,
    "font": FUENTE_BOTON,
    "relief": "flat",
    "cursor": "hand2",
    "activebackground": "#059669",
    "bd": 0
}

ESTILO_BOTON_INFO = {
    "bg": COLOR_INFO,
    "fg": COLOR_TEXTO_BLANCO,
    "font": FUENTE_BOTON,
    "relief": "flat",
    "cursor": "hand2",
    "activebackground": "#2563eb",
    "bd": 0
}

ESTILO_BOTON_ADVERTENCIA = {
    "bg": COLOR_ADVERTENCIA,
    "fg": COLOR_TEXTO_BLANCO,
    "font": FUENTE_BOTON,
    "relief": "flat",
    "cursor": "hand2",
    "activebackground": "#d97706",
    "bd": 0
}

ESTILO_BOTON_PELIGRO = {
    "bg": COLOR_PELIGRO,
    "fg": COLOR_TEXTO_BLANCO,
    "font": FUENTE_BOTON,
    "relief": "flat",
    "cursor": "hand2",
    "activebackground": "#dc2626",
    "bd": 0
}

ESTILO_BOTON_NEUTRAL = {
    "bg": COLOR_NEUTRAL,
    "fg": COLOR_TEXTO_BLANCO,
    "font": FUENTE_BOTON,
    "relief": "flat",
    "cursor": "hand2",
    "activebackground": "#4b5563",
    "bd": 0
}

ESTILO_BOTON_SECUNDARIO = {
    "bg": COLOR_SECUNDARIO,
    "fg": COLOR_TEXTO_PRINCIPAL,
    "font": FUENTE_BOTON,
    "relief": "flat",
    "cursor": "hand2",
    "activebackground": "#00b894",
    "bd": 0
}

ESTILO_BOTON_ACENTO = {
    "bg": COLOR_ACENTO,
    "fg": COLOR_TEXTO_BLANCO,
    "font": FUENTE_BOTON,
    "relief": "flat",
    "cursor": "hand2",
    "activebackground": "#7c3aed",
    "bd": 0
}

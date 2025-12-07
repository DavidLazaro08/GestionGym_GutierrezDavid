"""
Vista Principal
Ventana principal del sistema con menú de navegación
"""

import tkinter as tk
from tkinter import messagebox
from data.gestor_bd import GestorBD
from view.cliente_view import ClienteView
from view.aparato_view import AparatoView
from view.reserva_view import ReservaView
from view.pago_view import PagoView


class MainView:
    """Clase para la ventana principal"""
    
    def __init__(self, root):
        """
        Inicializa la ventana principal
        
        Args:
            root: Ventana raíz de Tkinter
        """
        self.root = root
        self.root.title("GymForTheMoment - Sistema de Gestión")
        self.root.geometry("800x600")
        
        # Inicializar base de datos
        self.inicializar_bd()
        
        # Configurar interfaz
        self.configurar_interfaz()
    
    def inicializar_bd(self):
        """Inicializa la base de datos y crea las tablas"""
        gestor = GestorBD()
        gestor.conectar()
        gestor.crear_tablas()
        gestor.desconectar()
    
    def configurar_interfaz(self):
        """Configura la interfaz principal"""
        # Título
        titulo = tk.Label(
            self.root,
            text="GymForTheMoment",
            font=("Arial", 24, "bold"),
            fg="#2c3e50"
        )
        titulo.pack(pady=30)
        
        # Subtítulo
        subtitulo = tk.Label(
            self.root,
            text="Sistema de Gestión de Gimnasio",
            font=("Arial", 14),
            fg="#7f8c8d"
        )
        subtitulo.pack(pady=10)
        
        # Frame para botones
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=50)
        
        # Botón Gestión de Clientes
        btn_clientes = tk.Button(
            frame_botones,
            text="Gestión de Clientes",
            command=self.abrir_clientes,
            width=25,
            height=2,
            font=("Arial", 12),
            bg="#3498db",
            fg="white",
            cursor="hand2"
        )
        btn_clientes.grid(row=0, column=0, padx=15, pady=15)
        
        # Botón Gestión de Aparatos
        btn_aparatos = tk.Button(
            frame_botones,
            text="Gestión de Aparatos",
            command=self.abrir_aparatos,
            width=25,
            height=2,
            font=("Arial", 12),
            bg="#2ecc71",
            fg="white",
            cursor="hand2"
        )
        btn_aparatos.grid(row=0, column=1, padx=15, pady=15)
        
        # Botón Gestión de Reservas
        btn_reservas = tk.Button(
            frame_botones,
            text="Gestión de Reservas",
            command=self.abrir_reservas,
            width=25,
            height=2,
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            cursor="hand2"
        )
        btn_reservas.grid(row=1, column=0, padx=15, pady=15)
        
        # Botón Gestión de Pagos
        btn_pagos = tk.Button(
            frame_botones,
            text="Gestión de Pagos",
            command=self.abrir_pagos,
            width=25,
            height=2,
            font=("Arial", 12),
            bg="#f39c12",
            fg="white",
            cursor="hand2"
        )
        btn_pagos.grid(row=1, column=1, padx=15, pady=15)
        
        # Botón Salir
        btn_salir = tk.Button(
            self.root,
            text="Salir",
            command=self.salir,
            width=15,
            font=("Arial", 10),
            bg="#95a5a6",
            fg="white",
            cursor="hand2"
        )
        btn_salir.pack(pady=30)
    
    def abrir_clientes(self):
        """Abre la ventana de gestión de clientes"""
        ventana = tk.Toplevel(self.root)
        ClienteView(ventana)
    
    def abrir_aparatos(self):
        """Abre la ventana de gestión de aparatos"""
        ventana = tk.Toplevel(self.root)
        AparatoView(ventana)
    
    def abrir_reservas(self):
        """Abre la ventana de gestión de reservas"""
        ventana = tk.Toplevel(self.root)
        ReservaView(ventana)
    
    def abrir_pagos(self):
        """Abre la ventana de gestión de pagos"""
        ventana = tk.Toplevel(self.root)
        PagoView(ventana)
    
    def salir(self):
        """Cierra la aplicación"""
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir?"):
            self.root.quit()

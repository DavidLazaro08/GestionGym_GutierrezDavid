"""
Vista de Clientes (Rediseño Dark Neon)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from controller.cliente_controller import ClienteController
from util.helpers import formatear_fecha, obtener_fecha_actual
from util.validaciones import validar_dni, validar_email, validar_telefono
from resources.style.colores import *

class ClienteView(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent, bg=COLOR_FONDO)
        self.main_window = main_window
        self.controller = ClienteController()
        self.id_cliente_seleccionado = None
        
        self._configurar_estilos_treeview()
        self._configurar_interfaz()
        self._cargar_clientes()

    def _configurar_estilos_treeview(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Estilo para el Treeview Dark
        style.configure(
            "Treeview",
            background="#161b22",
            foreground="white",
            fieldbackground="#161b22",
            borderwidth=0,
            font=("Segoe UI", 10),
            rowheight=30
        )
        
        style.configure(
            "Treeview.Heading",
            background="#0d1117",
            foreground=COLOR_SECUNDARIO,
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )
        
        style.map("Treeview.Heading", background=[("active", "#161b22")])
        style.map("Treeview", background=[("selected", COLOR_SECUNDARIO)], foreground=[("selected", "#000000")])

    def _configurar_interfaz(self):
        # Header
        header = tk.Frame(self, bg=COLOR_FONDO)
        header.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            header, text="Gestión de Clientes",
            font=FUENTE_TITULO, bg=COLOR_FONDO, fg="white"
        ).pack(anchor="w")
        
        tk.Label(
            header, text="Administra los socios del gimnasio",
            font=("Segoe UI", 11), bg=COLOR_FONDO, fg=COLOR_TEXTO_SECUNDARIO
        ).pack(anchor="w")

        # Contenedor Principal (Card)
        card = tk.Frame(self, bg=COLOR_FONDO_CARD)
        card.pack(fill="both", expand=True)

        # ---------------------------------------------------------
        # FORMULARIO (Dos columnas)
        # ---------------------------------------------------------
        form_frame = tk.Frame(card, bg=COLOR_FONDO_CARD)
        form_frame.pack(fill="x", padx=30, pady=30)
        
        # Grid Config
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)

        # Columna 1
        self.entry_nombre = self._crear_input_moderno(form_frame, "Nombre", 0, 0)
        self.entry_dni = self._crear_input_moderno(form_frame, "DNI", 1, 0)
        self.entry_telefono = self._crear_input_moderno(form_frame, "Teléfono", 2, 0)
        
        # Columna 2
        self.entry_apellidos = self._crear_input_moderno(form_frame, "Apellidos", 0, 1)
        self.entry_email = self._crear_input_moderno(form_frame, "Email", 1, 1)
        
        # Combo Estado (Custom Frame simple)
        frame_estado = tk.Frame(form_frame, bg=COLOR_FONDO_CARD)
        frame_estado.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        
        tk.Label(frame_estado, text="ESTADO", font=("Segoe UI", 8, "bold"), fg=COLOR_TEXTO_SECUNDARIO, bg=COLOR_FONDO_CARD).pack(anchor="w", pady=(0, 5))
        
        self.combo_estado = ttk.Combobox(frame_estado, values=["activo", "inactivo"], state="readonly", font=FUENTE_NORMAL)
        self.combo_estado.pack(fill="x", ipady=4)
        self.combo_estado.current(0)

        # ---------------------------------------------------------
        # BOTONERA ACCIONES
        # ---------------------------------------------------------
        btn_frame = tk.Frame(card, bg=COLOR_FONDO_CARD)
        btn_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        self._crear_boton(btn_frame, "NUEVO", self._nuevo_cliente, ESTILO_BOTON_SECUNDARIO).pack(side="left", padx=(0, 10))
        self._crear_boton(btn_frame, "GUARDAR", self._guardar_cliente, ESTILO_BOTON_EXITO).pack(side="left", padx=(0, 10))
        self._crear_boton(btn_frame, "MODIFICAR", self._modificar_cliente, ESTILO_BOTON_ADVERTENCIA).pack(side="left", padx=(0, 10))
        self._crear_boton(btn_frame, "ELIMINAR", self._eliminar_cliente, ESTILO_BOTON_PELIGRO).pack(side="left")

        # ---------------------------------------------------------
        # BUSCADOR Y TABLA
        # ---------------------------------------------------------
        search_frame = tk.Frame(card, bg=COLOR_FONDO_CARD)
        search_frame.pack(fill="x", padx=30, pady=(10, 10))
        
        self.entry_buscar = tk.Entry(search_frame, bg="#0d1117", fg="white", insertbackground=COLOR_SECUNDARIO,
                                     font=FUENTE_NORMAL, relief="flat", bd=1)
        self.entry_buscar.pack(side="left", fill="x", expand=True, ipady=5, padx=(0, 10))
        
        self._crear_boton(search_frame, "BUSCAR", self._buscar_clientes, ESTILO_BOTON_INFO).pack(side="left")
        self._crear_boton(search_frame, "VER TODOS", self._cargar_clientes, ESTILO_BOTON_NEUTRAL).pack(side="left", padx=(10, 0))

        # Tabla
        table_frame = tk.Frame(card, bg=COLOR_FONDO_CARD)
        table_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        scrollbar_y = tk.Scrollbar(table_frame)
        scrollbar_y.pack(side="right", fill="y")
        
        cols = ("ID", "Nombre", "Apellidos", "DNI", "Email", "Teléfono", "Fecha", "Estado")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", yscrollcommand=scrollbar_y.set)
        scrollbar_y.config(command=self.tree.yview)
        
        for col in cols:
            self.tree.heading(col, text=col)
            width = 50 if col == "ID" else 150
            self.tree.column(col, width=width)
            
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._seleccionar_cliente)

    def _crear_input_moderno(self, parent, label, row, col):
        """Crea un campo de entrada con estilo dark/neon."""
        frame = tk.Frame(parent, bg=COLOR_FONDO_CARD)
        frame.grid(row=row, column=col, padx=20, pady=10, sticky="ew")
        
        # Label
        tk.Label(
            frame, text=label.upper(), font=("Segoe UI", 8, "bold"),
            fg=COLOR_TEXTO_SECUNDARIO, bg=COLOR_FONDO_CARD
        ).pack(anchor="w", pady=(0, 5))
        
        # Borde contenedor
        border = tk.Frame(frame, bg=COLOR_INPUT_BORDER, padx=1, pady=1)
        border.pack(fill="x")
        
        # Entry
        entry = tk.Entry(
            border, bg=COLOR_INPUT_BG, fg="white",
            insertbackground=COLOR_SECUNDARIO, font=FUENTE_NORMAL,
            relief="flat", bd=5 # Padding interno simulado
        )
        entry.pack(fill="x")
        
        # Efectos Focus
        def on_focus_in(e): border.config(bg=COLOR_SECUNDARIO)
        def on_focus_out(e): border.config(bg=COLOR_INPUT_BORDER)
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        
        return entry

    def _crear_boton(self, parent, text, command, style_dict):
        btn = tk.Button(parent, text=text, command=command, **style_dict)
        return btn

    # ---------------------------------------------------------
    #   LÓGICA CRUD
    # ---------------------------------------------------------
    def _validar_datos(self):
        nombre = self.entry_nombre.get().strip()
        apellidos = self.entry_apellidos.get().strip()
        dni = self.entry_dni.get().strip()
        
        if not nombre or not apellidos or not dni:
            messagebox.showwarning("Faltan datos", "Nombre, Apellidos y DNI son obligatorios.")
            return False
        return True 

    def _nuevo_cliente(self):
        self._limpiar_formulario()

    def _guardar_cliente(self):
        if not self._validar_datos(): return
        
        try:
            self.controller.crear_cliente(
                self.entry_nombre.get(), self.entry_apellidos.get(),
                self.entry_dni.get(), self.entry_email.get(),
                self.entry_telefono.get(), obtener_fecha_actual()
            )
            messagebox.showinfo("Éxito", "Cliente creado.")
            self._limpiar_formulario()
            self._cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _modificar_cliente(self):
        if not self.id_cliente_seleccionado: return
        try:
            self.controller.actualizar_cliente(
                self.id_cliente_seleccionado, nombre=self.entry_nombre.get(),
                apellidos=self.entry_apellidos.get(), dni=self.entry_dni.get(),
                email=self.entry_email.get(), telefono=self.entry_telefono.get(),
                estado=self.combo_estado.get()
            )
            messagebox.showinfo("Éxito", "Cliente actualizado.")
            self._cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _eliminar_cliente(self):
        if not self.id_cliente_seleccionado: return
        if messagebox.askyesno("Confirmar", "¿Eliminar cliente?"):
            self.controller.eliminar_cliente(self.id_cliente_seleccionado)
            self._limpiar_formulario()
            self._cargar_clientes()

    def _cargar_clientes(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        clientes = self.controller.obtener_todos_clientes()
        for c in clientes:
            self.tree.insert("", "end", values=(c.id_cliente, c.nombre, c.apellidos, c.dni, c.email, c.telefono, c.fecha_alta, c.estado))

    def _buscar_clientes(self):
        criterio = self.entry_buscar.get()
        if not criterio: return
        for item in self.tree.get_children(): self.tree.delete(item)
        clientes = self.controller.buscar_clientes(criterio)
        for c in clientes:
            self.tree.insert("", "end", values=(c.id_cliente, c.nombre, c.apellidos, c.dni, c.email, c.telefono, c.fecha_alta, c.estado))

    def _seleccionar_cliente(self, event):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0])["values"]
        self.id_cliente_seleccionado = vals[0]
        
        self.entry_nombre.delete(0, "end"); self.entry_nombre.insert(0, vals[1])
        self.entry_apellidos.delete(0, "end"); self.entry_apellidos.insert(0, vals[2])
        self.entry_dni.delete(0, "end"); self.entry_dni.insert(0, vals[3])
        self.entry_email.delete(0, "end"); self.entry_email.insert(0, vals[4])
        self.entry_telefono.delete(0, "end"); self.entry_telefono.insert(0, vals[5])
        self.combo_estado.set(vals[7])

    def _limpiar_formulario(self):
        self.id_cliente_seleccionado = None
        self.entry_nombre.delete(0, "end")
        self.entry_apellidos.delete(0, "end")
        self.entry_dni.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.entry_telefono.delete(0, "end")
        self.combo_estado.current(0)

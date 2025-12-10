"""
Vista de Clientes
Pantalla para gestionar los socios del gimnasio.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from controller.cliente_controller import ClienteController
from util.helpers import formatear_fecha, obtener_fecha_actual
from util.validaciones import validar_dni, validar_email, validar_telefono
from resources.style.colores import *

# Colores propios de esta vista (modo oscuro)
R_COLOR_PANEL = "#151C25"
R_COLOR_BORDE_PANEL = "#00d4aa"   # Turquesa
R_COLOR_INPUT_BG = "#0F1620"
R_COLOR_INPUT_TEXT = "#E4E8EC"
R_COLOR_PLACEHOLDER = "#8A96A8"
R_COLOR_BTN_NUEVO = "#00d4aa"
R_COLOR_BTN_GUARDAR = "#3CA9FF"
R_COLOR_BTN_MODIFICAR = "#FF9F45"
R_COLOR_BTN_ELIMINAR = "#FF4F4F"
R_COLOR_TABLA_BG = "#10171E"
R_COLOR_TABLA_LINES = "#2B3440"
R_COLOR_TABLA_HEAD = "#1D2630"


class ClienteView(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent, bg=COLOR_FONDO)
        self.main_window = main_window
        self.controller = ClienteController()
        self.id_cliente_seleccionado = None

        self._configurar_estilos_treeview()
        self._configurar_interfaz()
        self._cargar_clientes()

    # ---------------------------------------------------------
    #   ESTILOS
    # ---------------------------------------------------------
    def _configurar_estilos_treeview(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Estilo base para la tabla
        style.configure(
            "Treeview",
            background=R_COLOR_TABLA_BG,
            foreground="white",
            fieldbackground=R_COLOR_TABLA_BG,
            borderwidth=0,
            font=("Segoe UI", 10),
            rowheight=25
        )

        # Cabecera de la tabla
        style.configure(
            "Treeview.Heading",
            background=R_COLOR_TABLA_HEAD,
            foreground="white",
            relief="flat",
            font=("Segoe UI", 11, "bold")
        )

        style.map("Treeview.Heading", background=[("active", R_COLOR_TABLA_HEAD)])
        style.map(
            "Treeview",
            background=[("selected", "#00d4aa")],
            foreground=[("selected", "black")]
        )

    # ---------------------------------------------------------
    #   INTERFAZ
    # ---------------------------------------------------------
    def _configurar_interfaz(self):
        # Cabecera
        header = tk.Frame(self, bg=COLOR_FONDO)
        header.pack(fill="x", pady=(0, 15))

        tk.Label(
            header,
            text="Gestión de Clientes",
            font=("Segoe UI", 24, "bold"),
            bg=COLOR_FONDO,
            fg="#00d4aa"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Administra los socios del gimnasio",
            font=("Segoe UI", 11),
            bg=COLOR_FONDO,
            fg="#A9B4C6"
        ).pack(anchor="w")

        # Contenedor principal con borde turquesa
        borde_card = tk.Frame(self, bg=R_COLOR_BORDE_PANEL, padx=1, pady=1)
        borde_card.pack(fill="both", expand=True)

        card = tk.Frame(borde_card, bg=R_COLOR_PANEL)
        card.pack(fill="both", expand=True)

        # -------- FORMULARIO --------
        form_frame = tk.Frame(card, bg=R_COLOR_PANEL)
        form_frame.pack(fill="x", padx=20, pady=15)

        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)

        # Columna 1
        self.entry_nombre = self._crear_input_refinado(form_frame, "Nombre", 0, 0)
        self.entry_dni = self._crear_input_refinado(form_frame, "DNI", 1, 0)
        self.entry_telefono = self._crear_input_refinado(form_frame, "Teléfono", 2, 0)

        # Columna 2
        self.entry_apellidos = self._crear_input_refinado(form_frame, "Apellidos", 0, 1)
        self.entry_email = self._crear_input_refinado(form_frame, "Email", 1, 1)

        # Estado
        frame_estado = tk.Frame(form_frame, bg=R_COLOR_PANEL)
        frame_estado.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(
            frame_estado,
            text="ESTADO",
            font=("Segoe UI", 9, "bold"),
            fg="#A9B4C6",
            bg=R_COLOR_PANEL
        ).pack(anchor="w", pady=(0, 2))

        self.combo_estado = ttk.Combobox(
            frame_estado,
            values=["activo", "inactivo"],
            state="readonly",
            font=("Segoe UI", 11)
        )
        self.combo_estado.pack(fill="x", ipady=6)
        self.combo_estado.current(0)

        # -------- BOTONES --------
        btn_frame = tk.Frame(card, bg=R_COLOR_PANEL)
        btn_frame.pack(fill="x", padx=20, pady=(10, 15))

        self._crear_boton_refinado(
            btn_frame, "NUEVO", self._nuevo_cliente, R_COLOR_BTN_NUEVO
        ).pack(side="left", padx=(0, 15))

        self._crear_boton_refinado(
            btn_frame, "GUARDAR", self._guardar_cliente, R_COLOR_BTN_GUARDAR
        ).pack(side="left", padx=(0, 15))

        self._crear_boton_refinado(
            btn_frame, "MODIFICAR", self._modificar_cliente, R_COLOR_BTN_MODIFICAR
        ).pack(side="left", padx=(0, 15))

        self._crear_boton_refinado(
            btn_frame, "ELIMINAR", self._eliminar_cliente, R_COLOR_BTN_ELIMINAR
        ).pack(side="left")

        # -------- BUSCADOR --------
        search_frame = tk.Frame(card, bg=R_COLOR_PANEL)
        search_frame.pack(fill="x", padx=20, pady=(5, 10))

        b_search = tk.Frame(search_frame, bg=R_COLOR_BORDE_PANEL, padx=1, pady=1)
        b_search.pack(side="left", fill="x", expand=True, padx=(0, 15))

        self.entry_buscar = tk.Entry(
            b_search,
            bg=R_COLOR_INPUT_BG,
            fg=R_COLOR_INPUT_TEXT,
            insertbackground="#00d4aa",
            font=("Segoe UI", 11),
            relief="flat",
            bd=8
        )
        self.entry_buscar.pack(fill="x")

        self._crear_boton_refinado(
            search_frame, "BUSCAR", self._buscar_clientes, "#3498db"
        ).pack(side="left")

        self._crear_boton_refinado(
            search_frame, "VER TODOS", self._cargar_clientes, "#95a5a6"
        ).pack(side="left", padx=(10, 0))

        # -------- TABLA --------
        table_frame = tk.Frame(card, bg=R_COLOR_PANEL)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        scrollbar_y = tk.Scrollbar(table_frame)
        scrollbar_y.pack(side="right", fill="y")

        cols = ("ID", "Nombre", "Apellidos", "DNI", "Email", "Teléfono", "Fecha", "Estado")
        self.tree = ttk.Treeview(
            table_frame,
            columns=cols,
            show="headings",
            yscrollcommand=scrollbar_y.set
        )
        scrollbar_y.config(command=self.tree.yview)

        for col in cols:
            self.tree.heading(col, text=col)
            width = 60 if col == "ID" else 160
            self.tree.column(col, width=width)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._seleccionar_cliente)

    # Crea un input con su etiqueta y borde turquesa
    def _crear_input_refinado(self, parent, label, row, col):
        frame = tk.Frame(parent, bg=R_COLOR_PANEL)
        frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")

        tk.Label(
            frame,
            text=label.upper(),
            font=("Segoe UI", 9, "bold"),
            fg="#A9B4C6",
            bg=R_COLOR_PANEL
        ).pack(anchor="w", pady=(0, 2))

        border = tk.Frame(frame, bg=R_COLOR_BORDE_PANEL, padx=1, pady=1)
        border.pack(fill="x")

        entry = tk.Entry(
            border,
            bg=R_COLOR_INPUT_BG,
            fg=R_COLOR_INPUT_TEXT,
            insertbackground="#00d4aa",
            font=("Segoe UI", 11),
            relief="flat",
            bd=5
        )
        entry.pack(fill="x")

        return entry

    # Crea un botón con efecto hover sencillo
    def _crear_boton_refinado(self, parent, text, cmd, bg_color):
        btn = tk.Button(
            parent,
            text=text,
            command=cmd,
            bg=bg_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            activebackground="white",
            activeforeground=bg_color,
            cursor="hand2",
            padx=20,
            pady=5
        )

        def on_enter(e):
            btn["bg"] = self._lighten_color(bg_color)

        def on_leave(e):
            btn["bg"] = bg_color

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def _lighten_color(self, color, factor=1.2):
        # Mapa simple de colores para el efecto hover
        hover_map = {
            R_COLOR_BTN_NUEVO: "#33e0c0",
            R_COLOR_BTN_GUARDAR: "#6ac0ff",
            R_COLOR_BTN_MODIFICAR: "#ffb46e",
            R_COLOR_BTN_ELIMINAR: "#ff7676",
            "#3498db": "#5dade2",
            "#95a5a6": "#b2babb",
        }
        return hover_map.get(color, color)

    # ---------------------------------------------------------
    #   LÓGICA / CRUD
    # ---------------------------------------------------------
    def _validar_datos(self):
        nombre = self.entry_nombre.get().strip()
        apellidos = self.entry_apellidos.get().strip()
        dni = self.entry_dni.get().strip()

        if not nombre or not apellidos or not dni:
            messagebox.showwarning(
                "Faltan datos",
                "Nombre, Apellidos y DNI son obligatorios."
            )
            return False
        return True

    def _nuevo_cliente(self):
        self._limpiar_formulario()

    def _guardar_cliente(self):
        if not self._validar_datos():
            return

        try:
            self.controller.crear_cliente(
                self.entry_nombre.get(),
                self.entry_apellidos.get(),
                self.entry_dni.get(),
                self.entry_email.get(),
                self.entry_telefono.get(),
                obtener_fecha_actual()
            )
            messagebox.showinfo("Éxito", "Cliente creado.")
            self._limpiar_formulario()
            self._cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _modificar_cliente(self):
        if not self.id_cliente_seleccionado:
            return
        try:
            self.controller.actualizar_cliente(
                self.id_cliente_seleccionado,
                nombre=self.entry_nombre.get(),
                apellidos=self.entry_apellidos.get(),
                dni=self.entry_dni.get(),
                email=self.entry_email.get(),
                telefono=self.entry_telefono.get(),
                estado=self.combo_estado.get()
            )
            messagebox.showinfo("Éxito", "Cliente actualizado.")
            self._cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _eliminar_cliente(self):
        if not self.id_cliente_seleccionado:
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar cliente?"):
            self.controller.eliminar_cliente(self.id_cliente_seleccionado)
            self._limpiar_formulario()
            self._cargar_clientes()

    # ---------------------------------------------------------
    #   TABLA
    # ---------------------------------------------------------
    def _cargar_clientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        clientes = self.controller.obtener_todos_clientes()
        for c in clientes:
            self.tree.insert(
                "",
                "end",
                values=(
                    c.id_cliente,
                    c.nombre,
                    c.apellidos,
                    c.dni,
                    c.email,
                    c.telefono,
                    c.fecha_alta,
                    c.estado
                )
            )

    def _buscar_clientes(self):
        criterio = self.entry_buscar.get()
        if not criterio:
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        clientes = self.controller.buscar_clientes(criterio)
        for c in clientes:
            self.tree.insert(
                "",
                "end",
                values=(
                    c.id_cliente,
                    c.nombre,
                    c.apellidos,
                    c.dni,
                    c.email,
                    c.telefono,
                    c.fecha_alta,
                    c.estado
                )
            )

    def _seleccionar_cliente(self, event):
        sel = self.tree.selection()
        if not sel:
            return

        vals = self.tree.item(sel[0])["values"]
        self.id_cliente_seleccionado = vals[0]

        self.entry_nombre.delete(0, "end")
        self.entry_nombre.insert(0, vals[1])

        self.entry_apellidos.delete(0, "end")
        self.entry_apellidos.insert(0, vals[2])

        self.entry_dni.delete(0, "end")
        self.entry_dni.insert(0, vals[3])

        self.entry_email.delete(0, "end")
        self.entry_email.insert(0, vals[4])

        self.entry_telefono.delete(0, "end")
        self.entry_telefono.insert(0, vals[5])

        self.combo_estado.set(vals[7])

    # ---------------------------------------------------------
    #   LIMPIEZA FORMULARIO
    # ---------------------------------------------------------
    def _limpiar_formulario(self):
        self.id_cliente_seleccionado = None
        self.entry_nombre.delete(0, "end")
        self.entry_apellidos.delete(0, "end")
        self.entry_dni.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.entry_telefono.delete(0, "end")
        self.combo_estado.current(0)

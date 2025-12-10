"""
Vista de Pagos (tema dark / neon)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from controller.pago_controller import PagoController
from controller.cliente_controller import ClienteController
from util.helpers import formatear_fecha, formatear_cuota
from util.validaciones import validar_fecha
from view.ventana_pago import VentanaPago
from resources.style.colores import *

# Paleta usada en el resto de vistas dark
R_COLOR_PANEL = "#151C25"
R_COLOR_BORDE_PANEL = "#00d4aa"
R_COLOR_INPUT_BG = "#0F1620"
R_COLOR_INPUT_TEXT = "#E4E8EC"
R_COLOR_BTN_GENERAR = "#00d4aa"
R_COLOR_BTN_FILTRAR = "#3498db"
R_COLOR_BTN_TODOS = "#95a5a6"
R_COLOR_BTN_PENDIENTES = "#f39c12"
R_COLOR_BTN_PAGAR = "#2ecc71"
R_COLOR_BTN_ELIMINAR = "#e74c3c"
R_COLOR_TABLA_BG = "#10171E"
R_COLOR_TABLA_HEAD = "#1D2630"


class PagoView(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent, bg=COLOR_FONDO)
        self.main_window = main_window

        self.controller = PagoController()
        self.cliente_controller = ClienteController()

        # id_cliente → "Nombre Apellidos"
        self.clientes_dict = {}
        self.id_pago_seleccionado = None

        self._configurar_estilos_treeview()
        self._configurar_interfaz()
        self.cargar_clientes()
        self.cargar_pagos()

    # --------- ESTILOS TABLA ---------
    def _configurar_estilos_treeview(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=R_COLOR_TABLA_BG,
            foreground="white",
            fieldbackground=R_COLOR_TABLA_BG,
            borderwidth=0,
            font=("Segoe UI", 10),
            rowheight=25,
        )

        style.configure(
            "Treeview.Heading",
            background=R_COLOR_TABLA_HEAD,
            foreground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
        )

        style.map("Treeview.Heading", background=[("active", R_COLOR_TABLA_HEAD)])
        style.map(
            "Treeview",
            background=[("selected", "#00d4aa")],
            foreground=[("selected", "black")],
        )

    # --------- INTERFAZ ---------
    def _configurar_interfaz(self):
        # Cabecera
        header = tk.Frame(self, bg=COLOR_FONDO)
        header.pack(fill="x", pady=(0, 15))

        tk.Label(
            header,
            text="Gestión de Pagos",
            font=("Segoe UI", 24, "bold"),
            bg=COLOR_FONDO,
            fg="#00d4aa",
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Control mensual de cuotas",
            font=("Segoe UI", 11),
            bg=COLOR_FONDO,
            fg="#A9B4C6",
        ).pack(anchor="w")

        # Contenedor principal con borde
        borde_card = tk.Frame(self, bg=R_COLOR_BORDE_PANEL, padx=1, pady=1)
        borde_card.pack(fill="both", expand=True)

        card = tk.Frame(borde_card, bg=R_COLOR_PANEL)
        card.pack(fill="both", expand=True)

        # --- Generar pagos del mes ---
        frame_generar = tk.Frame(card, bg=R_COLOR_PANEL)
        frame_generar.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            frame_generar,
            text="GENERAR PAGOS MENSUALES",
            font=("Segoe UI", 9, "bold"),
            fg="#A9B4C6",
            bg=R_COLOR_PANEL,
        ).pack(anchor="w", pady=(0, 5))

        cont_cols_gen = tk.Frame(frame_generar, bg=R_COLOR_PANEL)
        cont_cols_gen.pack(fill="x")

        self.combo_mes = ttk.Combobox(
            cont_cols_gen,
            values=[
                "01 - Enero",
                "02 - Febrero",
                "03 - Marzo",
                "04 - Abril",
                "05 - Mayo",
                "06 - Junio",
                "07 - Julio",
                "08 - Agosto",
                "09 - Septiembre",
                "10 - Octubre",
                "11 - Noviembre",
                "12 - Diciembre",
            ],
            state="readonly",
            width=15,
            font=("Segoe UI", 10),
        )
        self.combo_mes.pack(side="left", padx=(0, 10))

        self.combo_anio = ttk.Combobox(
            cont_cols_gen,
            values=[str(a) for a in range(2023, 2032)],
            state="readonly",
            width=8,
            font=("Segoe UI", 10),
        )
        self.combo_anio.pack(side="left", padx=(0, 15))

        hoy = datetime.now()
        self.combo_mes.current(hoy.month - 1)
        self.combo_anio.set(str(hoy.year))

        self._crear_boton_refinado(
            cont_cols_gen, "GENERAR", self.generar_pagos_mes, R_COLOR_BTN_GENERAR
        ).pack(side="left")

        # --- Filtros ---
        frame_filtros = tk.Frame(card, bg=R_COLOR_PANEL)
        frame_filtros.pack(fill="x", padx=20, pady=(10, 10))

        tk.Label(
            frame_filtros,
            text="FILTROS",
            font=("Segoe UI", 9, "bold"),
            fg="#A9B4C6",
            bg=R_COLOR_PANEL,
        ).pack(anchor="w", pady=(0, 5))

        cont_cols_filt = tk.Frame(frame_filtros, bg=R_COLOR_PANEL)
        cont_cols_filt.pack(fill="x")

        self.combo_filtro_cliente = ttk.Combobox(
            cont_cols_filt, width=30, state="readonly", font=("Segoe UI", 10)
        )
        self.combo_filtro_cliente.pack(side="left", padx=(0, 15))

        self._crear_boton_refinado(
            cont_cols_filt, "FILTRAR", self.filtrar_por_cliente, R_COLOR_BTN_FILTRAR
        ).pack(side="left", padx=(0, 10))

        self._crear_boton_refinado(
            cont_cols_filt, "VER TODOS", self.cargar_pagos, R_COLOR_BTN_TODOS
        ).pack(side="left", padx=(0, 10))

        self._crear_boton_refinado(
            cont_cols_filt, "PENDIENTES", self.mostrar_pendientes, R_COLOR_BTN_PENDIENTES
        ).pack(side="left")

        # --- Acciones sobre la tabla ---
        frame_acciones = tk.Frame(card, bg=R_COLOR_PANEL)
        frame_acciones.pack(fill="x", padx=20, pady=(15, 5))

        self._crear_boton_refinado(
            frame_acciones,
            "MARCAR PAGADO",
            self.marcar_pagado,
            R_COLOR_BTN_PAGAR,
        ).pack(side="left", padx=(0, 15))

        self._crear_boton_refinado(
            frame_acciones, "ELIMINAR", self.eliminar_pago, R_COLOR_BTN_ELIMINAR
        ).pack(side="left")

        # --- Tabla ---
        table_frame = tk.Frame(card, bg=R_COLOR_PANEL)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        scrollbar_y = tk.Scrollbar(table_frame)
        scrollbar_y.pack(side="right", fill="y")

        columnas = ("ID", "Cliente", "Mes", "Estado", "Cuota", "F. Pago", "Método")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columnas,
            show="headings",
            yscrollcommand=scrollbar_y.set,
        )
        scrollbar_y.config(command=self.tree.yview)

        for col in columnas:
            self.tree.heading(col, text=col)
            width = 50 if col == "ID" else 100
            if col == "Cliente":
                width = 180
            self.tree.column(col, width=width)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_pago)

    # --------- BOTONES ---------
    def _crear_boton_refinado(self, parent, text, cmd, bg_color):
        btn = tk.Button(
            parent,
            text=text,
            command=cmd,
            bg=bg_color,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            activebackground="white",
            activeforeground=bg_color,
            cursor="hand2",
            padx=15,
            pady=4,
        )

        def on_enter(e):
            btn["bg"] = self._lighten_color(bg_color)

        def on_leave(e):
            btn["bg"] = bg_color

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def _lighten_color(self, color):
        hover_map = {
            R_COLOR_BTN_GENERAR: "#33e0c0",
            R_COLOR_BTN_FILTRAR: "#5dade2",
            R_COLOR_BTN_TODOS: "#b2babb",
            R_COLOR_BTN_PENDIENTES: "#f5b041",
            R_COLOR_BTN_PAGAR: "#58d68d",
            R_COLOR_BTN_ELIMINAR: "#ec7063",
        }
        return hover_map.get(color, color)

    # --------- CARGA DE CLIENTES Y PAGOS ---------
    def cargar_clientes(self):
        try:
            clientes = self.cliente_controller.obtener_todos_clientes()
            valores = []

            for c in clientes:
                texto = f"{c.id_cliente} - {c.nombre} {c.apellidos}"
                valores.append(texto)
                self.clientes_dict[c.id_cliente] = f"{c.nombre} {c.apellidos}"

            self.combo_filtro_cliente["values"] = valores

        except Exception as e:
            messagebox.showerror("Error cargando clientes", str(e))

    def generar_pagos_mes(self):
        try:
            mes_num = self.combo_mes.get().split(" ")[0]
            anio = self.combo_anio.get()
            mes_formato = f"{anio}-{mes_num}"

            cantidad = self.controller.generar_pagos_mensuales(mes_formato)

            messagebox.showinfo(
                "Pagos generados",
                f"Se han creado {cantidad} pagos pendientes.",
            )
            self.cargar_pagos()

        except Exception as e:
            messagebox.showerror("Error generando pagos", str(e))

    def cargar_pagos(self):
        try:
            self.tree.delete(*self.tree.get_children())
            pagos = self.controller.obtener_todos_pagos()

            for p in pagos:
                nombre = self.clientes_dict.get(p.id_cliente, "Desconocido")
                estado = "Pagado" if p.pagado else "Pendiente"

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        p.id_pago,
                        nombre,
                        p.mes,
                        estado,
                        formatear_cuota(p.cuota),
                        formatear_fecha(p.fecha_pago),
                        p.metodo_pago or "",
                    ),
                )

        except Exception as e:
            messagebox.showerror("Error cargando pagos", str(e))

    def mostrar_pendientes(self):
        try:
            self.tree.delete(*self.tree.get_children())
            pagos = self.controller.obtener_todos_pagos()

            for p in pagos:
                if not p.pagado:
                    nombre = self.clientes_dict.get(p.id_cliente, "Desconocido")

                    self.tree.insert(
                        "",
                        "end",
                        values=(
                            p.id_pago,
                            nombre,
                            p.mes,
                            "Pendiente",
                            formatear_cuota(p.cuota),
                            "",
                            "",
                        ),
                    )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --------- FILTROS ---------
    def filtrar_por_cliente(self):
        texto = self.combo_filtro_cliente.get()
        if not texto:
            return

        try:
            id_cliente = int(texto.split(" ")[0])
            self.tree.delete(*self.tree.get_children())

            pagos = self.controller.obtener_pagos_por_cliente(id_cliente)

            for p in pagos:
                estado = "Pagado" if p.pagado else "Pendiente"
                nombre = self.clientes_dict.get(id_cliente, "Desconocido")

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        p.id_pago,
                        nombre,
                        p.mes,
                        estado,
                        formatear_cuota(p.cuota),
                        formatear_fecha(p.fecha_pago),
                        p.metodo_pago or "",
                    ),
                )

        except Exception as e:
            messagebox.showerror("Error filtrando pagos", str(e))

    # --------- SELECCIÓN / ACCIONES ---------
    def seleccionar_pago(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            valores = self.tree.item(seleccion[0])["values"]
            self.id_pago_seleccionado = valores[0]

    def marcar_pagado(self):
        if not self.id_pago_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un pago.")
            return

        try:
            pago_obj = self.controller.obtener_pago(self.id_pago_seleccionado)

            if pago_obj.pagado:
                messagebox.showinfo(
                    "Pago ya registrado", "Este pago ya está pagado."
                )
                return

            datos_pago = {
                "id_pago": pago_obj.id_pago,
                "cliente": self.clientes_dict.get(
                    pago_obj.id_cliente, "Desconocido"
                ),
                "mes": pago_obj.mes,
                "cuota": pago_obj.cuota,
            }

            def callback_confirmacion(metodo, fecha, concepto):
                if not metodo:
                    messagebox.showerror(
                        "Error", "Debe seleccionar un método de pago."
                    )
                    return

                if not validar_fecha(fecha):
                    messagebox.showerror(
                        "Fecha inválida", "Use el formato YYYY-MM-DD."
                    )
                    return

                try:
                    self.controller.marcar_pago_como_pagado(
                        self.id_pago_seleccionado,
                        fecha,
                        metodo,
                        concepto,
                    )
                    messagebox.showinfo(
                        "Éxito", "Pago marcado correctamente."
                    )
                    self.cargar_pagos()

                except Exception as e:
                    messagebox.showerror(
                        "Error al registrar pago", str(e)
                    )

            VentanaPago(self, datos_pago, callback_confirmacion)

        except Exception as e:
            messagebox.showerror("Error al cargar pago", str(e))

    def eliminar_pago(self):
        if not self.id_pago_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un pago.")
            return

        if not messagebox.askyesno("Confirmar", "¿Eliminar pago?"):
            return

        try:
            self.controller.eliminar_pago(self.id_pago_seleccionado)
            self.cargar_pagos()
            self.id_pago_seleccionado = None

        except Exception as e:
            messagebox.showerror("Error eliminando pago", str(e))

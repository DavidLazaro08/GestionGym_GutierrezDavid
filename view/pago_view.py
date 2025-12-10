"""
Vista de Pagos (Rediseño Matrix/Neon)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controller.pago_controller import PagoController
from controller.cliente_controller import ClienteController
from util.helpers import formatear_fecha, formatear_cuota
from view.ventana_pago import VentanaPago
from resources.style.colores import *

# --- ESTILOS MATRIX / NEON REFINADOS (Copiados de ClienteView) ---
R_COLOR_PANEL = "#151C25"
R_COLOR_BORDE_PANEL = "#00d4aa"  # Turquesa
R_COLOR_INPUT_BG = "#0F1620"
R_COLOR_INPUT_TEXT = "#E4E8EC"
R_COLOR_PLACEHOLDER = "#8A96A8"
R_COLOR_BTN_GENERAR = "#00d4aa"        # Turquesa
R_COLOR_BTN_FILTRAR = "#3498db"        # Azul
R_COLOR_BTN_TODOS = "#95a5a6"          # Gris
R_COLOR_BTN_PENDIENTES = "#f39c12"     # Naranja
R_COLOR_BTN_PAGAR = "#2ecc71"          # Verde
R_COLOR_BTN_ELIMINAR = "#e74c3c"       # Rojo
R_COLOR_TABLA_BG = "#10171E"
R_COLOR_TABLA_HEAD = "#1D2630"

class PagoView(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent, bg=COLOR_FONDO)
        self.main_window = main_window
        self.controller = PagoController()
        self.cliente_controller = ClienteController()
        
        self.clientes_dict = {}
        self.id_pago_seleccionado = None
        
        self._configurar_estilos_treeview()
        self._configurar_interfaz()
        self.cargar_clientes()
        self.cargar_pagos()

    def _configurar_estilos_treeview(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Estilo Matrix Compacto
        style.configure(
            "Treeview",
            background=R_COLOR_TABLA_BG,
            foreground="white",
            fieldbackground=R_COLOR_TABLA_BG,
            borderwidth=0,
            font=("Segoe UI", 10),
            rowheight=25
        )
        
        style.configure(
            "Treeview.Heading",
            background=R_COLOR_TABLA_HEAD,
            foreground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )
        
        style.map("Treeview.Heading", background=[("active", R_COLOR_TABLA_HEAD)])
        style.map("Treeview", background=[("selected", "#00d4aa")], foreground=[("selected", "black")])

    def _configurar_interfaz(self):
        # Header
        header = tk.Frame(self, bg=COLOR_FONDO)
        header.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            header, text="Gestión de Pagos",
            font=("Segoe UI", 24, "bold"),
            bg=COLOR_FONDO, fg="#00d4aa"
        ).pack(anchor="w")
        
        tk.Label(
            header, text="Control mensual de cuotas",
            font=("Segoe UI", 11), bg=COLOR_FONDO, fg="#A9B4C6"
        ).pack(anchor="w")

        # CONTENEDOR PRINCIPAL CON BORDE NEON
        borde_card = tk.Frame(self, bg=R_COLOR_BORDE_PANEL, padx=1, pady=1)
        borde_card.pack(fill="both", expand=True)

        card = tk.Frame(borde_card, bg=R_COLOR_PANEL)
        card.pack(fill="both", expand=True)

        # SECCION 1: GENERAR PAGOS
        frame_generar = tk.Frame(card, bg=R_COLOR_PANEL)
        frame_generar.pack(fill="x", padx=20, pady=(15, 10))
        
        tk.Label(frame_generar, text="GENERAR PAGOS MENSUALES", font=("Segoe UI", 9, "bold"), fg="#A9B4C6", bg=R_COLOR_PANEL).pack(anchor="w", pady=(0, 5))
        
        cont_cols_gen = tk.Frame(frame_generar, bg=R_COLOR_PANEL)
        cont_cols_gen.pack(fill="x")
        
        # Combos simulados con estilo simple (Combobox nativo es difícil de estilizar full, lo mantenemos limpio)
        self.combo_mes = ttk.Combobox(cont_cols_gen, values=["01 - Enero", "02 - Febrero", "03 - Marzo", "04 - Abril", "05 - Mayo", "06 - Junio", "07 - Julio", "08 - Agosto", "09 - Septiembre", "10 - Octubre", "11 - Noviembre", "12 - Diciembre"], state="readonly", width=15, font=("Segoe UI", 10))
        self.combo_mes.pack(side="left", padx=(0, 10))
        
        self.combo_anio = ttk.Combobox(cont_cols_gen, values=[str(a) for a in range(2023, 2032)], state="readonly", width=8, font=("Segoe UI", 10))
        self.combo_anio.pack(side="left", padx=(0, 15))
        
        # Init date
        hoy = datetime.now()
        self.combo_mes.current(hoy.month - 1)
        self.combo_anio.set(str(hoy.year))
        
        self._crear_boton_refinado(cont_cols_gen, "GENERAR", self.generar_pagos_mes, R_COLOR_BTN_GENERAR).pack(side="left")

        # SECCION 2: FILTROS
        frame_filtros = tk.Frame(card, bg=R_COLOR_PANEL)
        frame_filtros.pack(fill="x", padx=20, pady=(10, 10))
        
        tk.Label(frame_filtros, text="FILTROS", font=("Segoe UI", 9, "bold"), fg="#A9B4C6", bg=R_COLOR_PANEL).pack(anchor="w", pady=(0, 5))
        
        cont_cols_filt = tk.Frame(frame_filtros, bg=R_COLOR_PANEL)
        cont_cols_filt.pack(fill="x")
        
        self.combo_filtro_cliente = ttk.Combobox(cont_cols_filt, width=30, state="readonly", font=("Segoe UI", 10))
        self.combo_filtro_cliente.pack(side="left", padx=(0, 15))
        
        self._crear_boton_refinado(cont_cols_filt, "FILTRAR", self.filtrar_por_cliente, R_COLOR_BTN_FILTRAR).pack(side="left", padx=(0, 10))
        self._crear_boton_refinado(cont_cols_filt, "VER TODOS", self.cargar_pagos, R_COLOR_BTN_TODOS).pack(side="left", padx=(0, 10))
        self._crear_boton_refinado(cont_cols_filt, "PENDIENTES", self.mostrar_pendientes, R_COLOR_BTN_PENDIENTES).pack(side="left")

        # SECCION 3: ACCIONES TABLA
        frame_acciones = tk.Frame(card, bg=R_COLOR_PANEL)
        frame_acciones.pack(fill="x", padx=20, pady=(15, 5))
        
        self._crear_boton_refinado(frame_acciones, "MARCAR PAGADO", self.marcar_pagado, R_COLOR_BTN_PAGAR).pack(side="left", padx=(0, 15))
        self._crear_boton_refinado(frame_acciones, "ELIMINAR", self.eliminar_pago, R_COLOR_BTN_ELIMINAR).pack(side="left")

        # TABLA
        table_frame = tk.Frame(card, bg=R_COLOR_PANEL)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        scrollbar_y = tk.Scrollbar(table_frame)
        scrollbar_y.pack(side="right", fill="y")
        
        cols = ("ID", "Cliente", "Mes", "Estado", "Cuota", "F. Pago", "Método")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", yscrollcommand=scrollbar_y.set)
        scrollbar_y.config(command=self.tree.yview)
        
        for col in cols:
            self.tree.heading(col, text=col)
            width = 50 if col == "ID" else 100
            if col == "Cliente": width = 180
            self.tree.column(col, width=width)
            
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_pago)

    def _crear_boton_refinado(self, parent, text, cmd, bg_color):
        btn = tk.Button(
            parent, text=text, command=cmd,
            bg=bg_color, fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            activebackground="white",
            activeforeground=bg_color,
            cursor="hand2",
            padx=15, pady=4
        )
        def on_enter(e): btn['bg'] = self._lighten_color(bg_color)
        def on_leave(e): btn['bg'] = bg_color
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def _lighten_color(self, color):
        # Mapeo simple de hover
        hover_map = {
            R_COLOR_BTN_GENERAR: "#33e0c0",
            R_COLOR_BTN_FILTRAR: "#5dade2",
            R_COLOR_BTN_TODOS: "#b2babb",
            R_COLOR_BTN_PENDIENTES: "#f5b041",
            R_COLOR_BTN_PAGAR: "#58d68d",
            R_COLOR_BTN_ELIMINAR: "#ec7063"
        }
        return hover_map.get(color, color)

    # ---------------------------------------------------------
    #   LOGICA (Mantenida idéntica)
    # ---------------------------------------------------------
    def cargar_clientes(self):
        try:
            self.clientes_dict = {c.id_cliente: f"{c.nombre} {c.apellidos}" for c in self.cliente_controller.obtener_todos_clientes()}
            self.combo_filtro_cliente["values"] = [f"{k} - {v}" for k, v in self.clientes_dict.items()]
        except Exception: pass

    def generar_pagos_mes(self):
        try:
            mes = f"{self.combo_anio.get()}-{self.combo_mes.get().split(' ')[0]}"
            cnt = self.controller.generar_pagos_mensuales(mes)
            messagebox.showinfo("Generado", f"Se crearon {cnt} pagos."); self.cargar_pagos()
        except Exception as e: messagebox.showerror("Error", str(e))

    def cargar_pagos(self):
        self._llenar_tabla(self.controller.obtener_todos_pagos())

    def filtrar_por_cliente(self):
        if not self.combo_filtro_cliente.get(): return
        try:
            cid = int(self.combo_filtro_cliente.get().split(" ")[0])
            self._llenar_tabla(self.controller.obtener_pagos_por_cliente(cid))
        except: pass

    def mostrar_pendientes(self):
        self._llenar_tabla([p for p in self.controller.obtener_todos_pagos() if not p.pagado])

    def _llenar_tabla(self, pagos):
        for i in self.tree.get_children(): self.tree.delete(i)
        for p in pagos:
            val_estado = "PAGADO" if p.pagado else "PENDIENTE"
            self.tree.insert("", "end", values=(
                p.id_pago, self.clientes_dict.get(p.id_cliente, "Desconocido"),
                p.mes, val_estado,
                formatear_cuota(p.cuota), formatear_fecha(p.fecha_pago), p.metodo_pago or ""
            ))

    def seleccionar_pago(self, e):
        sel = self.tree.selection()
        if sel: self.id_pago_seleccionado = self.tree.item(sel[0])["values"][0]

    def marcar_pagado(self):
        if not self.id_pago_seleccionado: return
        pago = self.controller.obtener_pago(self.id_pago_seleccionado)
        if pago.pagado: return messagebox.showinfo("Info", "Ya está pagado.")
        
        def cb(met, fech, con):
            self.controller.marcar_pago_como_pagado(self.id_pago_seleccionado, fech, met, con)
            self.cargar_pagos()
            
        VentanaPago(self, {"id_pago": pago.id_pago, "cuota": pago.cuota}, cb)

    def eliminar_pago(self):
        if self.id_pago_seleccionado and messagebox.askyesno("Confirmar", "¿Eliminar?"):
            self.controller.eliminar_pago(self.id_pago_seleccionado)
            self.cargar_pagos(); self.id_pago_seleccionado = None

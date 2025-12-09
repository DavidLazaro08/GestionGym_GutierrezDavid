"""
Vista de Pagos (Rediseño Dark Neon)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controller.pago_controller import PagoController
from controller.cliente_controller import ClienteController
from util.helpers import formatear_fecha, formatear_cuota
from view.ventana_pago import VentanaPago
from resources.style.colores import *

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
        style.configure("Treeview", background="#161b22", foreground="white", fieldbackground="#161b22", borderwidth=0, font=("Segoe UI", 10), rowheight=30)
        style.configure("Treeview.Heading", background="#0d1117", foreground=COLOR_SECUNDARIO, relief="flat", font=("Segoe UI", 10, "bold"))
        style.map("Treeview.Heading", background=[("active", "#161b22")])
        style.map("Treeview", background=[("selected", COLOR_SECUNDARIO)], foreground=[("selected", "#000000")])

    def _configurar_interfaz(self):
        # Header
        header = tk.Frame(self, bg=COLOR_FONDO)
        header.pack(fill="x", pady=(0, 20))
        tk.Label(header, text="Gestión de Pagos", font=FUENTE_TITULO, bg=COLOR_FONDO, fg="white").pack(anchor="w")
        tk.Label(header, text="Control mensual de cuotas", font=FUENTE_SUBTITULO, bg=COLOR_FONDO, fg=COLOR_TEXTO_SECUNDARIO).pack(anchor="w")

        # Generar Pagos Card
        gen_card = tk.Frame(self, bg=COLOR_FONDO_CARD)
        gen_card.pack(fill="x", pady=(0, 20))
        
        tk.Label(gen_card, text="GENERAR PAGOS MENSUALES", font=("Segoe UI", 8, "bold"), fg=COLOR_SECUNDARIO, bg=COLOR_FONDO_CARD).pack(anchor="w", padx=20, pady=(15, 10))
        
        gen_frame = tk.Frame(gen_card, bg=COLOR_FONDO_CARD)
        gen_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.combo_mes = ttk.Combobox(gen_frame, values=["01 - Enero", "02 - Febrero", "03 - Marzo", "04 - Abril", "05 - Mayo", "06 - Junio", "07 - Julio", "08 - Agosto", "09 - Septiembre", "10 - Octubre", "11 - Noviembre", "12 - Diciembre"], state="readonly", width=15)
        self.combo_mes.pack(side="left", padx=(0, 10))
        self.combo_anio = ttk.Combobox(gen_frame, values=[str(a) for a in range(2023, 2032)], state="readonly", width=8)
        self.combo_anio.pack(side="left", padx=(0, 10))
        
        # Init date combos
        hoy = datetime.now()
        self.combo_mes.current(hoy.month - 1)
        self.combo_anio.set(str(hoy.year))
        
        self._crear_boton(gen_frame, "GENERAR", self.generar_pagos_mes, ESTILO_BOTON_EXITO).pack(side="left")

        # Filtros Card
        filt_card = tk.Frame(self, bg=COLOR_FONDO_CARD)
        filt_card.pack(fill="x", pady=(0, 20))
        
        tk.Label(filt_card, text="FILTROS", font=("Segoe UI", 8, "bold"), fg=COLOR_TEXTO_SECUNDARIO, bg=COLOR_FONDO_CARD).pack(anchor="w", padx=20, pady=(15, 10))
        
        filt_frame = tk.Frame(filt_card, bg=COLOR_FONDO_CARD)
        filt_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.combo_filtro_cliente = ttk.Combobox(filt_frame, width=30, state="readonly")
        self.combo_filtro_cliente.pack(side="left", padx=(0, 10))
        
        self._crear_boton(filt_frame, "FILTRAR", self.filtrar_por_cliente, ESTILO_BOTON_INFO).pack(side="left", padx=(0, 10))
        self._crear_boton(filt_frame, "MOSTRAR TODOS", self.cargar_pagos, ESTILO_BOTON_NEUTRAL).pack(side="left", padx=(0, 10))
        self._crear_boton(filt_frame, "SOLO PENDIENTES", self.mostrar_pendientes, ESTILO_BOTON_ADVERTENCIA).pack(side="left")

        # Tabla Card
        table_card = tk.Frame(self, bg=COLOR_FONDO_CARD)
        table_card.pack(fill="both", expand=True)
        
        # Acciones
        act_frame = tk.Frame(table_card, bg=COLOR_FONDO_CARD)
        act_frame.pack(fill="x", padx=20, pady=20)
        self._crear_boton(act_frame, "MARCAR PAGADO", self.marcar_pagado, ESTILO_BOTON_EXITO).pack(side="left", padx=(0, 10))
        self._crear_boton(act_frame, "ELIMINAR", self.eliminar_pago, ESTILO_BOTON_PELIGRO).pack(side="left", padx=(0, 10))
        
        # Tabla
        table_frame = tk.Frame(table_card, bg=COLOR_FONDO_CARD)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        scr_y = tk.Scrollbar(table_frame); scr_y.pack(side="right", fill="y")
        cols = ("ID", "Cliente", "Mes", "Estado", "Cuota", "F. Pago", "Método")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", yscrollcommand=scr_y.set)
        scr_y.config(command=self.tree.yview)
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=60 if col=="ID" else 120)
            
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_pago)

    def _crear_boton(self, parent, text, cmd, style):
        return tk.Button(parent, text=text, command=cmd, **style)

    # ---------------------------------------------------------
    #   LOGICA
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
            self.tree.insert("", "end", values=(
                p.id_pago, self.clientes_dict.get(p.id_cliente, "Desconocido"),
                p.mes, "PAGADO" if p.pagado else "PENDIENTE",
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

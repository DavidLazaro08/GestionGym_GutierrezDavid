"""
Vista de Pagos
Interfaz para gestionar pagos mensuales de los clientes.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

from controller.pago_controller import PagoController
from controller.cliente_controller import ClienteController
from util.helpers import formatear_fecha, formatear_cuota
from util.validaciones import validar_fecha
from view.ventana_pago import VentanaPago


class PagoView(tk.Frame):
    """Vista de gestión de pagos (Frame)."""

    def __init__(self, parent, main_window):
        super().__init__(parent, bg="#ecf0f1")
        self.main_window = main_window

        self.controller = PagoController()
        self.cliente_controller = ClienteController()

        self.clientes_dict = {}   # id_cliente → "Nombre Apellido"
        self.id_pago_seleccionado = None

        self.configurar_interfaz()
        self.cargar_clientes()
        self.cargar_pagos()

    # ---------------------------------------------------------
    #   INTERFAZ PRINCIPAL
    # ---------------------------------------------------------
    def configurar_interfaz(self):

        titulo = tk.Label(
            self,
            text="Gestión de Pagos",
            font=("Arial", 20, "bold"),
            fg="#f39c12",
            bg="#ecf0f1"
        )
        titulo.pack(pady=15)

        # ---------------------------------------------------------
        #   GENERAR PAGOS DEL MES
        # ---------------------------------------------------------
        frame_generar = tk.LabelFrame(self, text="Generar pagos del mes",
                                      padx=15, pady=10, bg="#ecf0f1")
        frame_generar.pack(padx=20, pady=10, fill="x")

        tk.Label(frame_generar, text="Mes:").grid(row=0, column=0, padx=5)
        self.combo_mes = ttk.Combobox(
            frame_generar,
            values=[
                "01 - Enero", "02 - Febrero", "03 - Marzo", "04 - Abril",
                "05 - Mayo", "06 - Junio", "07 - Julio", "08 - Agosto",
                "09 - Septiembre", "10 - Octubre", "11 - Noviembre", "12 - Diciembre"
            ],
            state="readonly", width=20
        )
        self.combo_mes.grid(row=0, column=1, padx=5)

        tk.Label(frame_generar, text="Año:").grid(row=0, column=2, padx=5)
        self.combo_anio = ttk.Combobox(
            frame_generar,
            values=[str(a) for a in range(2023, 2032)],
            state="readonly", width=10
        )
        self.combo_anio.grid(row=0, column=3, padx=5)

        # Selección automática mes/año actual
        hoy = datetime.now()
        self.combo_mes.current(hoy.month - 1)

        valores_anio = list(self.combo_anio["values"])
        if str(hoy.year) not in valores_anio:
            valores_anio.append(str(hoy.year))
            self.combo_anio["values"] = valores_anio

        self.combo_anio.set(str(hoy.year))

        tk.Button(
            frame_generar,
            text="Generar pagos",
            command=self.generar_pagos_mes,
            bg="#27ae60", fg="white", width=18
        ).grid(row=0, column=4, padx=10)

        # ---------------------------------------------------------
        #   FILTROS
        # ---------------------------------------------------------
        frame_filtros = tk.LabelFrame(self, text="Filtros", padx=15, pady=10, bg="#ecf0f1")
        frame_filtros.pack(padx=20, pady=10, fill="x")

        tk.Label(frame_filtros, text="Cliente:").grid(row=0, column=0, padx=5)
        self.combo_filtro_cliente = ttk.Combobox(frame_filtros, width=40, state="readonly")
        self.combo_filtro_cliente.grid(row=0, column=1, padx=5)

        tk.Button(
            frame_filtros,
            text="Filtrar",
            command=self.filtrar_por_cliente,
            bg="#3498db", fg="white", width=10
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            frame_filtros,
            text="Ver todos",
            command=self.cargar_pagos,
            bg="#95a5a6", fg="white", width=10
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            frame_filtros,
            text="Pendientes",
            command=self.mostrar_pendientes,
            bg="#e67e22", fg="white", width=12
        ).grid(row=0, column=4, padx=5)

        # ---------------------------------------------------------
        #   TABLA
        # ---------------------------------------------------------
        frame_tabla = tk.Frame(self, bg="#ecf0f1")
        frame_tabla.pack(padx=20, pady=10, fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")

        columnas = (
            "ID", "ClienteID", "ClienteNombre", "Mes", "Estado",
            "F. Generación", "F. Pago", "Cuota", "Método", "Concepto"
        )

        self.tree = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        for col in columnas:
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=60)
        self.tree.column("ClienteID", width=80)
        self.tree.column("ClienteNombre", width=200)
        self.tree.column("Mes", width=90)
        self.tree.column("Estado", width=100)
        self.tree.column("F. Generación", width=110)
        self.tree.column("F. Pago", width=110)
        self.tree.column("Cuota", width=90)
        self.tree.column("Método", width=120)
        self.tree.column("Concepto", width=200)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_pago)

        # ---------------------------------------------------------
        #   BOTONES DE ACCIÓN
        # ---------------------------------------------------------
        frame_acciones = tk.Frame(self, bg="#ecf0f1")
        frame_acciones.pack(pady=10)

        tk.Button(
            frame_acciones,
            text="Marcar como pagado",
            command=self.marcar_pagado,
            bg="#2ecc71", fg="white", width=18
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            frame_acciones,
            text="Eliminar",
            command=self.eliminar_pago,
            bg="#e74c3c", fg="white", width=18
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            frame_acciones,
            text="Limpiar selección",
            command=self.limpiar_seleccion,
            bg="#7f8c8d", fg="white", width=18
        ).grid(row=0, column=2, padx=10)

    # ---------------------------------------------------------
    #   CARGA DE CLIENTES
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    #   GENERAR PAGOS DEL MES
    # ---------------------------------------------------------
    def generar_pagos_mes(self):
        try:
            mes_num = self.combo_mes.get().split(" ")[0]
            anio = self.combo_anio.get()
            mes_formato = f"{anio}-{mes_num}"

            cantidad = self.controller.generar_pagos_mensuales(mes_formato)

            messagebox.showinfo(
                "Pagos generados",
                f"Se han creado {cantidad} pagos pendientes."
            )
            self.cargar_pagos()

        except Exception as e:
            messagebox.showerror("Error generando pagos", str(e))

    # ---------------------------------------------------------
    #   TABLA
    # ---------------------------------------------------------
    def cargar_pagos(self):
        try:
            self.tree.delete(*self.tree.get_children())
            pagos = self.controller.obtener_todos_pagos()

            for p in pagos:
                nombre = self.clientes_dict.get(p.id_cliente, "Desconocido")
                estado = "Pagado" if p.pagado else "Pendiente"

                self.tree.insert("", "end", values=(
                    p.id_pago,
                    p.id_cliente,
                    nombre,
                    p.mes,
                    estado,
                    formatear_fecha(p.fecha_generacion),
                    formatear_fecha(p.fecha_pago),
                    formatear_cuota(p.cuota),
                    p.metodo_pago or "",
                    p.concepto or ""
                ))

        except Exception as e:
            messagebox.showerror("Error cargando pagos", str(e))

    def mostrar_pendientes(self):
        try:
            self.tree.delete(*self.tree.get_children())
            pagos = self.controller.obtener_todos_pagos()

            for p in pagos:
                if not p.pagado:
                    nombre = self.clientes_dict.get(p.id_cliente, "Desconocido")

                    self.tree.insert("", "end", values=(
                        p.id_pago,
                        p.id_cliente,
                        nombre,
                        p.mes,
                        "Pendiente",
                        formatear_fecha(p.fecha_generacion),
                        "",
                        formatear_cuota(p.cuota),
                        "",
                        ""
                    ))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------
    #   FILTROS
    # ---------------------------------------------------------
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

                self.tree.insert("", "end", values=(
                    p.id_pago,
                    p.id_cliente,
                    nombre,
                    p.mes,
                    estado,
                    formatear_fecha(p.fecha_generacion),
                    formatear_fecha(p.fecha_pago),
                    formatear_cuota(p.cuota),
                    p.metodo_pago or "",
                    p.concepto or ""
                ))

        except Exception as e:
            messagebox.showerror("Error filtrando pagos", str(e))

    # ---------------------------------------------------------
    #   SELECCIÓN / ACCIONES
    # ---------------------------------------------------------
    def seleccionar_pago(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            valores = self.tree.item(seleccion[0])["values"]
            self.id_pago_seleccionado = valores[0]

    def limpiar_seleccion(self):
        self.id_pago_seleccionado = None
        self.tree.selection_remove(self.tree.selection())

    def marcar_pagado(self):
        if not self.id_pago_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un pago.")
            return

        try:
            pago_obj = self.controller.obtener_pago(self.id_pago_seleccionado)

            if pago_obj.pagado:
                messagebox.showinfo("Pago ya registrado", "Este pago ya está pagado.")
                return

            datos_pago = {
                "id_pago": pago_obj.id_pago,
                "cliente": self.clientes_dict.get(pago_obj.id_cliente, "Desconocido"),
                "mes": pago_obj.mes,
                "cuota": pago_obj.cuota
            }

            def callback_confirmacion(metodo, fecha, concepto):

                if not metodo:
                    messagebox.showerror("Error", "Debe seleccionar un método de pago.")
                    return

                if not validar_fecha(fecha):
                    messagebox.showerror("Fecha inválida", "Formato YYYY-MM-DD.")
                    return

                try:
                    self.controller.marcar_pago_como_pagado(
                        self.id_pago_seleccionado,
                        fecha,
                        metodo,
                        concepto
                    )
                    messagebox.showinfo("Éxito", "Pago marcado correctamente.")
                    self.cargar_pagos()

                except Exception as e:
                    messagebox.showerror("Error al registrar pago", str(e))

            # CORRECCIÓN IMPORTANTE:
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

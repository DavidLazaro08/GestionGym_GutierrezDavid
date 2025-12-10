import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from tkcalendar import DateEntry

from controller.reserva_controller import ReservaController
from controller.cliente_controller import ClienteController
from controller.aparato_controller import AparatoController

from util.helpers import calcular_hora_fin
from util.validaciones import validar_fecha, validar_hora

# === COLORES DARK/NEON ===
COLOR_FONDO = "#0e1217"
COLOR_PANEL = "#151C25"
COLOR_BORDE = "#00d4aa"
COLOR_INPUT_BG = "#0F1620"
COLOR_INPUT_FG = "#E4E8EC"
COLOR_BTN_TURQ = "#00d4aa"
COLOR_BTN_VERDE = "#2ecc71"
COLOR_BTN_NARANJA = "#f39c12"
COLOR_BTN_ROJO = "#e74c3c"
COLOR_BTN_MORADO = "#8b5cf6"

COLOR_TABLA_BG = "#10171E"
COLOR_TABLA_HEAD = "#1D2630"


class ReservaView(tk.Frame):

    def __init__(self, parent, main_window):
        super().__init__(parent, bg=COLOR_FONDO)
        self.main_window = main_window

        self.controller = ReservaController()
        self.cliente_controller = ClienteController()
        self.aparato_controller = AparatoController()

        self.id_reserva_seleccionada = None
        self.clientes_dict = {}
        self.aparatos_dict = {}

        self._configurar_estilos_treeview()
        self._configurar_interfaz()
        self.cargar_clientes()
        self.cargar_aparatos()
        self.cargar_reservas()

    # ---------------------------------------------------------
    #   ESTILOS DE TABLA
    # ---------------------------------------------------------
    # ---------------------------------------------------------
    #   ESTILOS DE TABLA
    # ---------------------------------------------------------
    def _configurar_estilos_treeview(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=COLOR_TABLA_BG,
            foreground="white",
            fieldbackground=COLOR_TABLA_BG,
            borderwidth=0,
            rowheight=25,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=COLOR_TABLA_HEAD,
            foreground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )

        style.map("Treeview", background=[("selected", "#00d4aa")],
                  foreground=[("selected", "black")])

        # --- ESTILO SCROLLBAR ---
        style.configure(
            "Vertical.TScrollbar",
            background=COLOR_PANEL,
            troughcolor="#0e1217",
            bordercolor=COLOR_PANEL,
            arrowcolor="#00d4aa",
            relief="flat"
        )
        style.configure(
            "Horizontal.TScrollbar",
            background=COLOR_PANEL,
            troughcolor="#0e1217",
            bordercolor=COLOR_PANEL,
            arrowcolor="#00d4aa",
            relief="flat"
        )
        style.map("Vertical.TScrollbar", background=[("active", "#00d4aa")])
        style.map("Horizontal.TScrollbar", background=[("active", "#00d4aa")])

    # ---------------------------------------------------------
    #   INTERFAZ PRINCIPAL
    # ---------------------------------------------------------
    def _configurar_interfaz(self):

        # HEADER
        header = tk.Frame(self, bg=COLOR_FONDO)
        header.pack(fill="x", pady=(0, 15))

        tk.Label(
            header, text="Gestión de Reservas",
            font=("Segoe UI", 24, "bold"),
            bg=COLOR_FONDO, fg="#00d4aa"
        ).pack(anchor="w")

        tk.Label(
            header, text="Planificación de aparatos y horarios",
            font=("Segoe UI", 11),
            bg=COLOR_FONDO, fg="#A9B4C6"
        ).pack(anchor="w")

        # CARD PRINCIPAL
        borde = tk.Frame(self, bg=COLOR_BORDE, padx=1, pady=1)
        borde.pack(fill="both", expand=True)

        card = tk.Frame(borde, bg=COLOR_PANEL)
        card.pack(fill="both", expand=True)

        # FORMULARIO
        form = tk.Frame(card, bg=COLOR_PANEL)
        form.pack(fill="x", padx=20, pady=20)

        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        # CLIENTE / APARATO / ESTADO
        self.combo_cliente = self._crear_combo(form, "Cliente", [], 0, 0)
        self.combo_aparato = self._crear_combo(form, "Aparato", [], 1, 0)
        self.combo_estado = self._crear_combo(form, "Estado",
                                              ["pendiente", "confirmada", "cancelada"],
                                              2, 0)

        # FECHA
        self.entry_fecha = self._crear_date_entry(form, "Fecha", 0, 2)

        # HORAS
        hora_frame = tk.Frame(form, bg=COLOR_PANEL)
        hora_frame.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        tk.Label(hora_frame, text="HORA INICIO", font=("Segoe UI", 8, "bold"),
                 fg="#A9B4C6", bg=COLOR_PANEL).grid(row=0, column=0, sticky="w")

        border_h = tk.Frame(hora_frame, bg=COLOR_BORDE, padx=1, pady=1)
        border_h.grid(row=1, column=0, sticky="w")

        self.entry_hora_inicio = tk.Entry(
            border_h, bg=COLOR_INPUT_BG, fg="white",
            font=("Segoe UI", 10),
            insertbackground="white",
            relief="flat", bd=4, width=8
        )
        self.entry_hora_inicio.pack()
        self.entry_hora_inicio.insert(0, "09:00")
        self.entry_hora_inicio.bind("<FocusOut>", self._actualizar_hora_fin)
        self.entry_hora_inicio.bind("<Return>", self._actualizar_hora_fin)

        # HORA FIN
        tk.Label(hora_frame, text="HORA FIN", font=("Segoe UI", 8, "bold"),
                 fg="#A9B4C6", bg=COLOR_PANEL).grid(row=0, column=1, sticky="w", padx=(20, 0))

        self.label_hora_fin = tk.Label(
            hora_frame, text="09:30",
            bg=COLOR_INPUT_BG, fg="#00d4aa",
            font=("Segoe UI", 10, "bold"),
            width=8, pady=4
        )
        self.label_hora_fin.grid(row=1, column=1, sticky="w", padx=(20, 0))

        # BOTONES CRUD
        btns = tk.Frame(card, bg=COLOR_PANEL)
        btns.pack(fill="x", padx=20, pady=(0, 15))

        self._crear_btn(btns, "NUEVA", self.limpiar_formulario, COLOR_BTN_TURQ).pack(side="left", padx=6)
        self._crear_btn(btns, "GUARDAR", self.guardar_reserva, COLOR_BTN_VERDE).pack(side="left", padx=6)
        self._crear_btn(btns, "MODIFICAR", self.modificar_reserva, COLOR_BTN_NARANJA).pack(side="left", padx=6)
        self._crear_btn(btns, "ELIMINAR", self.eliminar_reserva, COLOR_BTN_ROJO).pack(side="left", padx=6)
        self._crear_btn(btns, "DISPONIBILIDAD", self.abrir_informe_disponibilidad, COLOR_BTN_MORADO).pack(side="left", padx=6)

        # TABLA
        table_frame = tk.Frame(card, bg=COLOR_PANEL)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        cols = ("ID", "Cliente", "Aparato", "Fecha", "Inicio", "Fin", "Estado")

        self.tree = ttk.Treeview(
            table_frame, columns=cols, show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)

        for col in cols:
            self.tree.heading(col, text=col)
            # Anchos ampliados
            w = 140
            if col == "ID": w = 60
            if col in ("Cliente", "Aparato"):
                w = 220
            self.tree.column(col, width=w)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_reserva)

    # ---------------------------------------------------------
    #   CREAR COMBOS Y ENTRIES
    # ---------------------------------------------------------
    def _crear_combo(self, parent, label, values, row, col):
        frame = tk.Frame(parent, bg=COLOR_PANEL)
        frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")

        tk.Label(frame, text=label.upper(), font=("Segoe UI", 8, "bold"),
                 fg="#A9B4C6", bg=COLOR_PANEL).pack(anchor="w")

        combo = ttk.Combobox(frame, values=values, state="readonly",
                             font=("Segoe UI", 10))
        combo.pack(fill="x", ipady=2)
        return combo

    def _crear_date_entry(self, parent, label, row, col):
        frame = tk.Frame(parent, bg=COLOR_PANEL)
        frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")

        tk.Label(frame, text=label.upper(), font=("Segoe UI", 8, "bold"),
                 fg="#A9B4C6", bg=COLOR_PANEL).pack(anchor="w")

        entry = DateEntry(
            frame,
            width=30,
            background="#00d4aa",
            foreground="white",
            fieldbackground=COLOR_INPUT_BG,
            fieldforeground="white",
            borderwidth=0,
            date_pattern='yyyy-mm-dd',
            locale='es_ES'
        )
        entry.pack(fill="x", ipady=2)
        return entry

    def _crear_btn(self, parent, text, cmd, bg):
        btn = tk.Button(parent, text=text, command=cmd,
                        bg=bg, fg="white",
                        font=("Segoe UI", 9, "bold"),
                        relief="flat", cursor="hand2",
                        padx=12, pady=4)
        return btn

    # ---------------------------------------------------------
    #   CRUD Y CARGAS
    # ---------------------------------------------------------
    def cargar_clientes(self):
        clientes = self.cliente_controller.obtener_todos_clientes()
        valores = []
        for c in clientes:
            t = f"{c.id_cliente} - {c.nombre} {c.apellidos}"
            valores.append(t)
            self.clientes_dict[t] = c.id_cliente
        self.combo_cliente["values"] = valores

    def cargar_aparatos(self):
        aparatos = self.aparato_controller.obtener_aparatos_disponibles()
        valores = []
        for a in aparatos:
            t = f"{a.id_aparato} - {a.nombre}"
            valores.append(t)
            self.aparatos_dict[t] = a.id_aparato
        self.combo_aparato["values"] = valores

    def cargar_reservas(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in self.controller.obtener_reservas_con_nombres():
            self.tree.insert("", "end", values=(
                r["id_reserva"],
                r["cliente"],
                r["aparato"],
                r["fecha"],
                r["inicio"],
                r["fin"],
                r["estado"]
            ))

    # ---------------------------------------------------------
    #   INFORME DE DISPONIBILIDAD (DARK + FUNCIONAL)
    # ---------------------------------------------------------
    def abrir_informe_disponibilidad(self):
        v = tk.Toplevel(self)
        v.title("Informe de Disponibilidad por Día")
        v.geometry("750x600")
        v.configure(bg=COLOR_FONDO)
        v.transient(self.winfo_toplevel())

        # TOP
        frame_top = tk.Frame(v, bg=COLOR_FONDO, padx=20, pady=20)
        frame_top.pack(fill="x")

        tk.Label(frame_top, text="Selección fecha:",
                 bg=COLOR_FONDO, fg="white",
                 font=("Segoe UI", 11, "bold")).pack(side="left")

        entry_fecha = DateEntry(
            frame_top,
            width=15,
            date_pattern='yyyy-mm-dd',
            locale='es_ES',
            background="#00d4aa",
            foreground="white",
            fieldbackground="#161b22",
            fieldforeground="white",
            borderwidth=0
        )
        entry_fecha.set_date(date.today())
        entry_fecha.pack(side="left", padx=10)

        btn = tk.Button(
            frame_top,
            text="Generar Informe",
            bg=COLOR_BTN_TURQ,
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=12, pady=4,
            cursor="hand2"
        )
        btn.pack(side="left", padx=10)

        # === FRAME DEL INFORME ===
        frame_text = tk.Frame(v, bg=COLOR_FONDO, padx=20, pady=20)
        frame_text.pack(fill="both", expand=True)

        # Evitar colapso
        frame_text.pack_propagate(False)
        frame_text.configure(height=450)

        txt = tk.Text(
            frame_text,
            font=("Courier New", 10),
            bg="#161b22",
            fg="#e6edf3",
            relief="flat",
            padx=10, pady=10,
            highlightthickness=1,
            highlightbackground="#30363d",
            insertbackground="white"
        )

        scroll = ttk.Scrollbar(frame_text, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=scroll.set)

        txt.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # --- LÓGICA DE GENERAR ---
        def generar():
            fecha = entry_fecha.get().strip()

            if not validar_fecha(fecha):
                messagebox.showerror("Error", "Formato inválido YYYY-MM-DD", parent=v)
                return

            try:
                informe = self.controller.generar_informe_disponibilidad(fecha)
            except Exception as e:
                messagebox.showerror("Error", f"Fallo al generar: {e}", parent=v)
                return

            txt.config(state="normal")
            txt.delete("1.0", tk.END)

            texto = f"INFORME DE DISPONIBILIDAD - {fecha}\n\n"

            for id_ap, datos in informe.items():
                texto += f"Aparato {id_ap} - {datos['nombre']}\n"
                texto += "-" * 50 + "\n"

                if not datos["reservas"]:
                    texto += "   Sin reservas → disponible todo el día\n\n"
                else:
                    for h1, h2, cli in datos["reservas"]:
                        texto += f"   {h1}-{h2} → {cli}\n"
                    texto += "\n"

            txt.insert("1.0", texto)
            txt.config(state="disabled")

        btn.config(command=generar)

        # generar al abrir
        v.after(50, generar)

    # ---------------------------------------------------------
    #   CRUD
    # ---------------------------------------------------------
    def limpiar_formulario(self):
        if self.combo_cliente["values"]:
            self.combo_cliente.current(0)
        if self.combo_aparato["values"]:
            self.combo_aparato.current(0)

        self.entry_fecha.set_date(date.today())
        self.entry_hora_inicio.delete(0, tk.END)
        self.entry_hora_inicio.insert(0, "09:00")
        self.label_hora_fin.config(text="09:30")

        self.combo_estado.current(0)
        self.id_reserva_seleccionada = None

    def guardar_reserva(self):
        if not self.combo_cliente.get() or not self.combo_aparato.get():
            messagebox.showwarning("Advertencia", "Seleccione cliente y aparato.")
            return

        id_cli = self.clientes_dict[self.combo_cliente.get()]
        id_apa = self.aparatos_dict[self.combo_aparato.get()]

        fecha = self.entry_fecha.get()
        inicio = self.entry_hora_inicio.get().strip()
        fin = self.label_hora_fin.cget("text")
        estado = self.combo_estado.get()

        ok, err = self.controller.validar_reserva(id_cli, id_apa, fecha, inicio, fin)
        if not ok:
            messagebox.showerror("Error", err)
            return

        if self.controller.crear_reserva(id_cli, id_apa, fecha, inicio, fin, estado):
            messagebox.showinfo("Éxito", "Reserva creada.")
            self.cargar_reservas()
            self.limpiar_formulario()
        else:
            messagebox.showerror("Error", "No disponible.")

    def modificar_reserva(self):
        if not self.id_reserva_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una reserva.")
            return

        id_cli = self.clientes_dict[self.combo_cliente.get()]
        id_apa = self.aparatos_dict[self.combo_aparato.get()]

        fecha = self.entry_fecha.get()
        inicio = self.entry_hora_inicio.get().strip()
        fin = self.label_hora_fin.cget("text")
        estado = self.combo_estado.get()

        ok, err = self.controller.validar_reserva(id_cli, id_apa, fecha, inicio, fin)
        if not ok:
            messagebox.showerror("Error", err)
            return

        if self.controller.actualizar_reserva(
                self.id_reserva_seleccionada,
                id_cliente=id_cli,
                id_aparato=id_apa,
                fecha_reserva=fecha,
                hora_inicio=inicio,
                hora_fin=fin,
                estado=estado):

            messagebox.showinfo("Éxito", "Modificada.")
            self.cargar_reservas()
            self.limpiar_formulario()
        else:
            messagebox.showerror("Error", "No se pudo modificar.")

    def eliminar_reserva(self):
        if not self.id_reserva_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione reserva.")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar reserva?"):
            self.controller.eliminar_reserva(self.id_reserva_seleccionada)
            self.cargar_reservas()
            self.id_reserva_seleccionada = None

    # ---------------------------------------------------------
    #   UTILIDADES
    # ---------------------------------------------------------
    def seleccionar_reserva(self, e):
        sel = self.tree.selection()
        if not sel:
            return
        self.id_reserva_seleccionada = self.tree.item(sel[0])["values"][0]

    def _actualizar_hora_fin(self, e=None):
        h = self.entry_hora_inicio.get().strip()
        self.label_hora_fin.config(text=calcular_hora_fin(h) or "--:--")

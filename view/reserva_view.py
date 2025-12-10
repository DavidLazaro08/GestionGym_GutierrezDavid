"""
Vista de Reservas (Rediseño Matrix/Neon)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from tkcalendar import DateEntry
from controller.reserva_controller import ReservaController
from controller.cliente_controller import ClienteController
from controller.aparato_controller import AparatoController
from util.helpers import calcular_hora_fin
from util.validaciones import validar_fecha, validar_hora
from resources.style.colores import *

# --- ESTILOS MATRIX / NEON REFINADOS ---
R_COLOR_PANEL = "#151C25"
R_COLOR_BORDE_PANEL = "#00d4aa"  # Turquesa
R_COLOR_INPUT_BG = "#0F1620"
R_COLOR_INPUT_TEXT = "#E4E8EC"
R_COLOR_BTN_NUEVA = "#00d4aa"    # Turquesa
R_COLOR_BTN_GUARDAR = "#2ecc71"  # Verde
R_COLOR_BTN_MODIFICAR = "#f39c12" # Naranja
R_COLOR_BTN_ELIMINAR = "#e74c3c" # Rojo
R_COLOR_BTN_DISPO = "#8b5cf6"    # Morado
R_COLOR_TABLA_BG = "#10171E"
R_COLOR_TABLA_HEAD = "#1D2630"

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
            header, text="Gestión de Reservas",
            font=("Segoe UI", 24, "bold"),
            bg=COLOR_FONDO, fg="#00d4aa"
        ).pack(anchor="w")
        
        tk.Label(
            header, text="Planificación de aparatos y horarios",
            font=("Segoe UI", 11), bg=COLOR_FONDO, fg="#A9B4C6"
        ).pack(anchor="w")

        # CONTENEDOR PRINCIPAL CON BORDE NEON
        borde_card = tk.Frame(self, bg=R_COLOR_BORDE_PANEL, padx=1, pady=1)
        borde_card.pack(fill="both", expand=True)

        card = tk.Frame(borde_card, bg=R_COLOR_PANEL)
        card.pack(fill="both", expand=True)

        # Formulario
        form = tk.Frame(card, bg=R_COLOR_PANEL)
        form.pack(fill="x", padx=20, pady=20)
        
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        # Columna 1
        self.combo_cliente = self._crear_combo_moderno(form, "Cliente", [], 0, 0)
        self.combo_aparato = self._crear_combo_moderno(form, "Aparato", [], 1, 0)
        self.combo_estado = self._crear_combo_moderno(form, "Estado", ["pendiente", "confirmada", "cancelada"], 2, 0)
        
        # Columna 2 - DateEntry custom wrapper
        # En la Columna 2 pondremos: Fecha y Horas
        
        self.entry_fecha = self._crear_date_entry(form, "Fecha", 0, 2)
        
        # Hora Container (Alineado con los combos)
        hora_frame = tk.Frame(form, bg=R_COLOR_PANEL)
        hora_frame.grid(row=1, column=2, padx=10, pady=5, sticky="ew")
        
        # Hora Inicio
        tk.Label(hora_frame, text="HORA INICIO", font=("Segoe UI", 8, "bold"), fg="#A9B4C6", bg=R_COLOR_PANEL).grid(row=0, column=0, sticky="w")
        
        border_h = tk.Frame(hora_frame, bg="#00d4aa", padx=1, pady=1)
        border_h.grid(row=1, column=0, sticky="w", pady=(2,0))
        
        self.entry_hora_inicio = tk.Entry(
            border_h, bg=R_COLOR_INPUT_BG, fg="white", 
            insertbackground="#00d4aa", font=("Segoe UI", 10), 
            relief="flat", bd=4, width=8
        )
        self.entry_hora_inicio.pack()
        self.entry_hora_inicio.insert(0, "09:00")
        self.entry_hora_inicio.bind("<FocusOut>", self._actualizar_hora_fin)
        self.entry_hora_inicio.bind("<Return>", self._actualizar_hora_fin)
        
        # Hora Fin
        tk.Label(hora_frame, text="HORA FIN", font=("Segoe UI", 8, "bold"), fg="#A9B4C6", bg=R_COLOR_PANEL).grid(row=0, column=1, sticky="w", padx=(20,0))
        
        self.label_hora_fin = tk.Label(
            hora_frame, text="09:30", bg=R_COLOR_INPUT_BG, fg="#00d4aa", 
            font=("Segoe UI", 10, "bold"), width=8, pady=4
        )
        self.label_hora_fin.grid(row=1, column=1, sticky="w", padx=(20,0), pady=(2,0))

        # Botones
        btns = tk.Frame(card, bg=R_COLOR_PANEL)
        btns.pack(fill="x", padx=20, pady=(0, 15))
        
        self._crear_boton_refinado(btns, "NUEVA", self.nueva_reserva, R_COLOR_BTN_NUEVA).pack(side="left", padx=(0, 10))
        self._crear_boton_refinado(btns, "GUARDAR", self.guardar_reserva, R_COLOR_BTN_GUARDAR).pack(side="left", padx=(0, 10))
        self._crear_boton_refinado(btns, "MODIFICAR", self.modificar_reserva, R_COLOR_BTN_MODIFICAR).pack(side="left", padx=(0, 10))
        self._crear_boton_refinado(btns, "ELIMINAR", self.eliminar_reserva, R_COLOR_BTN_ELIMINAR).pack(side="left", padx=(0, 10))
        self._crear_boton_refinado(btns, "DISPONIBILIDAD", self.abrir_informe_disponibilidad, R_COLOR_BTN_DISPO).pack(side="left")

        # Tabla
        table_frame = tk.Frame(card, bg=R_COLOR_PANEL)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        scrollbar_y = tk.Scrollbar(table_frame); scrollbar_y.pack(side="right", fill="y")
        
        cols = ("ID", "Cliente", "Aparato", "Fecha", "Inicio", "Fin", "Estado")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", yscrollcommand=scrollbar_y.set)
        scrollbar_y.config(command=self.tree.yview)
        
        for col in cols:
            self.tree.heading(col, text=col)
            width = 50 if col=="ID" else 100
            if col == "Cliente" or col == "Aparato": width = 150
            self.tree.column(col, width=width)
        
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_reserva)

    def _crear_combo_moderno(self, parent, label, values, row, col):
        frame = tk.Frame(parent, bg=R_COLOR_PANEL)
        frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
        
        tk.Label(frame, text=label.upper(), font=("Segoe UI", 8, "bold"), fg="#A9B4C6", bg=R_COLOR_PANEL).pack(anchor="w", pady=(0, 2))
        
        combo = ttk.Combobox(frame, values=values, state="readonly", font=("Segoe UI", 10))
        combo.pack(fill="x", ipady=2) # ipady reducido para compacidad
        if values: combo.current(0)
        return combo

    def _crear_date_entry(self, parent, label, row, col):
        frame = tk.Frame(parent, bg=R_COLOR_PANEL)
        frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
        
        tk.Label(frame, text=label.upper(), font=("Segoe UI", 8, "bold"), fg="#A9B4C6", bg=R_COLOR_PANEL).pack(anchor="w", pady=(0, 2))
        
        # DateEntry no es 100% estilisable en borde, pero ajustamos colores
        entry = DateEntry(
            frame, width=30, background="#00d4aa", foreground='white', 
            borderwidth=0, date_pattern='yyyy-mm-dd', locale='es_ES',
            fieldbackground=R_COLOR_INPUT_BG, fieldforeground="white"
        )
        entry.pack(fill="x", ipady=2)
        return entry

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
        hover_map = {
            R_COLOR_BTN_NUEVA: "#33e0c0",
            R_COLOR_BTN_GUARDAR: "#58d68d",
            R_COLOR_BTN_MODIFICAR: "#f5b041",
            R_COLOR_BTN_ELIMINAR: "#ec7063",
            R_COLOR_BTN_DISPO: "#a569bd"
        }
        return hover_map.get(color, color)

    # ---------------------------------------------------------
    #   LÓGICA (Mantenida idéntica)
    # ---------------------------------------------------------
    def cargar_clientes(self):
        clientes = self.cliente_controller.obtener_todos_clientes()
        valores = []
        for c in clientes:
            texto = f"{c.id_cliente} - {c.nombre} {c.apellidos}"
            valores.append(texto); self.clientes_dict[texto] = c.id_cliente
        self.combo_cliente["values"] = valores

    def cargar_aparatos(self):
        aparatos = self.aparato_controller.obtener_aparatos_disponibles()
        valores = []
        for a in aparatos:
            texto = f"{a.id_aparato} - {a.nombre}"
            valores.append(texto); self.aparatos_dict[texto] = a.id_aparato
        self.combo_aparato["values"] = valores

    def cargar_reservas(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for r in self.controller.obtener_reservas_con_nombres():
            self.tree.insert("", "end", values=(r["id_reserva"], r["cliente"], r["aparato"], r["fecha"], r["inicio"], r["fin"], r["estado"]))

    def nueva_reserva(self): self.limpiar_formulario()

    def guardar_reserva(self):
        if not self._validar_sel(): return
        id_cli = self.clientes_dict[self.combo_cliente.get()]
        id_apa = self.aparatos_dict[self.combo_aparato.get()]
        
        valido, err = self.controller.validar_reserva(id_cli, id_apa, self.entry_fecha.get(), self.entry_hora_inicio.get().strip(), self.label_hora_fin.cget("text"))
        if not valido: return messagebox.showerror("Error", err)
        
        if self.controller.crear_reserva(id_cli, id_apa, self.entry_fecha.get(), self.entry_hora_inicio.get().strip(), self.label_hora_fin.cget("text"), self.combo_estado.get()):
            messagebox.showinfo("Éxito", "Reserva creada.")
            self.cargar_reservas(); self.limpiar_formulario()
        else: messagebox.showerror("Error", "Aparato no disponible.")

    def modificar_reserva(self):
        if not self.id_reserva_seleccionada: return
        if not self._validar_sel(): return
        id_cli = self.clientes_dict[self.combo_cliente.get()]
        id_apa = self.aparatos_dict[self.combo_aparato.get()]
        if self.controller.actualizar_reserva(self.id_reserva_seleccionada, id_cliente=id_cli, id_aparato=id_apa, fecha_reserva=self.entry_fecha.get(), hora_inicio=self.entry_hora_inicio.get(), hora_fin=self.label_hora_fin.cget("text"), estado=self.combo_estado.get()):
            messagebox.showinfo("Éxito", "Modificada."); self.cargar_reservas()
        else: messagebox.showerror("Error", "Error al modificar.")

    def eliminar_reserva(self):
        if self.id_reserva_seleccionada and messagebox.askyesno("Confirmar", "¿Eliminar?"):
            self.controller.eliminar_reserva(self.id_reserva_seleccionada); self.cargar_reservas(); self.limpiar_formulario()

    def _validar_sel(self):
        if not self.combo_cliente.get() or not self.combo_aparato.get():
            messagebox.showwarning("Faltan datos", "Seleccione Cliente y Aparato."); return False
        return True

    def _actualizar_hora_fin(self, e=None):
        self.label_hora_fin.config(text=calcular_hora_fin(self.entry_hora_inicio.get().strip()) or "--:--")

    def seleccionar_reserva(self, e):
        sel = self.tree.selection()
        if not sel: return
        self.id_reserva_seleccionada = self.tree.item(sel[0])["values"][0]

    def limpiar_formulario(self):
        if self.combo_cliente["values"]: self.combo_cliente.current(0)
        self.entry_fecha.set_date(date.today()); self.entry_hora_inicio.delete(0, tk.END); self.entry_hora_inicio.insert(0, "09:00"); self.label_hora_fin.config(text="09:30"); self.id_reserva_seleccionada = None

    def abrir_informe_disponibilidad(self):
        v = tk.Toplevel(self); v.title("Informe"); v.configure(bg=COLOR_FONDO)
        tk.Label(v, text="Funcionalidad de informe (Logica existente)", bg=COLOR_FONDO, fg="white").pack(pady=20)

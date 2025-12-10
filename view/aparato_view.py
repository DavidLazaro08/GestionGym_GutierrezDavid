"""
Vista de Aparatos (Rediseño Matrix/Neon)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from controller.aparato_controller import AparatoController
from resources.style.colores import *

# --- ESTILOS MATRIX / NEON REFINADOS ---
R_COLOR_PANEL = "#151C25"
R_COLOR_BORDE_PANEL = "#00d4aa"  # Turquesa
R_COLOR_INPUT_BG = "#0F1620"
R_COLOR_INPUT_TEXT = "#E4E8EC"
R_COLOR_BTN_NUEVO = "#00d4aa"    # Turquesa
R_COLOR_BTN_GUARDAR = "#2ecc71"  # Verde
R_COLOR_BTN_MODIFICAR = "#f39c12" # Naranja
R_COLOR_BTN_ELIMINAR = "#e74c3c" # Rojo
R_COLOR_TABLA_BG = "#10171E"
R_COLOR_TABLA_HEAD = "#1D2630"

class AparatoView(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent, bg=COLOR_FONDO)
        self.main_window = main_window
        self.controller = AparatoController()
        self.id_aparato_seleccionado = None
        
        self._configurar_estilos_treeview()
        self._configurar_interfaz()
        self._cargar_aparatos()

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
            header, text="Gestión de Aparatos",
            font=("Segoe UI", 24, "bold"),
            bg=COLOR_FONDO, fg="#00d4aa"
        ).pack(anchor="w")
        
        tk.Label(
            header, text="Control de inventario y estado de máquinas",
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
        
        # Inputs
        # Fila 0
        self.entry_nombre = self._crear_input_moderno(form, "Nombre del Aparato", 0, 0)
        self.combo_tipo = self._crear_combo_moderno(form, "Tipo", ["Cardio", "Fuerza", "Flexibilidad", "Funcional", "Otro"], 0, 1)
        
        # Fila 1
        self.combo_estado = self._crear_combo_moderno(form, "Estado", ["disponible", "en_uso", "mantenimiento"], 1, 0)
        
        # Descripción (Area de texto con borde)
        desc_container = tk.Frame(form, bg=R_COLOR_PANEL)
        desc_container.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)
        
        tk.Label(desc_container, text="DESCRIPCIÓN", font=("Segoe UI", 8, "bold"), fg="#A9B4C6", bg=R_COLOR_PANEL).pack(anchor="w", pady=(0, 2))
        
        border_desc = tk.Frame(desc_container, bg=R_COLOR_BORDE_PANEL, padx=1, pady=1)
        border_desc.pack(fill="x")
        
        self.text_descripcion = tk.Text(
            border_desc, height=3, bg=R_COLOR_INPUT_BG, fg="white", 
            bd=5, font=("Segoe UI", 10), relief="flat", insertbackground="#00d4aa"
        )
        self.text_descripcion.pack(fill="x")

        # Botones
        btns = tk.Frame(card, bg=R_COLOR_PANEL)
        btns.pack(fill="x", padx=20, pady=(0, 15))
        
        self._crear_boton_refinado(btns, "NUEVO", self.nuevo_aparato, R_COLOR_BTN_NUEVO).pack(side="left", padx=(0, 10))
        self._crear_boton_refinado(btns, "GUARDAR", self.guardar_aparato, R_COLOR_BTN_GUARDAR).pack(side="left", padx=(0, 10))
        self._crear_boton_refinado(btns, "MODIFICAR", self.modificar_aparato, R_COLOR_BTN_MODIFICAR).pack(side="left", padx=(0, 10))
        self._crear_boton_refinado(btns, "ELIMINAR", self.eliminar_aparato, R_COLOR_BTN_ELIMINAR).pack(side="left")

        # Tabla
        table_frame = tk.Frame(card, bg=R_COLOR_PANEL)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        scrollbar_y = tk.Scrollbar(table_frame); scrollbar_y.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Tipo", "Estado", "Descripción"), show="headings", yscrollcommand=scrollbar_y.set)
        scrollbar_y.config(command=self.tree.yview)
        
        for col in ("ID", "Nombre", "Tipo", "Estado", "Descripción"):
            self.tree.heading(col, text=col)
            width = 80 if col != "Descripción" else 200
            if col == "ID": width = 50
            self.tree.column(col, width=width)
            
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_aparato)

    def _crear_input_moderno(self, parent, label, row, col):
        frame = tk.Frame(parent, bg=R_COLOR_PANEL)
        frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
        
        tk.Label(frame, text=label.upper(), font=("Segoe UI", 8, "bold"), fg="#A9B4C6", bg=R_COLOR_PANEL).pack(anchor="w", pady=(0, 2))
        
        border = tk.Frame(frame, bg=R_COLOR_BORDE_PANEL, padx=1, pady=1)
        border.pack(fill="x")
        
        entry = tk.Entry(
            border, bg=R_COLOR_INPUT_BG, fg="white", 
            insertbackground="#00d4aa", font=("Segoe UI", 10), 
            relief="flat", bd=5
        )
        entry.pack(fill="x")
        return entry

    def _crear_combo_moderno(self, parent, label, values, row, col):
        frame = tk.Frame(parent, bg=R_COLOR_PANEL)
        frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
        
        tk.Label(frame, text=label.upper(), font=("Segoe UI", 8, "bold"), fg="#A9B4C6", bg=R_COLOR_PANEL).pack(anchor="w", pady=(0, 2))
        
        combo = ttk.Combobox(frame, values=values, state="readonly", font=("Segoe UI", 10))
        combo.pack(fill="x", ipady=2)
        if values: combo.current(0)
        return combo

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
            R_COLOR_BTN_NUEVO: "#33e0c0",
            R_COLOR_BTN_GUARDAR: "#58d68d",
            R_COLOR_BTN_MODIFICAR: "#f5b041",
            R_COLOR_BTN_ELIMINAR: "#ec7063"
        }
        return hover_map.get(color, color)

    # ---------------------------------------------------------
    #   LOGICA (Mantenida idéntica)
    # ---------------------------------------------------------
    def nuevo_aparato(self):
        self.limpiar_formulario()

    def guardar_aparato(self):
        nombre = self.entry_nombre.get().strip()
        if not nombre: return
        self.controller.crear_aparato(nombre, self.combo_tipo.get(), self.text_descripcion.get("1.0", tk.END).strip(), self.combo_estado.get())
        self.limpiar_formulario()
        self._cargar_aparatos()

    def modificar_aparato(self):
        if not self.id_aparato_seleccionado: return
        self.controller.actualizar_aparato(self.id_aparato_seleccionado, nombre=self.entry_nombre.get(), tipo=self.combo_tipo.get(), estado=self.combo_estado.get(), descripcion=self.text_descripcion.get("1.0", tk.END).strip())
        self._cargar_aparatos()

    def eliminar_aparato(self):
        if not self.id_aparato_seleccionado: return
        if messagebox.askyesno("Confirmar", "¿Eliminar?"):
            self.controller.eliminar_aparato(self.id_aparato_seleccionado)
            self.limpiar_formulario()
            self._cargar_aparatos()

    def _cargar_aparatos(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for a in self.controller.obtener_todos_aparatos():
            self.tree.insert("", "end", values=(a.id_aparato, a.nombre, a.tipo, a.estado, a.descripcion))

    def seleccionar_aparato(self, event):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0])["values"]
        self.id_aparato_seleccionado = vals[0]
        self.entry_nombre.delete(0, tk.END); self.entry_nombre.insert(0, vals[1])
        self.combo_tipo.set(vals[2])
        self.combo_estado.set(vals[3])
        self.text_descripcion.delete("1.0", tk.END); self.text_descripcion.insert("1.0", vals[4])

    def limpiar_formulario(self):
        self.id_aparato_seleccionado = None
        self.entry_nombre.delete(0, tk.END)
        self.combo_tipo.current(0)
        self.combo_estado.current(0)
        self.text_descripcion.delete("1.0", tk.END)

"""
Vista de Clientes
Interfaz para gestionar clientes
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from controller.cliente_controller import ClienteController
from util.helpers import formatear_fecha, obtener_fecha_actual
from util.validaciones import (
    validar_dni,
    validar_email,
    validar_telefono
)


class ClienteView:
    """Ventana de gestión de clientes."""

    # ---------------------------------------------------------
    #   CONSTRUCTOR DE LA VISTA
    # ---------------------------------------------------------
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestión de Clientes")
        self.ventana.geometry("900x600")

        self.controller = ClienteController()
        self.id_cliente_seleccionado = None

        self.configurar_interfaz()
        self.cargar_clientes()

    # ---------------------------------------------------------
    #   CONFIGURACIÓN DE INTERFAZ
    # ---------------------------------------------------------
    def configurar_interfaz(self):
        """Genera todos los elementos gráficos de la ventana."""

        titulo = tk.Label(
            self.ventana,
            text="Gestión de Clientes",
            font=("Arial", 18, "bold"),
            fg="#3498db"
        )
        titulo.pack(pady=20)

        # ---------- FORMULARIO ----------
        frame_form = tk.LabelFrame(self.ventana, text="Datos del Cliente", padx=20, pady=20)
        frame_form.pack(padx=20, pady=10, fill="x")

        tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nombre = tk.Entry(frame_form, width=30)
        self.entry_nombre.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(frame_form, text="Apellidos:").grid(row=0, column=2, sticky="w", pady=5)
        self.entry_apellidos = tk.Entry(frame_form, width=30)
        self.entry_apellidos.grid(row=0, column=3, pady=5, padx=10)

        tk.Label(frame_form, text="DNI:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_dni = tk.Entry(frame_form, width=30)
        self.entry_dni.grid(row=1, column=1, pady=5, padx=10)

        tk.Label(frame_form, text="Email:").grid(row=1, column=2, sticky="w", pady=5)
        self.entry_email = tk.Entry(frame_form, width=30)
        self.entry_email.grid(row=1, column=3, pady=5, padx=10)

        tk.Label(frame_form, text="Teléfono:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_telefono = tk.Entry(frame_form, width=30)
        self.entry_telefono.grid(row=2, column=1, pady=5, padx=10)

        tk.Label(frame_form, text="Estado:").grid(row=2, column=2, sticky="w", pady=5)
        self.combo_estado = ttk.Combobox(
            frame_form,
            values=["activo", "inactivo"],
            width=28,
            state="readonly"
        )
        self.combo_estado.grid(row=2, column=3, pady=5, padx=10)
        self.combo_estado.current(0)

        # ---------- BOTONES ----------
        frame_botones = tk.Frame(self.ventana)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Nuevo", command=self.nuevo_cliente,
                  bg="#2ecc71", fg="white", width=12).grid(row=0, column=0, padx=5)

        tk.Button(frame_botones, text="Guardar", command=self.guardar_cliente,
                  bg="#3498db", fg="white", width=12).grid(row=0, column=1, padx=5)

        tk.Button(frame_botones, text="Modificar", command=self.modificar_cliente,
                  bg="#f39c12", fg="white", width=12).grid(row=0, column=2, padx=5)

        tk.Button(frame_botones, text="Eliminar", command=self.eliminar_cliente,
                  bg="#e74c3c", fg="white", width=12).grid(row=0, column=3, padx=5)

        # ---------- BÚSQUEDA ----------
        frame_busqueda = tk.Frame(self.ventana)
        frame_busqueda.pack(pady=10)

        tk.Label(frame_busqueda, text="Buscar:").pack(side="left", padx=5)
        self.entry_buscar = tk.Entry(frame_busqueda, width=40)
        self.entry_buscar.pack(side="left", padx=5)

        tk.Button(
            frame_busqueda, text="Buscar", command=self.buscar_clientes,
            bg="#9b59b6", fg="white"
        ).pack(side="left", padx=5)

        tk.Button(
            frame_busqueda, text="Mostrar Todos", command=self.cargar_clientes,
            bg="#95a5a6", fg="white"
        ).pack(side="left", padx=5)

        # ---------- TABLA ----------
        frame_tabla = tk.Frame(self.ventana)
        frame_tabla.pack(padx=20, pady=10, fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            frame_tabla,
            columns=("ID", "Nombre", "Apellidos", "DNI", "Email", "Teléfono", "Fecha", "Estado"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        for col, txt in zip(
            ("ID", "Nombre", "Apellidos", "DNI", "Email", "Teléfono", "Fecha", "Estado"),
            ("ID", "Nombre", "Apellidos", "DNI", "Email", "Teléfono", "Fecha Registro", "Estado")
        ):
            self.tree.heading(col, text=txt)

        self.tree.column("ID", width=50)
        self.tree.column("Nombre", width=100)
        self.tree.column("Apellidos", width=120)
        self.tree.column("DNI", width=100)
        self.tree.column("Email", width=150)
        self.tree.column("Teléfono", width=100)
        self.tree.column("Fecha", width=100)
        self.tree.column("Estado", width=80)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

    # ---------------------------------------------------------
    #   CRUD – CLIENTES
    # ---------------------------------------------------------
    def nuevo_cliente(self):
        self.limpiar_formulario()
        self.id_cliente_seleccionado = None

    def guardar_cliente(self):
        nombre = self.entry_nombre.get().strip()
        apellidos = self.entry_apellidos.get().strip()
        dni = self.entry_dni.get().strip()
        email = self.entry_email.get().strip()
        telefono = self.entry_telefono.get().strip()

        # ---------------------------
        #   VALIDACIONES
        # ---------------------------
        if not nombre or not apellidos or not dni:
            messagebox.showwarning("Advertencia", "Nombre, apellidos y DNI son obligatorios.")
            return

        if not validar_dni(dni):
            messagebox.showerror("DNI incorrecto", "El DNI introducido no es válido.")
            return

        if email and not validar_email(email):
            messagebox.showerror("Email incorrecto", "El formato del email no es válido.")
            return

        if telefono and not validar_telefono(telefono):
            messagebox.showerror("Teléfono incorrecto", "Debe contener 9 dígitos válidos de España.")
            return

        fecha_alta = obtener_fecha_actual()

        id_cliente = self.controller.crear_cliente(
            nombre, apellidos, dni, email, telefono, fecha_alta
        )

        if id_cliente:
            messagebox.showinfo("Éxito", "Cliente guardado correctamente")
            self.limpiar_formulario()
            self.cargar_clientes()
        else:
            messagebox.showerror("Error", "No se pudo guardar el cliente")

    def modificar_cliente(self):
        if not self.id_cliente_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un cliente.")
            return

        nombre = self.entry_nombre.get().strip()
        apellidos = self.entry_apellidos.get().strip()
        dni = self.entry_dni.get().strip()
        email = self.entry_email.get().strip()
        telefono = self.entry_telefono.get().strip()
        estado = self.combo_estado.get()

        if not nombre or not apellidos or not dni:
            messagebox.showwarning("Advertencia", "Nombre, apellidos y DNI son obligatorios.")
            return

        if not validar_dni(dni):
            messagebox.showerror("DNI incorrecto", "El DNI introducido no es válido.")
            return

        if email and not validar_email(email):
            messagebox.showerror("Email incorrecto", "Formato inválido de email.")
            return

        if telefono and not validar_telefono(telefono):
            messagebox.showerror("Teléfono incorrecto", "Debe contener 9 dígitos válidos de España.")
            return

        resultado = self.controller.actualizar_cliente(
            self.id_cliente_seleccionado,
            nombre=nombre,
            apellidos=apellidos,
            dni=dni,
            email=email,
            telefono=telefono,
            estado=estado
        )

        if resultado:
            messagebox.showinfo("Éxito", "Cliente modificado correctamente")
            self.limpiar_formulario()
            self.cargar_clientes()
        else:
            messagebox.showerror("Error", "No se pudo modificar el cliente")

    def eliminar_cliente(self):
        if not self.id_cliente_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un cliente.")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar cliente?"):
            res = self.controller.eliminar_cliente(self.id_cliente_seleccionado)
            if res:
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                self.limpiar_formulario()
                self.cargar_clientes()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente.")

    # ---------------------------------------------------------
    #   TABLA Y BÚSQUEDA
    # ---------------------------------------------------------
    def cargar_clientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        clientes = self.controller.obtener_todos_clientes()

        for c in clientes:
            self.tree.insert("", "end", values=(
                c.id_cliente,
                c.nombre,
                c.apellidos,
                c.dni,
                c.email,
                c.telefono,
                formatear_fecha(c.fecha_alta),
                c.estado
            ))

    def buscar_clientes(self):
        criterio = self.entry_buscar.get()
        if not criterio:
            messagebox.showwarning("Advertencia", "Ingrese un criterio.")
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        clientes = self.controller.buscar_clientes(criterio)

        for c in clientes:
            self.tree.insert("", "end", values=(
                c.id_cliente,
                c.nombre,
                c.apellidos,
                c.dni,
                c.email,
                c.telefono,
                formatear_fecha(c.fecha_alta),
                c.estado
            ))

    def seleccionar_cliente(self, event):
        seleccion = self.tree.selection()
        if not seleccion:
            return

        valores = self.tree.item(seleccion[0])["values"]

        self.id_cliente_seleccionado = valores[0]

        self.entry_nombre.delete(0, "end")
        self.entry_nombre.insert(0, valores[1])

        self.entry_apellidos.delete(0, "end")
        self.entry_apellidos.insert(0, valores[2])

        self.entry_dni.delete(0, "end")
        self.entry_dni.insert(0, valores[3])

        self.entry_email.delete(0, "end")
        self.entry_email.insert(0, valores[4])

        self.entry_telefono.delete(0, "end")
        self.entry_telefono.insert(0, valores[5])

        self.combo_estado.set(valores[7])

    # ---------------------------------------------------------
    #   UTILIDADES
    # ---------------------------------------------------------
    def limpiar_formulario(self):
        self.entry_nombre.delete(0, "end")
        self.entry_apellidos.delete(0, "end")
        self.entry_dni.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.entry_telefono.delete(0, "end")
        self.combo_estado.current(0)
        self.id_cliente_seleccionado = None

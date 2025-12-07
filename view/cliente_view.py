"""
Vista de Clientes
Interfaz para gestionar clientes.
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


class ClienteView(tk.Frame):
    """Vista de gestión de clientes."""

    # ---------------------------------------------------------
    #   CONSTRUCTOR
    # ---------------------------------------------------------
    def __init__(self, parent, main_window):
        super().__init__(parent, bg="#ecf0f1")

        self.main_window = main_window
        self.controller = ClienteController()
        self.id_cliente_seleccionado = None

        self._configurar_interfaz()
        self._cargar_clientes()

    # ---------------------------------------------------------
    #   INTERFAZ
    # ---------------------------------------------------------
    def _configurar_interfaz(self):
        """Crea todos los elementos gráficos de la vista."""

        titulo = tk.Label(
            self,
            text="Gestión de Clientes",
            font=("Arial", 18, "bold"),
            fg="#3498db",
            bg="#ecf0f1"
        )
        titulo.pack(pady=20)

        # ---------- FORMULARIO ----------
        frame_form = tk.LabelFrame(self, text="Datos del Cliente",
                                   padx=20, pady=20, bg="#ecf0f1")
        frame_form.pack(padx=20, pady=10, fill="x")

        # Nombre
        tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="w")
        self.entry_nombre = tk.Entry(frame_form, width=30)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=5)

        # Apellidos
        tk.Label(frame_form, text="Apellidos:").grid(row=0, column=2, sticky="w")
        self.entry_apellidos = tk.Entry(frame_form, width=30)
        self.entry_apellidos.grid(row=0, column=3, padx=10, pady=5)

        # DNI
        tk.Label(frame_form, text="DNI:").grid(row=1, column=0, sticky="w")
        self.entry_dni = tk.Entry(frame_form, width=30)
        self.entry_dni.grid(row=1, column=1, padx=10, pady=5)

        # Email
        tk.Label(frame_form, text="Email:").grid(row=1, column=2, sticky="w")
        self.entry_email = tk.Entry(frame_form, width=30)
        self.entry_email.grid(row=1, column=3, padx=10, pady=5)

        # Teléfono
        tk.Label(frame_form, text="Teléfono:").grid(row=2, column=0, sticky="w")
        self.entry_telefono = tk.Entry(frame_form, width=30)
        self.entry_telefono.grid(row=2, column=1, padx=10, pady=5)

        # Estado
        tk.Label(frame_form, text="Estado:").grid(row=2, column=2, sticky="w")
        self.combo_estado = ttk.Combobox(
            frame_form,
            values=["activo", "inactivo"],
            width=28,
            state="readonly"
        )
        self.combo_estado.grid(row=2, column=3, padx=10, pady=5)
        self.combo_estado.current(0)

        # ---------- BOTONES ----------
        frame_botones = tk.Frame(self, bg="#ecf0f1")
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Nuevo",
                  command=self._nuevo_cliente,
                  bg="#2ecc71", fg="white", width=12).grid(row=0, column=0, padx=5)

        tk.Button(frame_botones, text="Guardar",
                  command=self._guardar_cliente,
                  bg="#3498db", fg="white", width=12).grid(row=0, column=1, padx=5)

        tk.Button(frame_botones, text="Modificar",
                  command=self._modificar_cliente,
                  bg="#f39c12", fg="white", width=12).grid(row=0, column=2, padx=5)

        tk.Button(frame_botones, text="Eliminar",
                  command=self._eliminar_cliente,
                  bg="#e74c3c", fg="white", width=12).grid(row=0, column=3, padx=5)

        # ---------- BÚSQUEDA ----------
        frame_busqueda = tk.Frame(self, bg="#ecf0f1")
        frame_busqueda.pack(pady=10)

        tk.Label(frame_busqueda, text="Buscar:", bg="#ecf0f1").pack(side="left", padx=5)
        self.entry_buscar = tk.Entry(frame_busqueda, width=40)
        self.entry_buscar.pack(side="left", padx=5)

        tk.Button(frame_busqueda, text="Buscar",
                  command=self._buscar_clientes,
                  bg="#9b59b6", fg="white").pack(side="left", padx=5)

        tk.Button(frame_busqueda, text="Mostrar Todos",
                  command=self._cargar_clientes,
                  bg="#95a5a6", fg="white").pack(side="left", padx=5)

        # ---------- TABLA ----------
        frame_tabla = tk.Frame(self, bg="#ecf0f1")
        frame_tabla.pack(padx=20, pady=10, fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")

        columnas = ("ID", "Nombre", "Apellidos", "DNI",
                    "Email", "Teléfono", "Fecha", "Estado")

        self.tree = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        # Encabezados
        titulos = {
            "ID": "ID",
            "Nombre": "Nombre",
            "Apellidos": "Apellidos",
            "DNI": "DNI",
            "Email": "Email",
            "Teléfono": "Teléfono",
            "Fecha": "Fecha Registro",
            "Estado": "Estado"
        }

        for col in columnas:
            self.tree.heading(col, text=titulos[col])
            self.tree.column(col, width=110 if col != "ID" else 50)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._seleccionar_cliente)

    # ---------------------------------------------------------
    #   VALIDACIÓN CENTRALIZADA
    # ---------------------------------------------------------
    def _validar_datos(self, nombre, apellidos, dni, email, telefono):
        """Valida los datos del formulario. Nivel intermedio."""

        if not nombre or not apellidos or not dni:
            messagebox.showwarning(
                "Campos obligatorios",
                "El nombre, los apellidos y el DNI son obligatorios."
            )
            return False

        if not validar_dni(dni):
            messagebox.showerror(
                "DNI incorrecto",
                "El DNI introducido no es válido."
            )
            return False

        if email and not validar_email(email):
            messagebox.showerror(
                "Email incorrecto",
                "Revise el formato del correo electrónico."
            )
            return False

        if telefono and not validar_telefono(telefono):
            messagebox.showerror(
                "Teléfono incorrecto",
                "El teléfono debe tener 9 dígitos válidos."
            )
            return False

        return True

    # ---------------------------------------------------------
    #   CRUD
    # ---------------------------------------------------------
    def _nuevo_cliente(self):
        self._limpiar_formulario()
        self.id_cliente_seleccionado = None

    def _guardar_cliente(self):
        nombre = self.entry_nombre.get().strip()
        apellidos = self.entry_apellidos.get().strip()
        dni = self.entry_dni.get().strip()
        email = self.entry_email.get().strip()
        telefono = self.entry_telefono.get().strip()

        # Validación previa en la vista (sin cambios)
        if not self._validar_datos(nombre, apellidos, dni, email, telefono):
            return

        fecha_alta = obtener_fecha_actual()

        try:
            id_cliente = self.controller.crear_cliente(
                nombre, apellidos, dni, email, telefono, fecha_alta
            )

            messagebox.showinfo("Éxito", "Cliente guardado correctamente.")
            self._limpiar_formulario()
            self._cargar_clientes()

        except Exception as e:
            # Cualquier error de la capa de controlador se captura aquí
            messagebox.showerror("Error", str(e))

    def _modificar_cliente(self):
        if not self.id_cliente_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un cliente.")
            return

        nombre = self.entry_nombre.get().strip()
        apellidos = self.entry_apellidos.get().strip()
        dni = self.entry_dni.get().strip()
        email = self.entry_email.get().strip()
        telefono = self.entry_telefono.get().strip()
        estado = self.combo_estado.get()

        if not self._validar_datos(nombre, apellidos, dni, email, telefono):
            return

        try:
            ok = self.controller.actualizar_cliente(
                self.id_cliente_seleccionado,
                nombre=nombre,
                apellidos=apellidos,
                dni=dni,
                email=email,
                telefono=telefono,
                estado=estado
            )

            if ok:
                messagebox.showinfo("Éxito", "Cliente modificado correctamente.")
                self._limpiar_formulario()
                self._cargar_clientes()
            else:
                messagebox.showerror("Error", "No se pudo modificar el cliente.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _eliminar_cliente(self):
        if not self.id_cliente_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un cliente.")
            return

        if not messagebox.askyesno("Confirmar", "¿Eliminar cliente?"):
            return

        try:
            ok = self.controller.eliminar_cliente(self.id_cliente_seleccionado)

            if ok:
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                self._limpiar_formulario()
                self._cargar_clientes()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------
    #   TABLA / FORMULARIO
    # ---------------------------------------------------------
    def _cargar_clientes(self):
        try:
            clientes = self.controller.obtener_todos_clientes()

            self.tree.delete(*self.tree.get_children())
            for c in clientes:
                self.tree.insert("", "end", values=(
                    c.id_cliente, c.nombre, c.apellidos,
                    c.dni, c.email, c.telefono,
                    formatear_fecha(c.fecha_alta), c.estado
                ))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _buscar_clientes(self):
        criterio = self.entry_buscar.get().strip()

        if not criterio:
            messagebox.showwarning("Advertencia", "Ingrese un criterio de búsqueda.")
            return

        try:
            clientes = self.controller.buscar_clientes(criterio)

            self.tree.delete(*self.tree.get_children())
            for c in clientes:
                self.tree.insert("", "end", values=(
                    c.id_cliente, c.nombre, c.apellidos,
                    c.dni, c.email, c.telefono,
                    formatear_fecha(c.fecha_alta), c.estado
                ))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _seleccionar_cliente(self, event):
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
    def _limpiar_formulario(self):
        self.entry_nombre.delete(0, "end")
        self.entry_apellidos.delete(0, "end")
        self.entry_dni.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.entry_telefono.delete(0, "end")
        self.combo_estado.current(0)
        self.id_cliente_seleccionado = None

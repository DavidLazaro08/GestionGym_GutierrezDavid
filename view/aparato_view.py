"""
Vista de Aparatos
Interfaz para gestionar aparatos del gimnasio.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from controller.aparato_controller import AparatoController


class AparatoView(tk.Frame):
    """Vista de gestión de aparatos (Frame)."""

    # ---------------------------------------------------------
    #   CONSTRUCTOR
    # ---------------------------------------------------------
    def __init__(self, parent, main_window):
        """Inicializa la vista de aparatos dentro del panel principal."""
        super().__init__(parent, bg="#ecf0f1")
        self.main_window = main_window

        self.controller = AparatoController()
        self.id_aparato_seleccionado = None

        self.configurar_interfaz()
        self.cargar_aparatos()

    # ---------------------------------------------------------
    #   INTERFAZ
    # ---------------------------------------------------------
    def configurar_interfaz(self):
        """Configura todos los elementos gráficos de la vista."""

        titulo = tk.Label(
            self,
            text="Gestión de Aparatos",
            font=("Arial", 18, "bold"),
            fg="#2ecc71",
            bg="#ecf0f1"
        )
        titulo.pack(pady=20)

        # -------- FORMULARIO --------
        frame_form = tk.LabelFrame(
            self,
            text="Datos del Aparato",
            padx=20,
            pady=20,
            bg="#ecf0f1"
        )
        frame_form.pack(padx=20, pady=10, fill="x")

        # NOMBRE
        tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nombre = tk.Entry(frame_form, width=40)
        self.entry_nombre.grid(row=0, column=1, pady=5, padx=10)

        # TIPO
        tk.Label(frame_form, text="Tipo:").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_tipo = ttk.Combobox(
            frame_form,
            values=["Cardio", "Fuerza", "Flexibilidad", "Funcional", "Otro"],
            width=37,
            state="readonly"
        )
        self.combo_tipo.grid(row=1, column=1, pady=5, padx=10)
        self.combo_tipo.current(0)

        # ESTADO
        tk.Label(frame_form, text="Estado:").grid(row=2, column=0, sticky="w", pady=5)
        self.combo_estado = ttk.Combobox(
            frame_form,
            values=["disponible", "en_uso", "mantenimiento"],
            width=37,
            state="readonly"
        )
        self.combo_estado.grid(row=2, column=1, pady=5, padx=10)
        self.combo_estado.current(0)

        # DESCRIPCIÓN
        tk.Label(frame_form, text="Descripción:").grid(row=3, column=0, sticky="w", pady=5)
        self.text_descripcion = tk.Text(frame_form, width=40, height=3)
        self.text_descripcion.grid(row=3, column=1, pady=5, padx=10)

        # -------- BOTONES --------
        frame_botones = tk.Frame(self, bg="#ecf0f1")
        frame_botones.pack(pady=10)

        tk.Button(
            frame_botones,
            text="Nuevo",
            command=self.nuevo_aparato,
            bg="#2ecc71",
            fg="white",
            width=12
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            frame_botones,
            text="Guardar",
            command=self.guardar_aparato,
            bg="#3498db",
            fg="white",
            width=12
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            frame_botones,
            text="Modificar",
            command=self.modificar_aparato,
            bg="#f39c12",
            fg="white",
            width=12
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            frame_botones,
            text="Eliminar",
            command=self.eliminar_aparato,
            bg="#e74c3c",
            fg="white",
            width=12
        ).grid(row=0, column=3, padx=5)

        # -------- TABLA --------
        frame_tabla = tk.Frame(self, bg="#ecf0f1")
        frame_tabla.pack(padx=20, pady=10, fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            frame_tabla,
            columns=("ID", "Nombre", "Tipo", "Estado", "Descripción"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        # Cabeceras
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("Descripción", text="Descripción")

        # Tamaño columnas
        self.tree.column("ID", width=50)
        self.tree.column("Nombre", width=200)
        self.tree.column("Tipo", width=120)
        self.tree.column("Estado", width=120)
        self.tree.column("Descripción", width=250)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_aparato)

    # ---------------------------------------------------------
    #   ACCIONES
    # ---------------------------------------------------------
    def nuevo_aparato(self):
        """Limpia el formulario para crear un aparato nuevo."""
        self.limpiar_formulario()
        self.id_aparato_seleccionado = None

    def guardar_aparato(self):
        """Guarda un aparato nuevo en la base de datos."""
        nombre = self.entry_nombre.get().strip()
        tipo = self.combo_tipo.get()
        estado = self.combo_estado.get()
        descripcion = self.text_descripcion.get("1.0", tk.END).strip()

        if not nombre or not tipo:
            messagebox.showwarning(
                "Advertencia",
                "Nombre y tipo son obligatorios."
            )
            return

        nuevo_id = self.controller.crear_aparato(
            nombre,
            tipo,
            descripcion,
            estado
        )

        if nuevo_id:
            messagebox.showinfo("Éxito", "Aparato guardado correctamente.")
            self.limpiar_formulario()
            self.cargar_aparatos()
        else:
            messagebox.showerror("Error", "No se pudo guardar el aparato.")

    def modificar_aparato(self):
        """Modifica el aparato seleccionado."""
        if not self.id_aparato_seleccionado:
            messagebox.showwarning(
                "Advertencia",
                "Debe seleccionar un aparato."
            )
            return

        nombre = self.entry_nombre.get().strip()
        tipo = self.combo_tipo.get()
        estado = self.combo_estado.get()
        descripcion = self.text_descripcion.get("1.0", tk.END).strip()

        if not nombre or not tipo:
            messagebox.showwarning(
                "Advertencia",
                "Nombre y tipo son obligatorios."
            )
            return

        ok = self.controller.actualizar_aparato(
            self.id_aparato_seleccionado,
            nombre=nombre,
            tipo=tipo,
            estado=estado,
            descripcion=descripcion
        )

        if ok:
            messagebox.showinfo("Éxito", "Aparato modificado correctamente.")
            self.limpiar_formulario()
            self.cargar_aparatos()
        else:
            messagebox.showerror("Error", "No se pudo modificar el aparato.")

    def eliminar_aparato(self):
        """Elimina el aparato seleccionado."""
        if not self.id_aparato_seleccionado:
            messagebox.showwarning(
                "Advertencia",
                "Seleccione un aparato."
            )
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar este aparato?"):
            ok = self.controller.eliminar_aparato(self.id_aparato_seleccionado)

            if ok:
                messagebox.showinfo("Éxito", "Aparato eliminado.")
                self.limpiar_formulario()
                self.cargar_aparatos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el aparato.")

    # ---------------------------------------------------------
    #   TABLA Y FORMULARIO
    # ---------------------------------------------------------
    def cargar_aparatos(self):
        """Carga o recarga el listado de aparatos en la tabla."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        aparatos = self.controller.obtener_todos_aparatos()

        for aparato in aparatos:
            self.tree.insert(
                "",
                "end",
                values=(
                    aparato.id_aparato,
                    aparato.nombre,
                    aparato.tipo,
                    aparato.estado,
                    aparato.descripcion
                )
            )

    def seleccionar_aparato(self, event):
        """Carga los datos del aparato seleccionado en el formulario."""
        seleccion = self.tree.selection()
        if not seleccion:
            return

        fila = self.tree.item(seleccion[0])["values"]

        self.id_aparato_seleccionado = fila[0]

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, fila[1])

        self.combo_tipo.set(fila[2])
        self.combo_estado.set(fila[3])

        self.text_descripcion.delete("1.0", tk.END)
        self.text_descripcion.insert("1.0", fila[4])

    def limpiar_formulario(self):
        """Vacía todos los campos del formulario."""
        self.entry_nombre.delete(0, tk.END)
        self.combo_tipo.current(0)
        self.combo_estado.current(0)
        self.text_descripcion.delete("1.0", tk.END)
        self.id_aparato_seleccionado = None

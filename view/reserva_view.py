"""
Vista de Reservas
Interfaz para gestionar reservas
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from controller.reserva_controller import ReservaController
from controller.cliente_controller import ClienteController
from controller.aparato_controller import AparatoController
from util.validaciones import validar_fecha, validar_hora


class ReservaView(tk.Frame):
    """Vista de gestión de reservas (Frame)"""

    def __init__(self, parent, main_window):
        """
        Inicializa la vista de reservas
        
        Args:
            parent: Frame contenedor donde se dibuja
            main_window: Referencia a MainWindow
        """
        super().__init__(parent, bg="#ecf0f1")
        self.main_window = main_window

        self.controller = ReservaController()
        self.cliente_controller = ClienteController()
        self.aparato_controller = AparatoController()

        self.id_reserva_seleccionada = None
        self.clientes_dict = {}   # "id - nombre" → id_cliente
        self.aparatos_dict = {}   # "id - aparato" → id_aparato

        self.configurar_interfaz()
        self.cargar_clientes()
        self.cargar_aparatos()
        self.cargar_reservas()

    # ---------------------------------------------------------
    #   INTERFAZ
    # ---------------------------------------------------------
    def configurar_interfaz(self):
        titulo = tk.Label(self, text="Gestión de Reservas",
                          font=("Arial", 18, "bold"), fg="#e74c3c", bg="#ecf0f1")
        titulo.pack(pady=20)

        frame_form = tk.LabelFrame(self, text="Datos de la Reserva",
                                   padx=20, pady=20, bg="#ecf0f1")
        frame_form.pack(padx=20, pady=10, fill="x")

        tk.Label(frame_form, text="Cliente:").grid(row=0, column=0, sticky="w")
        self.combo_cliente = ttk.Combobox(frame_form, width=37, state="readonly")
        self.combo_cliente.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Aparato:").grid(row=1, column=0, sticky="w")
        self.combo_aparato = ttk.Combobox(frame_form, width=37, state="readonly")
        self.combo_aparato.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Fecha (YYYY-MM-DD):").grid(row=2, column=0, sticky="w")
        self.entry_fecha = tk.Entry(frame_form, width=40)
        self.entry_fecha.insert(0, str(date.today()))
        self.entry_fecha.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Hora Inicio:").grid(row=3, column=0, sticky="w")
        self.entry_hora_inicio = tk.Entry(frame_form, width=40)
        self.entry_hora_inicio.insert(0, "09:00")
        self.entry_hora_inicio.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Hora Fin:").grid(row=4, column=0, sticky="w")
        self.entry_hora_fin = tk.Entry(frame_form, width=40)
        self.entry_hora_fin.insert(0, "10:00")
        self.entry_hora_fin.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Estado:").grid(row=5, column=0, sticky="w")
        self.combo_estado = ttk.Combobox(frame_form,
                                         values=["pendiente", "confirmada", "cancelada"],
                                         width=37, state="readonly")
        self.combo_estado.grid(row=5, column=1, padx=10, pady=5)
        self.combo_estado.current(0)

        frame_botones = tk.Frame(self, bg="#ecf0f1")
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Nueva", bg="#2ecc71", fg="white",
                  width=12, command=self.nueva_reserva).grid(row=0, column=0, padx=5)

        tk.Button(frame_botones, text="Guardar", bg="#3498db", fg="white",
                  width=12, command=self.guardar_reserva).grid(row=0, column=1, padx=5)

        tk.Button(frame_botones, text="Modificar", bg="#f39c12", fg="white",
                  width=12, command=self.modificar_reserva).grid(row=0, column=2, padx=5)

        tk.Button(frame_botones, text="Eliminar", bg="#e74c3c", fg="white",
                  width=12, command=self.eliminar_reserva).grid(row=0, column=3, padx=5)

        # TABLA
        frame_tabla = tk.Frame(self, bg="#ecf0f1")
        frame_tabla.pack(padx=20, pady=10, fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            frame_tabla,
            columns=("ID", "Cliente", "Aparato", "Fecha", "Inicio", "Fin", "Estado"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        for col in ("ID", "Cliente", "Aparato", "Fecha", "Inicio", "Fin", "Estado"):
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=50)
        self.tree.column("Cliente", width=150)
        self.tree.column("Aparato", width=150)
        self.tree.column("Fecha", width=100)
        self.tree.column("Inicio", width=80)
        self.tree.column("Fin", width=80)
        self.tree.column("Estado", width=100)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_reserva)

    # ---------------------------------------------------------
    #   CARGAS
    # ---------------------------------------------------------
    def cargar_clientes(self):
        clientes = self.cliente_controller.obtener_todos_clientes()
        valores = []
        for c in clientes:
            texto = f"{c.id_cliente} - {c.nombre} {c.apellidos}"
            valores.append(texto)
            self.clientes_dict[texto] = c.id_cliente
        self.combo_cliente["values"] = valores

    def cargar_aparatos(self):
        aparatos = self.aparato_controller.obtener_aparatos_disponibles()
        valores = []
        for a in aparatos:
            texto = f"{a.id_aparato} - {a.nombre}"
            valores.append(texto)
            self.aparatos_dict[texto] = a.id_aparato
        self.combo_aparato["values"] = valores

    def cargar_reservas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for r in self.controller.obtener_todas_reservas():
            cliente = f"{r.id_cliente}"
            aparato = f"{r.id_aparato}"

            self.tree.insert(
                "",
                "end",
                values=(
                    r.id_reserva,
                    cliente,
                    aparato,
                    r.fecha_reserva,
                    r.hora_inicio,
                    r.hora_fin,
                    r.estado
                )
            )

    # ---------------------------------------------------------
    #   CRUD
    # ---------------------------------------------------------
    def nueva_reserva(self):
        self.limpiar_formulario()

    def guardar_reserva(self):
        cliente_txt = self.combo_cliente.get()
        aparato_txt = self.combo_aparato.get()

        if not cliente_txt or not aparato_txt:
            messagebox.showwarning("Advertencia", "Debe seleccionar cliente y aparato.")
            return

        id_cliente = self.clientes_dict[cliente_txt]
        id_aparato = self.aparatos_dict[aparato_txt]
        fecha = self.entry_fecha.get()
        inicio = self.entry_hora_inicio.get()
        fin = self.entry_hora_fin.get()
        estado = self.combo_estado.get()

        # ---- VALIDACIONES ----

        # Fecha válida
        if not validar_fecha(fecha):
            messagebox.showerror("Error", "La fecha debe tener formato YYYY-MM-DD.")
            return

        # Horas válidas
        if not validar_hora(inicio):
            messagebox.showerror("Error", "Hora de inicio inválida (HH:MM).")
            return

        if not validar_hora(fin):
            messagebox.showerror("Error", "Hora de fin inválida (HH:MM).")
            return

        # Orden de horas
        if inicio >= fin:
            messagebox.showerror(
                "Error",
                "La hora de fin debe ser posterior a la de inicio."
            )
            return

        # Crear reserva
        nuevo = self.controller.crear_reserva(
            id_cliente, id_aparato, fecha, inicio, fin, estado
        )

        if not nuevo:
            messagebox.showerror("Error", "El aparato no está disponible en ese horario.")
            return

        messagebox.showinfo("Éxito", "Reserva guardada correctamente.")
        self.cargar_reservas()
        self.limpiar_formulario()

    def modificar_reserva(self):
        if not self.id_reserva_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar una reserva.")
            return

        cliente_txt = self.combo_cliente.get()
        aparato_txt = self.combo_aparato.get()

        if not cliente_txt or not aparato_txt:
            messagebox.showwarning("Advertencia", "Debe seleccionar cliente y aparato.")
            return

        id_cliente = self.clientes_dict[cliente_txt]
        id_aparato = self.aparatos_dict[aparato_txt]
        fecha = self.entry_fecha.get()
        inicio = self.entry_hora_inicio.get()
        fin = self.entry_hora_fin.get()
        estado = self.combo_estado.get()

        # ---- VALIDACIONES ----

        if not validar_fecha(fecha):
            messagebox.showerror("Error", "La fecha debe tener formato YYYY-MM-DD.")
            return

        if not validar_hora(inicio):
            messagebox.showerror("Error", "Hora de inicio inválida (HH:MM).")
            return

        if not validar_hora(fin):
            messagebox.showerror("Error", "Hora de fin inválida (HH:MM).")
            return

        if inicio >= fin:
            messagebox.showerror("Error", "La hora de fin debe ser posterior a la de inicio.")
            return

        # ---- VERIFICAR DISPONIBILIDAD (si cambian aparato o horario) ----
        reserva_original = self.controller.obtener_reserva(self.id_reserva_seleccionada)

        cambios_aparato = (reserva_original.id_aparato != id_aparato)
        cambios_horas = (reserva_original.hora_inicio != inicio or reserva_original.hora_fin != fin)
        cambios_fecha = (reserva_original.fecha_reserva != fecha)

        if cambios_aparato or cambios_horas or cambios_fecha:
            disponible = self.controller.verificar_disponibilidad(
                id_aparato, fecha, inicio, fin
            )

            if not disponible:
                messagebox.showerror(
                    "Conflicto",
                    "El aparato no está disponible en ese horario."
                )
                return

        # ---- ACTUALIZAR RESERVA ----
        ok = self.controller.actualizar_reserva(
            self.id_reserva_seleccionada,
            id_cliente=id_cliente,
            id_aparato=id_aparato,
            fecha_reserva=fecha,
            hora_inicio=inicio,
            hora_fin=fin,
            estado=estado
        )

        if ok:
            messagebox.showinfo("Éxito", "Reserva modificada correctamente.")
            self.cargar_reservas()
            self.limpiar_formulario()
        else:
            messagebox.showerror("Error", "No se pudo modificar la reserva.")

    def eliminar_reserva(self):
        if not self.id_reserva_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una reserva.")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar reserva?"):
            self.controller.eliminar_reserva(self.id_reserva_seleccionada)
            self.cargar_reservas()
            self.id_reserva_seleccionada = None

    # ---------------------------------------------------------
    #   SELECCIÓN
    # ---------------------------------------------------------
    def seleccionar_reserva(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            fila = self.tree.item(seleccion[0])["values"]
            self.id_reserva_seleccionada = fila[0]

    # ---------------------------------------------------------
    #   UTILIDADES
    # ---------------------------------------------------------
    def limpiar_formulario(self):
        if self.combo_cliente["values"]:
            self.combo_cliente.current(0)
        if self.combo_aparato["values"]:
            self.combo_aparato.current(0)

        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, str(date.today()))

        self.entry_hora_inicio.delete(0, tk.END)
        self.entry_hora_inicio.insert(0, "09:00")

        self.entry_hora_fin.delete(0, tk.END)
        self.entry_hora_fin.insert(0, "10:00")

        self.combo_estado.current(0)
        self.id_reserva_seleccionada = None

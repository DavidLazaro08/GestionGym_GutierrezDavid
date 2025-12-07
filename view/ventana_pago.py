import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from util.helpers import formatear_cuota
from util.validaciones import validar_fecha


class VentanaPago(tk.Toplevel):

    def __init__(self, master, pago, callback_confirmacion):
        super().__init__(master)
        self.title("Registrar Pago")
        self.geometry("420x360")
        self.resizable(False, False)

        self.pago = pago
        self.callback = callback_confirmacion

        self.configurar_interfaz()

    def configurar_interfaz(self):

        tk.Label(self, text="Registrar Pago",
                 font=("Arial", 16, "bold"),
                 fg="#2ecc71").pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(pady=10, padx=20)

        # ---------------------------------------
        # DATOS INFORMATIVOS (solo lectura)
        # ---------------------------------------
        tk.Label(frame, text="Cliente:").grid(row=0, column=0, sticky="w")
        tk.Label(frame, text=self.pago["cliente"]).grid(row=0, column=1, sticky="w")

        tk.Label(frame, text="Mes:").grid(row=1, column=0, sticky="w")
        tk.Label(frame, text=self.pago["mes"]).grid(row=1, column=1, sticky="w")

        tk.Label(frame, text="Cuota:").grid(row=2, column=0, sticky="w")
        tk.Label(frame, text=formatear_cuota(self.pago["cuota"])).grid(row=2, column=1, sticky="w")

        # ---------------------------------------
        # CAMPOS EDITABLES
        # ---------------------------------------
        tk.Label(frame, text="Método de pago:").grid(row=3, column=0, sticky="w", pady=5)
        self.combo_metodo = ttk.Combobox(
            frame,
            values=["efectivo", "tarjeta", "transferencia", "bizum"],
            state="readonly",
            width=20
        )
        self.combo_metodo.current(0)
        self.combo_metodo.grid(row=3, column=1, pady=5)

        tk.Label(frame, text="Fecha de pago:").grid(row=4, column=0, sticky="w", pady=5)
        self.entry_fecha = tk.Entry(frame, width=22)
        self.entry_fecha.insert(0, str(date.today()))
        self.entry_fecha.grid(row=4, column=1, pady=5)

        tk.Label(frame, text="Concepto:").grid(row=5, column=0, sticky="nw", pady=5)
        self.text_concepto = tk.Text(frame, width=22, height=3)
        self.text_concepto.insert("1.0", "Cuota mensual")
        self.text_concepto.grid(row=5, column=1, pady=5)

        # ---------------------------------------
        # BOTONES
        # ---------------------------------------
        frame_btn = tk.Frame(self)
        frame_btn.pack(pady=15)

        tk.Button(
            frame_btn,
            text="Confirmar pago",
            bg="#2ecc71",
            fg="white",
            width=16,
            command=self.confirmar
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            frame_btn,
            text="Cancelar",
            bg="#e74c3c",
            fg="white",
            width=16,
            command=self.destroy
        ).grid(row=0, column=1, padx=10)

    # ---------------------------------------------------------
    # VALIDACIÓN Y CONFIRMACIÓN
    # ---------------------------------------------------------
    def confirmar(self):
        metodo = self.combo_metodo.get()
        fecha = self.entry_fecha.get()
        concepto = self.text_concepto.get("1.0", "end").strip()

        # VALIDACIÓN 1 — Método obligatorio
        if not metodo:
            messagebox.showerror("Error", "Debe seleccionar un método de pago.")
            return

        # VALIDACIÓN 2 — Fecha válida
        if not validar_fecha(fecha):
            messagebox.showerror(
                "Fecha inválida",
                "La fecha debe tener formato YYYY-MM-DD."
            )
            return

        # VALIDACIÓN 3 — Concepto no vacío (pero opcional si tú quieres)
        if concepto == "":
            concepto = "Cuota mensual"

        # Envío de datos a PagoView
        self.callback(metodo, fecha, concepto)

        # Cerrar ventana (PagoView mostrará mensajes)
        self.destroy()

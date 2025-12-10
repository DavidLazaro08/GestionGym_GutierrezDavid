# NO CONSEGUÍ IMPLEMENTAR ESTA CLASE DE ESTILOS PARA LAS ALERTAS


import tkinter as tk
from resources.style.colores import *

class CustomMessagebox(tk.Toplevel):
    def __init__(self, parent, title, message, tipo="info", botones=["Aceptar"]):
        super().__init__(parent)
        self.withdraw() # Ocultar mientras se configura
        
        self.title(title)
        self.message = message
        self.result = None
        self.tipo = tipo
        
        # Configuración de ventana
        self.overrideredirect(True) # Sin barra de título estándar
        self.configure(bg=COLOR_FONDO)
        self.attributes("-topmost", True)
        
        # Color de borde según tipo
        colors = {
            "info": COLOR_EXITO,
            "warning": COLOR_ADVERTENCIA,
            "error": COLOR_PELIGRO,
            "question": COLOR_INFO
        }
        accent_color = colors.get(tipo, COLOR_EXITO)
        
        # Frame Principal (Borde)
        main_border = tk.Frame(self, bg=accent_color, padx=2, pady=2)
        main_border.pack(fill="both", expand=True)
        
        # Contenido
        content_frame = tk.Frame(main_border, bg="#1a1f26", padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Título Personalizado
        title_frame = tk.Frame(content_frame, bg="#1a1f26")
        title_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            title_frame, 
            text=title.upper(), 
            font=("Segoe UI", 10, "bold"),
            fg=accent_color,
            bg="#1a1f26"
        ).pack(side="left")
        
        # Mensaje
        msg_label = tk.Label(
            content_frame,
            text=message,
            font=("Segoe UI", 11),
            fg="#e6edf3",
            bg="#1a1f26",
            wraplength=350,
            justify="left"
        )
        msg_label.pack(fill="x", pady=15)
        
        # Botones
        btn_frame = tk.Frame(content_frame, bg="#1a1f26")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        for btn_text in botones:
            if btn_text == "Sí" or btn_text == "Aceptar":
                bg_btn = accent_color
            else:
                bg_btn = "#374151" # Gris oscuro para cancelar/no
            
            b = tk.Button(
                btn_frame,
                text=btn_text,
                font=("Segoe UI", 9, "bold"),
                bg=bg_btn,
                fg="white",
                activebackground="white",
                activeforeground=bg_btn,
                relief="flat",
                cursor="hand2",
                width=10,
                command=lambda t=btn_text: self.on_btn_click(t)
            )
            b.pack(side="right", padx=5)

        # Centrar ventana
        self.update_idletasks()
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        
        # Calcular centro relativo al padre o pantalla
        if parent:
            x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (w // 2)
            y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (h // 2)
        else:
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            x = (sw - w) // 2
            y = (sh - h) // 2
            
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.deiconify()
        
        # Hacerla modal
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def on_btn_click(self, text):
        if text in ["Sí", "Aceptar"]:
            self.result = True
        else:
            self.result = False
        self.destroy()

# Helpers para reemplazar messagebox fácilmente
def showinfo(title, message, parent=None):
    CustomMessagebox(parent, title, message, "info", ["Aceptar"])

def showwarning(title, message, parent=None):
    CustomMessagebox(parent, title, message, "warning", ["Aceptar"])

def showerror(title, message, parent=None):
    CustomMessagebox(parent, title, message, "error", ["Aceptar"])

def askyesno(title, message, parent=None):
    mbox = CustomMessagebox(parent, title, message, "question", ["Sí", "No"])
    return mbox.result

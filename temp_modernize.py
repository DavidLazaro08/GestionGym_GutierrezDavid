"""
Script para modernizar cliente_view.py
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Leer el archivo original
with open(r"c:\Users\Usuario\Documents\Grado S Programación - SEGUNDO\Sistemas de gestión empresarial\00 PROYECTO EN PYTHON\Proyecto_GymForTheMoment\GestionGym_GutierrezDavid\view\cliente_view.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Encontrar la línea donde insertar el método de estilos
insert_index = None
for i, line in enumerate(lines):
    if "# ---------------------------------------------------------" in line and i > 30:
        if "INTERFAZ" in lines[i+1]:
            insert_index = i
            break

if insert_index:
    # Crear el nuevo método de estilos
    new_method = """    # ---------------------------------------------------------
    #   ESTILOS
    # ---------------------------------------------------------
    def _configurar_estilos(self):
        \"\"\"Configura estilos ttk modernos para la vista.\"\"\"
        style = ttk.Style()
        
        # Estilo para Treeview - Tema moderno con color cyan
        style.theme_use('clam')
        
        # Treeview general
        style.configure("Clientes.Treeview",
                       background="#ffffff",
                       foreground="#1f2937",
                       fieldbackground="#ffffff",
                       borderwidth=0,
                       font=("Segoe UI", 10))
        
        # Cabecera del Treeview
        style.configure("Clientes.Treeview.Heading",
                       background="#f3f4f6",
                       foreground="#1f2937",
                       borderwidth=1,
                       relief="flat",
                       font=("Segoe UI", 10, "bold"))
        
        # Hover en cabecera
        style.map("Clientes.Treeview.Heading",
                 background=[('active', '#e5e7eb')])
        
        # Selección con color cyan
        style.map("Clientes.Treeview",
                 background=[('selected', '#00d4aa')],
                 foreground=[('selected', '#ffffff')])

"""
    # Insertar el nuevo método
    lines.insert(insert_index, new_method)
    
    # Escribir el archivo modificado
    with open(r"c:\Users\Usuario\Documents\Grado S Programación - SEGUNDO\Sistemas de gestión empresarial\00 PROYECTO EN PYTHON\Proyecto_GymForTheMoment\GestionGym_GutierrezDavid\view\cliente_view.py", "w", encoding="utf-8") as f:
        f.writelines(lines)
    
    print("OK: Metodo _configurar_estilos insertado correctamente")
else:
    print("ERROR: No se encontro el lugar de insercion")

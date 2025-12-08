"""
Script para eliminar líneas duplicadas en cliente_view.py
"""

# Leer el archivo
with open(r"c:\Users\Usuario\Documents\Grado S Programación - SEGUNDO\Sistemas de gestión empresarial\00 PROYECTO EN PYTHON\Proyecto_GymForTheMoment\GestionGym_GutierrezDavid\view\cliente_view.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Eliminar líneas duplicadas (397-398)
if len(lines) > 398:
    if "scrollbar_y.config" in lines[396] and "scrollbar_y.config" in lines[394]:
        # Eliminar las líneas duplicadas 396 y 397
        del lines[396:398]
        print("OK: Lineas duplicadas eliminadas")
    else:
        print("INFO: No se encontraron duplicados exactos")

# Escribir el archivo
with open(r"c:\Users\Usuario\Documents\Grado S Programación - SEGUNDO\Sistemas de gestión empresarial\00 PROYECTO EN PYTHON\Proyecto_GymForTheMoment\GestionGym_GutierrezDavid\view\cliente_view.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

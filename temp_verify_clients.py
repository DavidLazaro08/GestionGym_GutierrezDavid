import sys
import os

# Ajustar path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.gestor_bd import GestorBD

def verificar_clientes():
    db = GestorBD()
    try:
        db.conectar()
        # Consulta directa ordenando por ID descendente
        filas = db.obtener_datos("SELECT id_cliente, nombre, apellidos, dni, fecha_alta FROM Cliente ORDER BY id_cliente DESC LIMIT 5")
        
        print("\n--- ÚLTIMOS 5 CLIENTES REGISTRADOS ---")
        for f in filas:
            print(f"ID: {f[0]} | {f[1]} {f[2]} | DNI: {f[3]} | Alta: {f[4]}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.desconectar()

if __name__ == "__main__":
    verificar_clientes()

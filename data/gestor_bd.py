# ---------------------------------------------------------
#   GESTOR DE BASE DE DATOS (SQLite)
#   Maneja la conexión y operaciones básicas del sistema.
# ---------------------------------------------------------

import sqlite3
import os


class GestorBD:
    """Gestor de base de datos para el proyecto GymForTheMoment."""

    # ---------------------------------------------------------
    #   CONSTRUCTOR
    # ---------------------------------------------------------
    def __init__(self, db_name="gym.db"):
        """Define la ruta del archivo de base de datos."""
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.conexion = None
        self.cursor = None

    # ---------------------------------------------------------
    #   CONEXIÓN / DESCONEXIÓN
    # ---------------------------------------------------------
    def conectar(self):
        """Abre la conexión y habilita claves foráneas."""
        try:
            self.conexion = sqlite3.connect(self.db_path)
            self.conexion.execute("PRAGMA foreign_keys = ON")
            self.cursor = self.conexion.cursor()
            return True
        except sqlite3.Error as e:
            print(f"[Error] No se pudo conectar: {e}")
            return False

    def desconectar(self):
        """Cierra la conexión si existe."""
        if self.conexion:
            self.conexion.close()

    # ---------------------------------------------------------
    #   QUERIES GENÉRICAS
    # ---------------------------------------------------------
    def ejecutar_query(self, query, parametros=None):
        """Ejecuta INSERT, UPDATE o DELETE."""
        try:
            if parametros:
                self.cursor.execute(query, parametros)
            else:
                self.cursor.execute(query)

            self.conexion.commit()
            return True
        except sqlite3.Error as e:
            print(f"[Error al ejecutar query] {e}")
            return False

    def obtener_datos(self, query, parametros=None):
        """Ejecuta un SELECT y devuelve los resultados."""
        try:
            if parametros:
                self.cursor.execute(query, parametros)
            else:
                self.cursor.execute(query)

            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[Error al obtener datos] {e}")
            return []

    # ---------------------------------------------------------
    #   CRUD AUXILIAR
    # ---------------------------------------------------------
    def insertar(self, tabla, datos):
        """Inserta un registro usando un diccionario {columna: valor}."""
        columnas = ', '.join(datos.keys())
        placeholders = ', '.join(['?' for _ in datos])
        query = f"INSERT INTO {tabla} ({columnas}) VALUES ({placeholders})"

        try:
            self.cursor.execute(query, tuple(datos.values()))
            self.conexion.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"[Error al insertar] {e}")
            return None

    def actualizar(self, tabla, datos, condicion):
        """Actualiza un registro según una condición."""
        set_clause = ', '.join([f"{k} = ?" for k in datos.keys()])
        query = f"UPDATE {tabla} SET {set_clause} WHERE {condicion}"

        try:
            self.cursor.execute(query, tuple(datos.values()))
            self.conexion.commit()
            return True
        except sqlite3.Error as e:
            print(f"[Error al actualizar] {e}")
            return False

    def eliminar(self, tabla, condicion):
        """Elimina registros según una condición."""
        query = f"DELETE FROM {tabla} WHERE {condicion}"
        try:
            self.cursor.execute(query)
            self.conexion.commit()
            return True
        except sqlite3.Error as e:
            print(f"[Error al eliminar] {e}")
            return False

    # ---------------------------------------------------------
    #   CREACIÓN DE TABLAS
    # ---------------------------------------------------------
    def crear_tablas(self):
        """Crea todas las tablas necesarias del sistema."""

        tablas = [

            # -------- CLIENTE --------
            """
            CREATE TABLE IF NOT EXISTS Cliente (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                dni TEXT UNIQUE NOT NULL,
                email TEXT,
                telefono TEXT,
                fecha_alta DATE NOT NULL,
                estado TEXT DEFAULT 'activo'
            );
            """,

            # -------- APARATO --------
            """
            CREATE TABLE IF NOT EXISTS Aparato (
                id_aparato INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                estado TEXT DEFAULT 'disponible',
                descripcion TEXT
            );
            """,

            # -------- RESERVA --------
            """
            CREATE TABLE IF NOT EXISTS Reserva (
                id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER NOT NULL,
                id_aparato INTEGER NOT NULL,
                fecha_reserva DATE NOT NULL,
                hora_inicio TIME NOT NULL,
                hora_fin TIME NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
                FOREIGN KEY (id_aparato) REFERENCES Aparato(id_aparato)
            );
            """,

            # -------- PAGO --------
            """
            CREATE TABLE IF NOT EXISTS Pago (
                id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER NOT NULL,
                mes TEXT NOT NULL,
                fecha_generacion DATE NOT NULL,
                pagado INTEGER DEFAULT 0,
                fecha_pago DATE,
                cuota REAL NOT NULL DEFAULT 30,
                metodo_pago TEXT,
                concepto TEXT,
                FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
            );
            """
        ]

        for tabla in tablas:
            self.ejecutar_query(tabla)

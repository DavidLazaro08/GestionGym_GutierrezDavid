# ---------------------------------------------------------
#   GESTOR DE BASE DE DATOS (SQLite)
#   Maneja la conexión y operaciones básicas del sistema.
# ---------------------------------------------------------

import sqlite3
import os
import hashlib

# Excepciones personalizadas del sistema
from excepciones import (
    ErrorBaseDatos,
    DBConexionError,
    DBConsultaError,
    DBInsercionError,
    DBActualizacionError,
    DBEliminacionError
)


class GestorBD:
    """Gestor de base de datos para el proyecto GymForTheMoment."""

    def __init__(self, db_name="gym.db"):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.conexion = None
        self.cursor = None

    # ---------------------------------------------------------
    #   CONEXIÓN / DESCONEXIÓN
    # ---------------------------------------------------------
    def conectar(self):
        try:
            self.conexion = sqlite3.connect(self.db_path)
            self.conexion.execute("PRAGMA foreign_keys = ON")
            self.cursor = self.conexion.cursor()
            return True

        except sqlite3.Error as e:
            raise DBConexionError(f"No se pudo conectar a la base de datos: {e}")

    def desconectar(self):
        if self.conexion:
            self.conexion.close()

    # ---------------------------------------------------------
    #   QUERIES GENÉRICAS
    # ---------------------------------------------------------
    def ejecutar_query(self, query, parametros=None):
        try:
            if parametros:
                self.cursor.execute(query, parametros)
            else:
                self.cursor.execute(query)

            self.conexion.commit()
            return True

        except sqlite3.Error as e:
            raise DBConsultaError(f"Error ejecutando query: {e}\nQUERY: {query}")

    def obtener_datos(self, query, parametros=None):
        try:
            if parametros:
                self.cursor.execute(query, parametros)
            else:
                self.cursor.execute(query)

            return self.cursor.fetchall()

        except sqlite3.Error as e:
            raise DBConsultaError(f"Error obteniendo datos: {e}\nQUERY: {query}")

    # ---------------------------------------------------------
    #   CRUD AUXILIAR
    # ---------------------------------------------------------
    def insertar(self, tabla, datos):
        columnas = ', '.join(datos.keys())
        placeholders = ', '.join(['?' for _ in datos])
        query = f"INSERT INTO {tabla} ({columnas}) VALUES ({placeholders})"

        try:
            self.cursor.execute(query, tuple(datos.values()))
            self.conexion.commit()
            return self.cursor.lastrowid

        except sqlite3.Error as e:
            raise DBInsercionError(f"Error al insertar en {tabla}: {e}")

    def actualizar(self, tabla, datos, condicion):
        set_clause = ', '.join([f"{k} = ?" for k in datos.keys()])
        query = f"UPDATE {tabla} SET {set_clause} WHERE {condicion}"

        try:
            self.cursor.execute(query, tuple(datos.values()))
            self.conexion.commit()
            return True

        except sqlite3.Error as e:
            raise DBActualizacionError(f"Error al actualizar en {tabla}: {e}")

    def eliminar(self, tabla, condicion):
        query = f"DELETE FROM {tabla} WHERE {condicion}"

        try:
            self.cursor.execute(query)
            self.conexion.commit()
            return True

        except sqlite3.Error as e:
            raise DBEliminacionError(f"Error al eliminar en {tabla}: {e}")

    # ---------------------------------------------------------
    #   CREACIÓN DE TABLAS
    # ---------------------------------------------------------
    def crear_tablas(self):
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
            """,

            # -------- USUARIO --------
            """
            CREATE TABLE IF NOT EXISTS Usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
            """
        ]

        for t in tablas:
            self.ejecutar_query(t)

        self.insertar_usuario_por_defecto()

    # ---------------------------------------------------------
    #   USUARIO POR DEFECTO
    # ---------------------------------------------------------
    def insertar_usuario_por_defecto(self):
        query = "SELECT COUNT(*) FROM Usuario WHERE usuario = 'admin'"
        resultado = self.obtener_datos(query)

        if resultado and resultado[0][0] == 0:
            password = "admin123"
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            datos = {
                "usuario": "admin",
                "password_hash": password_hash
            }

            self.insertar("Usuario", datos)
            print("[INFO] Usuario admin creado por defecto")

    # ---------------------------------------------------------
    #   INSERTO DATOS DE EJEMPLO A PARTIR DE SQL
    # ---------------------------------------------------------
    def ejecutar_sql_desde_archivo(self, ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                sql = f.read()
            self.cursor.executescript(sql)
            self.conexion.commit()
        except Exception as e:
            raise ErrorBaseDatos(f"Error ejecutando archivo SQL: {e}")

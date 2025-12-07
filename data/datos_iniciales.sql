------------------------------------------------------------
-- DATOS INICIALES DEL SISTEMA (Clientes + Aparatos)
-- Este archivo se ejecutará SOLO si la tabla Cliente está vacía.
------------------------------------------------------------

------------------------------------------------------------
-- CLIENTES
------------------------------------------------------------
INSERT INTO Cliente (nombre, apellidos, dni, email, telefono, fecha_alta, estado) VALUES
('David', 'Gutiérrez', '28641499J', 'empirio14@gmail.com', '600600600', DATE('now'), 'activo'),
('Patricia', 'Fernández', '30253966L', 'patfervil@gmail.com', '600600601', DATE('now'), 'activo'),
('Martín', 'Rivero', '12345678Z', 'martin.rivero@example.com', '600600602', DATE('now'), 'activo'),
('Alejandro', 'Campos', '98765432M', 'ale.campos@example.com', '600600603', DATE('now'), 'activo');

------------------------------------------------------------
-- APARATOS DEL GIMNASIO
------------------------------------------------------------
INSERT INTO Aparato (nombre, tipo, estado, descripcion) VALUES
('Cinta de correr 01', 'cardio', 'disponible', 'Cinta de uso general para carrera suave y entrenamientos moderados'),
('Elíptica 01', 'cardio', 'disponible', 'Máquina elíptica para trabajo cardiovascular sin impacto'),
('Bicicleta estática 01', 'cardio', 'disponible', 'Bicicleta indoor apta para sesiones de spinning'),
('Banco de pesas 01', 'fuerza', 'disponible', 'Banco de musculación básico para press y ejercicios con mancuernas'),
('Prensa de piernas 01', 'fuerza', 'disponible', 'Máquina de fuerza orientada al trabajo de tren inferior'),
('Máquina de remo 01', 'cardio', 'disponible', 'Rower profesional para entrenamiento completo del cuerpo');

-- =====================================================
-- SCRIPT DE DATOS DE PRUEBA - BRISA BACKEND
-- Sistema de Gestión Académica
-- Módulo: Retiros Tempranos
-- =====================================================
-- 
-- PROPÓSITO: Alimentar la base de datos con datos genéricos
--            para probar los endpoints de creación de retiros
--
-- NO INCLUYE: solicitudes_retiro, registros_salida, autorizaciones_retiro
--              (estos se crearán mediante los endpoints)
--
-- ORDEN DE INSERCIÓN: Respeta las dependencias de Foreign Keys
-- =====================================================

USE brisa_db;

-- Limpiar datos existentes (opcional - comentar si no se desea)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE profesores_cursos_materias;
TRUNCATE TABLE estudiantes_cursos;
TRUNCATE TABLE estudiantes_apoderados;
TRUNCATE TABLE motivos_retiro;
TRUNCATE TABLE materias;
TRUNCATE TABLE cursos;
TRUNCATE TABLE apoderados;
TRUNCATE TABLE estudiantes;
TRUNCATE TABLE personas;
SET FOREIGN_KEY_CHECKS = 1;


-- =====================================================

INSERT INTO apoderados (ci, nombres, apellidos, telefono, correo, direccion) VALUES
('5123456', 'José Antonio', 'García Quispe', '70123456', 'jose.garcia@email.com', 'Calle Los Pinos #100'),
('5234567', 'Rosa María', 'Mamani Condori', '71123456', 'rosa.mamani@email.com', 'Calle Los Pinos #100'),
('5345678', 'Miguel Ángel', 'López Vargas', '70234567', 'miguel.lopez@email.com', 'Av. del Maestro #200'),
('5456789', 'Carmen Elena', 'Flores Cruz', '71234567', 'carmen.flores@email.com', 'Av. del Maestro #200'),
('5567890', 'Fernando José', 'Morales Pérez', '70345678', 'fernando.morales@email.com', 'Zona Central #300'),
('5678901', 'Ricardo Andrés', 'Quispe Mamani', '70456789', 'ricardo.quispe@email.com', 'Calle Libertad #400'),
('5789012', 'Alberto Daniel', 'Fernández Torres', '70567890', 'alberto.fernandez@email.com', 'Av. Principal #500'),
('5890123', 'Sandra Beatriz', 'Rojas Morales', '71567890', 'sandra.rojas@email.com', 'Av. Principal #500');

-- =====================================================
-- 6. RELACIONES ESTUDIANTES-APODERADOS
--    (Con contactos principales marcados)
-- =====================================================

-- Estudiante 1: Pedro Luis García Mamani
INSERT INTO estudiantes_apoderados (id_estudiante, id_apoderado, parentesco, es_contacto_principal) VALUES
(1, 1, 'Padre', true),
(1, 2, 'Madre', false);

-- Estudiante 2: Sofía Andrea López Flores
INSERT INTO estudiantes_apoderados (id_estudiante, id_apoderado, parentesco, es_contacto_principal) VALUES
(2, 3, 'Padre', true),
(2, 4, 'Madre', false);

-- Estudiante 3: Diego Alejandro Morales Castro
INSERT INTO estudiantes_apoderados (id_estudiante, id_apoderado, parentesco, es_contacto_principal) VALUES
(3, 5, 'Padre', true);

-- Estudiante 4: Valentina María Quispe Gutiérrez
INSERT INTO estudiantes_apoderados (id_estudiante, id_apoderado, parentesco, es_contacto_principal) VALUES
(4, 6, 'Padre', true);

-- Estudiante 5: Mateo Sebastián Fernández Rojas
INSERT INTO estudiantes_apoderados (id_estudiante, id_apoderado, parentesco, es_contacto_principal) VALUES
(5, 7, 'Padre', false),
(5, 8, 'Madre', true);

-- Estudiante 6: Isabella Carolina Condori Pérez (apoderado compartido con estudiante 1)
INSERT INTO estudiantes_apoderados (id_estudiante, id_apoderado, parentesco, es_contacto_principal) VALUES
(6, 1, 'Tío', true);

-- Estudiante 7: Santiago Andrés Vargas Mamani (apoderado compartido)
INSERT INTO estudiantes_apoderados (id_estudiante, id_apoderado, parentesco, es_contacto_principal) VALUES
(7, 3, 'Abuelo', true);

-- Estudiante 8: Camila Sofía Silva González
INSERT INTO estudiantes_apoderados (id_estudiante, id_apoderado, parentesco, es_contacto_principal) VALUES
(8, 5, 'Padre', true);

-- Estudiante 9: Nicolás Gabriel Cruz Torrico
INSERT INTO estudiantes_apoderados (id_estudiante, id_apoderado, parentesco, es_contacto_principal) VALUES
(9, 6, 'Tutor Legal', true);

-- Estudiante 10: Emilia Victoria Mamani López
INSERT INTO estudiantes_apoderados (id_estudiante, id_apoderado, parentesco, es_contacto_principal) VALUES
(10, 7, 'Padre', true),
(10, 8, 'Madre', false);


-- =====================================================
-- 9. MOTIVOS DE RETIRO (Catálogo)
-- =====================================================

INSERT INTO motivos_retiro (nombre, descripcion, severidad, activo) VALUES
('Cita Médica', 'Estudiante tiene cita médica programada', 'leve', true),
('Emergencia Familiar', 'Situación familiar urgente que requiere la presencia del estudiante', 'grave', true),
('Enfermedad', 'Estudiante presenta síntomas de enfermedad', 'grave', true),
('Trámite Urgente', 'Apoderado necesita realizar trámite con el estudiante', 'leve', true),
('Otro', 'Otros motivos no especificados', 'leve', true);


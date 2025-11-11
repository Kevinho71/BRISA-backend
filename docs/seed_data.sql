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
-- 1. PERSONAS (Profesores y Administrativos)
-- =====================================================

INSERT INTO personas (ci, nombres, apellido_paterno, apellido_materno, direccion, telefono, correo, tipo_persona, is_active) VALUES
('7123456', 'Juan Carlos', 'Pérez', 'González', 'Av. América #123', '71234567', 'juan.perez@colegio.edu.bo', 'administrativo', true),
('8234567', 'María Elena', 'Rodríguez', 'López', 'Calle Ballivián #456', '72345678', 'maria.rodriguez@colegio.edu.bo', 'administrativo', true),
('9345678', 'Roberto', 'Martínez', 'Silva', 'Zona Sur #789', '73456789', 'roberto.martinez@colegio.edu.bo', 'profesor', true),
('6456789', 'Ana Patricia', 'Flores', 'Vargas', 'Av. 6 de Agosto #321', '74567890', 'ana.flores@colegio.edu.bo', 'profesor', true),
('7567890', 'Carlos Alberto', 'Sánchez', 'Morales', 'Calle Comercio #654', '75678901', 'carlos.sanchez@colegio.edu.bo', 'profesor', true),
('8678901', 'Laura Isabel', 'Torres', 'Gutiérrez', 'Zona Norte #987', '76789012', 'laura.torres@colegio.edu.bo', 'profesor', true),
('9789012', 'Diego Fernando', 'Ramírez', 'Castro', 'Av. Arce #147', '77890123', 'diego.ramirez@colegio.edu.bo', 'administrativo', true);

-- =====================================================
-- 2. ESTUDIANTES
-- =====================================================

INSERT INTO estudiantes (ci, nombres, apellido_paterno, apellido_materno, fecha_nacimiento, direccion, 
                         nombre_padre, apellido_paterno_padre, apellido_materno_padre, telefono_padre,
                         nombre_madre, apellido_paterno_madre, apellido_materno_madre, telefono_madre) VALUES
('12345678', 'Pedro Luis', 'García', 'Mamani', '2015-03-15', 'Calle Los Pinos #100', 
 'José Antonio', 'García', 'Quispe', '70123456',
 'Rosa María', 'Mamani', 'Condori', '71123456'),

('23456789', 'Sofía Andrea', 'López', 'Flores', '2014-07-22', 'Av. del Maestro #200',
 'Miguel Ángel', 'López', 'Vargas', '70234567',
 'Carmen Elena', 'Flores', 'Cruz', '71234567'),

('34567890', 'Diego Alejandro', 'Morales', 'Castro', '2013-11-08', 'Zona Central #300',
 'Fernando José', 'Morales', 'Pérez', '70345678',
 'Patricia Isabel', 'Castro', 'Luna', '71345678'),

('45678901', 'Valentina María', 'Quispe', 'Gutiérrez', '2016-01-30', 'Calle Libertad #400',
 'Ricardo Andrés', 'Quispe', 'Mamani', '70456789',
 'Lucía Victoria', 'Gutiérrez', 'Silva', '71456789'),

('56789012', 'Mateo Sebastián', 'Fernández', 'Rojas', '2015-05-12', 'Av. Principal #500',
 'Alberto Daniel', 'Fernández', 'Torres', '70567890',
 'Sandra Beatriz', 'Rojas', 'Morales', '71567890'),

('67890123', 'Isabella Carolina', 'Condori', 'Pérez', '2014-09-25', 'Calle Sucre #600',
 'Juan Pablo', 'Condori', 'Quispe', '70678901',
 'María José', 'Pérez', 'López', '71678901'),

('78901234', 'Santiago Andrés', 'Vargas', 'Mamani', '2013-12-18', 'Zona Este #700',
 'Carlos Eduardo', 'Vargas', 'Cruz', '70789012',
 'Ana Claudia', 'Mamani', 'Flores', '71789012'),

('89012345', 'Camila Sofía', 'Silva', 'González', '2016-04-05', 'Av. Circunvalación #800',
 'Roberto Luis', 'Silva', 'Vargas', '70890123',
 'Teresa Alejandra', 'González', 'Castro', '71890123'),

('90123456', 'Nicolás Gabriel', 'Cruz', 'Torrico', '2015-08-20', 'Calle Bolivia #900',
 'Javier Antonio', 'Cruz', 'Pérez', '70901234',
 'Diana Carolina', 'Torrico', 'Quispe', '71901234'),

('01234567', 'Emilia Victoria', 'Mamani', 'López', '2014-02-14', 'Zona Oeste #1000',
 'Hugo Rafael', 'Mamani', 'Condori', '70012345',
 'Silvia Beatriz', 'López', 'Silva', '71012345');

-- =====================================================
-- 3. CURSOS (por gestion 2025)
-- =====================================================

INSERT INTO cursos (nombre_curso, nivel, gestion) VALUES
('1ro de Primaria A', 'primaria', '2025'),
('2do de Primaria A', 'primaria', '2025'),
('3ro de Primaria A', 'primaria', '2025'),
('1ro de Secundaria A', 'secundaria', '2025'),
('2do de Secundaria A', 'secundaria', '2025');

-- =====================================================
-- 4. MATERIAS
-- =====================================================

INSERT INTO materias (nombre_materia, nivel) VALUES
('Matemáticas', 'primaria'),
('Lenguaje', 'primaria'),
('Ciencias Naturales', 'primaria'),
('Ciencias Sociales', 'primaria'),
('Matemáticas', 'secundaria'),
('Física', 'secundaria'),
('Química', 'secundaria'),
('Literatura', 'secundaria');

-- =====================================================
-- 5. APODERADOS
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
-- 7. INSCRIPCIONES ESTUDIANTES-CURSOS
-- =====================================================

-- Curso 1: 1ro de Primaria A
INSERT INTO estudiantes_cursos (id_estudiante, id_curso) VALUES
(1, 1),  -- Pedro Luis
(4, 1),  -- Valentina
(8, 1);  -- Camila

-- Curso 2: 2do de Primaria A
INSERT INTO estudiantes_cursos (id_estudiante, id_curso) VALUES
(2, 2),  -- Sofía
(5, 2),  -- Mateo
(9, 2);  -- Nicolás

-- Curso 3: 3ro de Primaria A
INSERT INTO estudiantes_cursos (id_estudiante, id_curso) VALUES
(6, 3),  -- Isabella
(10, 3); -- Emilia

-- Curso 4: 1ro de Secundaria A
INSERT INTO estudiantes_cursos (id_estudiante, id_curso) VALUES
(3, 4),  -- Diego
(7, 4);  -- Santiago

-- Curso 5: 2do de Secundaria A
-- (Sin estudiantes asignados aún - disponible para pruebas)

-- =====================================================
-- 8. ASIGNACIONES PROFESORES-CURSOS-MATERIAS
-- =====================================================

-- Profesor Roberto Martínez (id_persona: 3) - Matemáticas Primaria
INSERT INTO profesores_cursos_materias (id_profesor, id_curso, id_materia) VALUES
(3, 1, 1),  -- 1ro Primaria - Matemáticas
(3, 2, 1),  -- 2do Primaria - Matemáticas
(3, 3, 1);  -- 3ro Primaria - Matemáticas

-- Profesora Ana Flores (id_persona: 4) - Lenguaje Primaria
INSERT INTO profesores_cursos_materias (id_profesor, id_curso, id_materia) VALUES
(4, 1, 2),  -- 1ro Primaria - Lenguaje
(4, 2, 2),  -- 2do Primaria - Lenguaje
(4, 3, 2);  -- 3ro Primaria - Lenguaje

-- Profesor Carlos Sánchez (id_persona: 5) - Matemáticas y Física Secundaria
INSERT INTO profesores_cursos_materias (id_profesor, id_curso, id_materia) VALUES
(5, 4, 5),  -- 1ro Secundaria - Matemáticas
(5, 4, 6),  -- 1ro Secundaria - Física
(5, 5, 5);  -- 2do Secundaria - Matemáticas

-- Profesora Laura Torres (id_persona: 6) - Literatura Secundaria
INSERT INTO profesores_cursos_materias (id_profesor, id_curso, id_materia) VALUES
(6, 4, 8);  -- 1ro Secundaria - Literatura

-- =====================================================
-- 9. MOTIVOS DE RETIRO (Catálogo)
-- =====================================================

INSERT INTO motivos_retiro (nombre, descripcion, severidad, activo) VALUES
('Cita Médica', 'Estudiante tiene cita médica programada', 'leve', true),
('Emergencia Familiar', 'Situación familiar urgente que requiere la presencia del estudiante', 'grave', true),
('Enfermedad', 'Estudiante presenta síntomas de enfermedad', 'grave', true),
('Trámite Urgente', 'Apoderado necesita realizar trámite con el estudiante', 'leve', true),
('Otro', 'Otros motivos no especificados', 'leve', true);

-- =====================================================
-- SCRIPT COMPLETADO
-- =====================================================

-- Verificar datos insertados
SELECT 'RESUMEN DE DATOS INSERTADOS:' as '';
SELECT COUNT(*) as 'Personas (Profesores/Admin)' FROM personas;
SELECT COUNT(*) as 'Estudiantes' FROM estudiantes;
SELECT COUNT(*) as 'Cursos' FROM cursos;
SELECT COUNT(*) as 'Materias' FROM materias;
SELECT COUNT(*) as 'Apoderados' FROM apoderados;
SELECT COUNT(*) as 'Relaciones Estudiante-Apoderado' FROM estudiantes_apoderados;
SELECT COUNT(*) as 'Inscripciones Estudiante-Curso' FROM estudiantes_cursos;
SELECT COUNT(*) as 'Asignaciones Profesor-Curso-Materia' FROM profesores_cursos_materias;
SELECT COUNT(*) as 'Motivos de Retiro' FROM motivos_retiro;

-- =====================================================
-- NOTAS PARA PRUEBAS:
-- =====================================================
-- 
-- ENDPOINTS LISTOS PARA PROBAR:
-- 
-- 1. POST /api/solicitudes-retiro
--    Usar:
--    - id_estudiante: 1-10
--    - id_apoderado: 1-8
--    - id_motivo: 1-5
--    - id_curso: obtener de estudiantes_cursos
--    - id_materia: obtener de profesores_cursos_materias
--
-- 2. POST /api/autorizaciones-retiro
--    Usar:
--    - decidido_por: 1, 2, 7 (administrativos)
--
-- 3. POST /api/registros-salida
--    Crear después de tener solicitudes aprobadas
--
-- EJEMPLOS DE RELACIONES:
-- - Estudiante 1 (Pedro) tiene 2 apoderados (padre y madre)
-- - Estudiante 5 (Mateo) comparte madre con estudiante 10
-- - Apoderado 1 es padre de estudiante 1 y tío de estudiante 6
-- - Curso 1 tiene 3 estudiantes inscritos
-- - Profesor 3 enseña Matemáticas en 3 cursos de primaria
--
-- =====================================================

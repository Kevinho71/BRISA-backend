USE bienestar_estudiantil;

-- ========================================
-- 1. PERSONAS
-- ========================================
INSERT INTO personas (ci, nombres, apellido_paterno, apellido_materno, direccion, telefono, correo, tipo_persona) VALUES
('1234567','Carlos','Pérez','Gómez','Calle Falsa 123','77712345','carlos.perez@mail.com','profesor'),
('2345678','María','González','Lopez','Av. Siempre Viva 456','77723456','maria.gonzalez@mail.com','profesor'),
('3456789','Juan','Ramírez','Diaz','Calle Sol 789','77734567','juan.ramirez@mail.com','profesor'),
('4567890','Ana','Fernández','Martínez','Av. Luna 101','77745678','ana.fernandez@mail.com','administrativo'),
('5678901','Pedro','Sánchez','Torres','Calle Estrella 202','77756789','pedro.sanchez@mail.com','profesor'),
('6789012','Lucía','Morales','Vega','Av. Río 303','77767890','lucia.morales@mail.com','profesor'),
('7890123','Jorge','Flores','Ríos','Calle Mar 404','77778901','jorge.flores@mail.com','profesor'),
('8901234','Sofía','Castillo','Paredes','Av. Tierra 505','77789012','sofia.castillo@mail.com','profesor'),
('9012345','Miguel','Ramón','Cabrera','Calle Cielo 606','77790123','miguel.ramon@mail.com','profesor'),
('0123456','Elena','Vargas','Salinas','Av. Sol 707','77701234','elena.vargas@mail.com','profesor'),
('1122334','Raúl','Meza','Alvarado','Calle Luna 808','77711223','raul.meza@mail.com','profesor'),
('2233445','Isabel','Torrez','Quintana','Av. Río 909','77722334','isabel.torrez@mail.com','profesor'),
('3344556','Andrés','Mendoza','Rojas','Calle Estrella 111','77733445','andres.mendoza@mail.com','profesor'),
('4455667','Patricia','Loayza','Salcedo','Av. Mar 222','77744556','patricia.loayza@mail.com','profesor'),
('5566778','Fernando','Cordero','Vargas','Calle Tierra 333','77755667','fernando.cordero@mail.com','administrativo');

-- ========================================
-- 2. ROLES
-- ========================================
INSERT INTO roles (nombre, descripcion, is_active, created_at, updated_at) VALUES
('Director','Acceso total al sistema', true, NOW(), NOW()),
('Profesor','Acceso a módulos de estudiantes, esquelas e incidentes', true, NOW(), NOW()),
('Regente','Acceso a incidentes y esquelas', true, NOW(), NOW()),
('Gabinete Psicopedagógico','Acceso a incidentes y seguimiento', true, NOW(), NOW()),
('Gabinete Psicología','Acceso a incidentes y seguimiento', true, NOW(), NOW()),
('Administrativo','Acceso a usuarios y registros de retiros', true, NOW(), NOW()),
('Recepción','Acceso a retiros tempranos', true, NOW(), NOW());

-- ========================================
-- 3. PERMISOS
-- ========================================
INSERT INTO permisos (nombre, descripcion, modulo, is_active, created_at, updated_at) VALUES
-- Módulo de Usuarios
('Lectura', 'Puede ver información', 'usuarios', true, NOW(), NOW()),
('Agregar', 'Puede agregar información', 'usuarios', true, NOW(), NOW()),
('Modificar', 'Puede modificar información', 'usuarios', true, NOW(), NOW()),
('Eliminar', 'Puede eliminar información', 'usuarios', true, NOW(), NOW()),

-- Módulo de Esquelas
('Lectura', 'Puede ver información', 'esquelas', true, NOW(), NOW()),
('Agregar', 'Puede agregar información', 'esquelas', true, NOW(), NOW()),
('Modificar', 'Puede modificar información', 'esquelas', true, NOW(), NOW()),
('Eliminar', 'Puede eliminar información', 'esquelas', true, NOW(), NOW()),

-- Módulo de Incidentes
('Lectura', 'Puede ver información', 'incidentes', true, NOW(), NOW()),
('Agregar', 'Puede agregar información', 'incidentes', true, NOW(), NOW()),
('Modificar', 'Puede modificar información', 'incidentes', true, NOW(), NOW()),
('Eliminar', 'Puede eliminar información', 'incidentes', true, NOW(), NOW()),

-- Módulo de Retiros Tempranos
('Lectura', 'Puede ver información', 'retiros_tempranos', true, NOW(), NOW()),
('Agregar', 'Puede agregar información', 'retiros_tempranos', true, NOW(), NOW()),
('Modificar', 'Puede modificar información', 'retiros_tempranos', true, NOW(), NOW()),
('Eliminar', 'Puede eliminar información', 'retiros_tempranos', true, NOW(), NOW()),

-- Módulo de Reportes
('Lectura', 'Puede ver información', 'reportes', true, NOW(), NOW()),
('Agregar', 'Puede agregar información', 'reportes', true, NOW(), NOW()),
('Modificar', 'Puede modificar información', 'reportes', true, NOW(), NOW()),
('Eliminar', 'Puede eliminar información', 'reportes', true, NOW(), NOW()),

-- Módulo de Profesores
('Lectura', 'Puede ver información', 'profesores', true, NOW(), NOW()),
('Agregar', 'Puede agregar información', 'profesores', true, NOW(), NOW()),
('Modificar', 'Puede modificar información', 'profesores', true, NOW(), NOW()),
('Eliminar', 'Puede eliminar información', 'profesores', true, NOW(), NOW()),

-- Módulo Administración
('Lectura', 'Puede ver información', 'administracion', true, NOW(), NOW()),
('Agregar', 'Puede agregar información', 'administracion', true, NOW(), NOW()),
('Modificar', 'Puede modificar información', 'administracion', true, NOW(), NOW()),
('Eliminar', 'Puede eliminar información', 'administracion', true, NOW(), NOW());

-- ========================================
-- 4. ROL_PERMISOS
-- ========================================
INSERT INTO rol_permisos (id_rol,id_permiso) VALUES
-- Director
(1,1),(1,2),(1,3),(1,4),
(1,5),(1,6),(1,7),(1,8),
(1,9),(1,10),(1,11),(1,12),
(1,13),(1,14),(1,15),(1,16),
(1,17),(1,18),(1,19),(1,20),
(1,21),(1,22),(1,23),(1,24),
(1,25),(1,26),(1,27),(1,28),

-- Profesor
(2,5),(2,6),(2,7),
(2,9),(2,10),(2,11),
(2,21),(2,22),(2,23),

-- Regente
(3,5),(3,6),
(3,9),(3,10),

-- Gabinete Psicopedagógico
(4,9),(4,10),(4,11),

-- Gabinete Psicología

(5,9),(5,10),

-- Administrativo
(6,1),(6,2),(6,3),
(6,13),(6,14),(6,15),

-- Recepción
(7,13),(7,14);


-- ========================================
-- 5. USUARIOS
-- ========================================
INSERT INTO usuarios (id_persona, usuario, correo, password) VALUES
(1,'cperez','carlos.perez@mail.com','1234'),
(2,'mgonzalez','maria.gonzalez@mail.com','1234'),
(3,'jramirez','juan.ramirez@mail.com','1234'),
(4,'afernandez','ana.fernandez@mail.com','1234'),
(5,'psanchez','pedro.sanchez@mail.com','1234'),
(6,'lmorales','lucia.morales@mail.com','1234'),
(7,'jflores','jorge.flores@mail.com','1234'),
(8,'scastillo','sofia.castillo@mail.com','1234'),
(9,'mramon','miguel.ramon@mail.com','1234'),
(10,'evargas','elena.vargas@mail.com','1234'),
(11,'rmeza','raul.meza@mail.com','1234'),
(12,'itorrez','isabel.torrez@mail.com','1234'),
(13,'amendoza','andres.mendoza@mail.com','1234'),
(14,'ploayza','patricia.loayza@mail.com','1234'),
(15,'fcordero','fernando.cordero@mail.com','1234');

-- ========================================
-- 6. USUARIO_ROLES
-- ========================================
INSERT INTO usuario_roles (id_usuario, id_rol, fecha_inicio, estado) VALUES
(1,2,'2025-01-01','activo'),
(2,2,'2025-01-01','activo'),
(3,2,'2025-01-01','activo'),
(4,6,'2025-01-01','activo'),
(5,2,'2025-01-01','activo'),
(6,2,'2025-01-01','activo'),
(7,2,'2025-01-01','activo'),
(8,2,'2025-01-01','activo'),
(9,2,'2025-01-01','activo'),
(10,2,'2025-01-01','activo'),
(11,2,'2025-01-01','activo'),
(12,2,'2025-01-01','activo'),
(13,2,'2025-01-01','activo'),
(14,2,'2025-01-01','activo'),
(15,6,'2025-01-01','activo');

-- ========================================
-- 7. LOGIN_LOGS
-- ========================================
INSERT INTO login_logs (id_usuario, fecha_hora, ip_address, user_agent, estado) VALUES
(1,'2025-09-01 08:00:00','127.0.0.1','Mozilla/5.0','exitoso'),
(2,'2025-09-01 08:05:00','127.0.0.1','Mozilla/5.0','exitoso'),
(3,'2025-09-01 08:10:00','127.0.0.1','Mozilla/5.0','exitoso'),
(4,'2025-09-01 08:15:00','127.0.0.1','Mozilla/5.0','exitoso'),
(5,'2025-09-01 08:20:00','127.0.0.1','Mozilla/5.0','exitoso'),
(6,'2025-09-01 08:25:00','127.0.0.1','Mozilla/5.0','exitoso'),
(7,'2025-09-01 08:30:00','127.0.0.1','Mozilla/5.0','exitoso'),
(8,'2025-09-01 08:35:00','127.0.0.1','Mozilla/5.0','exitoso'),
(9,'2025-09-01 08:40:00','127.0.0.1','Mozilla/5.0','exitoso'),
(10,'2025-09-01 08:45:00','127.0.0.1','Mozilla/5.0','exitoso'),
(11,'2025-09-01 08:50:00','127.0.0.1','Mozilla/5.0','exitoso'),
(12,'2025-09-01 08:55:00','127.0.0.1','Mozilla/5.0','exitoso'),
(13,'2025-09-01 09:00:00','127.0.0.1','Mozilla/5.0','exitoso'),
(14,'2025-09-01 09:05:00','127.0.0.1','Mozilla/5.0','exitoso'),
(15,'2025-09-01 09:10:00','127.0.0.1','Mozilla/5.0','exitoso');

-- ========================================
-- 8. ESTUDIANTES
-- ========================================
INSERT INTO estudiantes (ci, nombres, apellido_paterno, apellido_materno, fecha_nacimiento, direccion, nombre_padre, apellido_paterno_padre, apellido_materno_padre, telefono_padre, nombre_madre, apellido_paterno_madre, apellido_materno_madre, telefono_madre) VALUES
('100001','Luis','Ramirez','Cruz','2012-05-12','Calle A 1','José','Ramirez','Lopez','77711111','María','Cruz','Gómez','77711112'),
('100002','Ana','Torres','Vega','2011-03-22','Calle B 2','Pedro','Torres','Lopez','77722221','Lucía','Vega','Diaz','77722222'),
('100003','Juan','Flores','Paredes','2012-07-15','Calle C 3','Miguel','Flores','Rojas','77733331','Sofía','Paredes','Mendoza','77733332'),
('100004','Carla','Salinas','Alvarado','2011-09-18','Calle D 4','Raúl','Salinas','Vargas','77744441','Elena','Alvarado','Meza','77744442'),
('100005','Diego','Rojas','Lopez','2012-11-20','Calle E 5','Andrés','Rojas','Torres','77755551','Isabel','Lopez','Quintana','77755552'),
('100006','Laura','Mendoza','Salcedo','2011-02-11','Calle F 6','Fernando','Mendoza','Gomez','77766661','Patricia','Salcedo','Vargas','77766662'),
('100007','Miguel','Vargas','Paredes','2012-01-05','Calle G 7','Jorge','Vargas','Rojas','77777771','Ana','Paredes','Torres','77777772'),
('100008','Sofía','Lopez','Ramírez','2011-06-14','Calle H 8','Carlos','Lopez','Diaz','77788881','Lucía','Ramírez','Salinas','77788882'),
('100009','Andrés','Gómez','Vega','2012-03-30','Calle I 9','Pedro','Gómez','Lopez','77799991','Isabel','Vega','Torres','77799992'),
('100010','Patricia','Salazar','Cruz','2011-12-02','Calle J 10','Miguel','Salazar','Rojas','77700001','Sofía','Cruz','Vargas','77700002'),
('100011','Fernando','Ramírez','Lopez','2012-04-05','Calle K 11','Jorge','Ramírez','Diaz','77711113','Ana','Lopez','Martínez','77711114'),
('100012','Elena','Mendoza','Torres','2011-07-16','Calle L 12','Carlos','Mendoza','Gómez','77722223','Lucía','Torres','Rojas','77722224'),
('100013','Raúl','Salinas','Vega','2012-05-25','Calle M 13','Pedro','Salinas','Torres','77733333','Isabel','Vega','Diaz','77733334'),
('100014','Isabel','Lopez','Rojas','2011-08-07','Calle N 14','Miguel','Lopez','Salcedo','77744443','Sofía','Rojas','Torres','77744444'),
('100015','Andrés','Ramírez','Cruz','2012-09-19','Calle O 15','Jorge','Ramírez','Mendoza','77755553','Ana','Cruz','Gómez','77755554');

-- ========================================
-- 9. CURSOS
-- ========================================
INSERT INTO cursos (nombre_curso, nivel, gestion) VALUES
('Inicial A','inicial','2025'),
('Inicial B','inicial','2025'),
('Primaria 1A','primaria','2025'),
('Primaria 1B','primaria','2025'),
('Primaria 2A','primaria','2025'),
('Primaria 2B','primaria','2025'),
('Primaria 3A','primaria','2025'),
('Primaria 3B','primaria','2025'),
('Primaria 4A','primaria','2025'),
('Primaria 4B','primaria','2025'),
('Primaria 5A','primaria','2025'),
('Primaria 5B','primaria','2025'),
('Secundaria 1A','secundaria','2025'),
('Secundaria 1B','secundaria','2025'),
('Secundaria 2A','secundaria','2025');

-- ========================================
-- 10. ESTUDIANTES_CURSOS
-- ========================================
INSERT INTO estudiantes_cursos (id_estudiante, id_curso) VALUES
(1,3),(2,3),(3,4),(4,4),(5,5),(6,5),(7,6),(8,6),(9,7),(10,7),(11,8),(12,8),(13,9),(14,9),(15,10);

-- ========================================
-- 11. MATERIAS
-- ========================================
INSERT INTO materias (nombre_materia, nivel) VALUES
('Matemáticas','primaria'),
('Lengua','primaria'),
('Ciencias','primaria'),
('Inglés','primaria'),
('Historia','primaria'),
('Geografía','primaria'),
('Arte','primaria'),
('Educación Física','primaria'),
('Música','primaria'),
('Informática','primaria'),
('Religión','primaria'),
('Valores','primaria'),
('Tecnología','primaria'),
('Educación Cívica','primaria'),
('Literatura','primaria');

-- ========================================
-- 12. PROFESORES_CURSOS_MATERIAS
-- ========================================
INSERT INTO profesores_cursos_materias (id_profesor,id_curso,id_materia) VALUES
(1,3,1),(1,3,2),(2,4,1),(2,4,2),(3,5,1),(3,5,3),(4,6,4),(5,7,5),(6,8,6),(7,9,7),
(8,10,8),(9,11,9),(10,12,10),(11,13,11),(12,14,12);

-- ========================================
-- 13. APODERADOS
-- ========================================
INSERT INTO apoderados (ci, nombres, apellidos, telefono, correo, direccion) VALUES
('5123456','José Antonio','García Quispe','70123456','jose.garcia@email.com','Calle Los Pinos #100'),
('5234567','Rosa María','Mamani Condori','71123456','rosa.mamani@email.com','Calle Los Pinos #100'),
('5345678','Miguel Ángel','López Vargas','70234567','miguel.lopez@email.com','Av. del Maestro #200'),
('5456789','Carmen Elena','Flores Cruz','71234567','carmen.flores@email.com','Av. del Maestro #200'),
('5567890','Fernando José','Morales Pérez','70345678','fernando.morales@email.com','Zona Central #300'),
('5678901','Ricardo Andrés','Quispe Mamani','70456789','ricardo.quispe@email.com','Calle Libertad #400'),
('5789012','Alberto Daniel','Fernández Torres','70567890','alberto.fernandez@email.com','Av. Principal #500'),
('5890123','Sandra Beatriz','Rojas Morales','71567890','sandra.rojas@email.com','Av. Principal #500'),
('5901234','Jorge Eduardo','Ramírez López','70678901','jorge.ramirez@email.com','Calle Nueva #600'),
('6012345','Patricia Isabel','Mendoza Torres','71678901','patricia.mendoza@email.com','Calle Nueva #600'),
('6123456','Carlos Alberto','Salinas Vega','70789012','carlos.salinas@email.com','Av. Secundaria #700'),
('6234567','María Luisa','Vega Díaz','71789012','maria.vega@email.com','Av. Secundaria #700'),
('6345678','Roberto Carlos','López Rojas','70890123','roberto.lopez@email.com','Zona Norte #800'),
('6456789','Elena Patricia','Rojas Torres','71890123','elena.rojas@email.com','Zona Norte #800'),
('6567890','Daniel Fernando','Ramírez Cruz','70901234','daniel.ramirez@email.com','Calle Central #900'),
('6678901','Ana Carolina','Cruz Gómez','71901234','ana.cruz@email.com','Calle Central #900');

-- ========================================
-- 14. ESTUDIANTES_APODERADOS
-- ========================================
INSERT INTO estudiantes_apoderados (id_estudiante, id_apoderado, parentesco, es_contacto_principal) VALUES
-- Estudiante 1: Luis Ramirez Cruz
(1,1,'Padre',true),
(1,2,'Madre',false),
-- Estudiante 2: Ana Torres Vega
(2,3,'Padre',true),
(2,4,'Madre',false),
-- Estudiante 3: Juan Flores Paredes
(3,5,'Padre',true),
-- Estudiante 4: Carla Salinas Alvarado
(4,6,'Padre',true),
-- Estudiante 5: Diego Rojas Lopez
(5,7,'Padre',false),
(5,8,'Madre',true),
-- Estudiante 6: Laura Mendoza Salcedo (apoderado compartido con estudiante 1)
(6,1,'Tío',true),
-- Estudiante 7: Miguel Vargas Paredes (apoderado compartido)
(7,3,'Abuelo',true),
-- Estudiante 8: Sofía Lopez Ramírez
(8,5,'Padre',true),
-- Estudiante 9: Andrés Gómez Vega
(9,6,'Tutor Legal',true),
-- Estudiante 10: Patricia Salazar Cruz
(10,7,'Padre',true),
(10,8,'Madre',false),
-- Estudiante 11: Fernando Ramírez Lopez
(11,9,'Padre',true),
(11,10,'Madre',false),
-- Estudiante 12: Elena Mendoza Torres
(12,11,'Padre',true),
(12,12,'Madre',false),
-- Estudiante 13: Raúl Salinas Vega
(13,13,'Padre',true),
(13,14,'Madre',false),
-- Estudiante 14: Isabel Lopez Rojas
(14,15,'Padre',true),
(14,16,'Madre',false),
-- Estudiante 15: Andrés Ramírez Cruz
(15,9,'Tío',true);

-- ========================================
-- 15. MOTIVOS_RETIRO
-- ========================================
INSERT INTO motivos_retiro (nombre, descripcion, severidad, activo) VALUES
('Cita Médica','Estudiante tiene cita médica programada','leve',true),
('Emergencia Familiar','Situación familiar urgente que requiere la presencia del estudiante','grave',true),
('Enfermedad','Estudiante presenta síntomas de enfermedad','grave',true),
('Trámite Urgente','Apoderado necesita realizar trámite con el estudiante','leve',true),
('Otro','Otros motivos no especificados','leve',true);

-- ========================================
-- 16. AREAS_INCIDENTE
-- ========================================
INSERT INTO areas_incidente (nombre_area, descripcion) VALUES
('Emocional','Problemas de ansiedad, estrés o autoestima'),
('Convivencia Escolar','Conflictos y bullying'),
('Familiar','Problemas en casa o con tutores'),
('Salud Integral','Conductas de riesgo'),
('Académica','Problemas de rendimiento');

-- ========================================
-- 17. SITUACIONES_INCIDENTE
-- ========================================
INSERT INTO situaciones_incidente (id_area, nombre_situacion, nivel_gravedad) VALUES
(1,'Ansiedad','leve'),
(1,'Baja autoestima','leve'),
(1,'Crisis emocional','grave'),
(2,'Conflicto frecuente','leve'),
(2,'Pelea física','grave'),
(2,'Acoso / Bullying','muy grave'),
(3,'Problemas económicos','grave'),
(3,'Violencia doméstica','muy grave'),
(3,'Separación reciente','leve'),
(4,'Sospecha consumo sustancias','muy grave'),
(4,'Conducta autodestructiva','grave'),
(4,'Crisis identidad personal','leve'),
(5,'Bajo rendimiento','leve'),
(5,'Problemas de atención','grave'),
(5,'Desinterés académico','leve');

-- ========================================
-- 18. INCIDENTES
-- ========================================
INSERT INTO incidentes (fecha, antecedentes, acciones_tomadas, seguimiento, estado) VALUES
('2025-09-01 10:00:00','Conflicto en clase','Llamado de atención','Seguimiento semanal','provisional'),
('2025-09-02 11:00:00','Problema familiar','Consejería','Revisión mensual','derivado'),
('2025-09-03 12:00:00','Baja asistencia','Advertencia','Monitoreo','provisional'),
('2025-09-04 13:00:00','Problema de bullying','Intervención','Seguimiento semanal','derivado'),
('2025-09-05 14:00:00','Rendimiento bajo','Tutoría','Evaluación quincenal','cerrado'),
('2025-09-06 15:00:00','Conflicto en clase','Llamado de atención','Seguimiento semanal','provisional'),
('2025-09-07 16:00:00','Problema familiar','Consejería','Revisión mensual','derivado'),
('2025-09-08 17:00:00','Baja asistencia','Advertencia','Monitoreo','provisional'),
('2025-09-09 08:00:00','Problema de bullying','Intervención','Seguimiento semanal','derivado'),
('2025-09-10 09:00:00','Rendimiento bajo','Tutoría','Evaluación quincenal','cerrado'),
('2025-09-11 10:00:00','Conflicto en clase','Llamado de atención','Seguimiento semanal','provisional'),
('2025-09-12 11:00:00','Problema familiar','Consejería','Revisión mensual','derivado'),
('2025-09-13 12:00:00','Baja asistencia','Advertencia','Monitoreo','provisional'),
('2025-09-14 13:00:00','Problema de bullying','Intervención','Seguimiento semanal','derivado'),
('2025-09-15 14:00:00','Rendimiento bajo','Tutoría','Evaluación quincenal','cerrado');

-- ========================================
-- 19. INCIDENTES_ESTUDIANTES
-- ========================================
INSERT INTO incidentes_estudiantes (id_incidente, id_estudiante) VALUES
(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15);

-- ========================================
-- 20. INCIDENTES_PROFESORES
-- ========================================
INSERT INTO incidentes_profesores (id_incidente, id_profesor) VALUES
(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15);

-- ========================================
-- 21. INCIDENTES_SITUACIONES
-- ========================================
INSERT INTO incidentes_situaciones (id_incidente, id_situacion) VALUES
(1,1),(2,4),(3,14),(4,6),(5,13),(6,3),(7,7),(8,8),(9,12),(10,11),(11,2),(12,5),(13,9),(14,10),(15,15);

-- ========================================
-- 22. CODIGOS_ESQUELAS
-- ========================================
INSERT INTO codigos_esquelas (tipo, codigo, descripcion) VALUES
('reconocimiento','R01','Buen rendimiento académico'),
('reconocimiento','R02','Entrega puntual de tareas'),
('reconocimiento','R03','Buena actitud en clase'),
('reconocimiento','R04','Respeto a compañeros'),
('reconocimiento','R05','Participación activa'),
('orientacion','O01','No respetó normas'),
('orientacion','O02','Faltas frecuentes'),
('orientacion','O03','Problemas de convivencia'),
('orientacion','O04','Desinterés académico'),
('orientacion','O05','Falta de materiales'),
('reconocimiento','R06','Ayuda a compañeros'),
('reconocimiento','R07','Excelente comportamiento'),
('orientacion','O06','Contestó mal al profesor'),
('orientacion','O07','Llegó tarde a clases'),
('reconocimiento','R08','Cumple con los reglamentos');

-- ========================================
-- 23. ESQUELAS
-- ========================================
INSERT INTO esquelas (id_estudiante, id_profesor, id_registrador, fecha, observaciones) VALUES
(1,1,1,'2025-09-01','Excelente desempeño'),
(2,2,2,'2025-09-02','Participación destacada'),
(3,3,3,'2025-09-03','Faltó a clase'),
(4,4,4,'2025-09-04','Buen comportamiento'),
(5,5,5,'2025-09-05','Llegó tarde'),
(6,6,6,'2025-09-06','Entrega puntual'),
(7,7,7,'2025-09-07','No respetó normas'),
(8,8,8,'2025-09-08','Ayuda a compañeros'),
(9,9,9,'2025-09-09','Problema de conducta'),
(10,10,10,'2025-09-10','Buen rendimiento'),
(11,11,11,'2025-09-11','Desinterés académico'),
(12,12,12,'2025-09-12','Excelente comportamiento'),
(13,13,13,'2025-09-13','Llegó tarde'),
(14,14,14,'2025-09-14','Participación activa'),
(15,15,15,'2025-09-15','Buen comportamiento');

-- ========================================
-- 24. ESQUELAS_CODIGOS
-- ========================================
INSERT INTO esquelas_codigos (id_esquela, id_codigo) VALUES
(1,1),(1,2),(2,2),(2,5),(3,6),(3,7),(4,3),(4,1),(5,4),(5,7),
(6,2),(6,8),(7,6),(7,13),(8,1),(8,6),(9,7),(9,4),(10,5),(10,2),
(11,4),(11,3),(12,1),(12,5),(13,7),(13,14),(14,8),(14,5),(15,1),(15,7);


-- ========================================
-- 0. CARGOS
-- ========================================
INSERT INTO cargos (nombre_cargo, descripcion, nivel_jerarquico, is_active) VALUES
('Director General','Máxima autoridad de la institución',1,true),
('Regente','Autoridad pedagógica',2,true),
('Coordinador Académico','Coordinación de actividades académicas',3,true),
('Secretaria','Personal administrativo de secretaría',4,true),
('Auxiliar Administrativo','Apoyo en tareas administrativas',5,true),
('Recepcionista','Atención en recepción',5,true),
('Contador','Gestión contable y financiera',4,true),
('Psicólogo','Gabinete psicopedagógico',3,true),
('Enfermero','Atención de salud escolar',4,true),
('Bibliotecario','Gestión de biblioteca',5,true);

-- ========================================
-- 1. PERSONAS
-- ========================================
INSERT INTO personas (ci, nombres, apellido_paterno, apellido_materno, direccion, telefono, correo, tipo_persona, id_cargo, estado_laboral, años_experiencia, fecha_ingreso, is_active) VALUES
-- Profesores (20 personas)
('1234567','Carlos','Pérez','Gómez','Calle Falsa 123','77712345','carlos.perez@mail.com','profesor',NULL,'activo',15,'2010-02-01',true),
('2345678','María','González','Lopez','Av. Siempre Viva 456','77723456','maria.gonzalez@mail.com','profesor',NULL,'activo',12,'2013-03-15',true),
('3456789','Juan','Ramírez','Diaz','Calle Sol 789','77734567','juan.ramirez@mail.com','profesor',NULL,'activo',10,'2015-01-20',true),
('5678901','Pedro','Sánchez','Torres','Calle Estrella 202','77756789','pedro.sanchez@mail.com','profesor',NULL,'activo',8,'2017-08-10',true),
('6789012','Lucía','Morales','Vega','Av. Río 303','77767890','lucia.morales@mail.com','profesor',NULL,'activo',7,'2018-02-14',true),
('7890123','Jorge','Flores','Ríos','Calle Mar 404','77778901','jorge.flores@mail.com','profesor',NULL,'activo',6,'2019-09-01',true),
('8901234','Sofía','Castillo','Paredes','Av. Tierra 505','77789012','sofia.castillo@mail.com','profesor',NULL,'activo',9,'2016-03-12',true),
('9012345','Miguel','Ramón','Cabrera','Calle Cielo 606','77790123','miguel.ramon@mail.com','profesor',NULL,'activo',11,'2014-05-22',true),
('0123456','Elena','Vargas','Salinas','Av. Sol 707','77701234','elena.vargas@mail.com','profesor',NULL,'activo',13,'2012-07-18',true),
('1122334','Raúl','Meza','Alvarado','Calle Luna 808','77711223','raul.meza@mail.com','profesor',NULL,'activo',5,'2020-01-10',true),
('2233445','Isabel','Torrez','Quintana','Av. Río 909','77722334','isabel.torrez@mail.com','profesor',NULL,'activo',14,'2011-04-05',true),
('3344556','Andrés','Mendoza','Rojas','Calle Estrella 111','77733445','andres.mendoza@mail.com','profesor',NULL,'activo',4,'2021-02-15',true),
('4455667','Patricia','Loayza','Salcedo','Av. Mar 222','77744556','patricia.loayza@mail.com','profesor',NULL,'activo',16,'2009-09-01',true),
('6677889','Roberto','Silva','Moreno','Calle Central 444','77766778','roberto.silva@mail.com','profesor',NULL,'activo',7,'2018-08-20',true),
('7788990','Claudia','Quispe','Mamani','Av. Norte 555','77777889','claudia.quispe@mail.com','profesor',NULL,'activo',6,'2019-03-12',true),
('8899001','Diego','Fernández','Castro','Calle Sur 666','77788990','diego.fernandez@mail.com','profesor',NULL,'activo',5,'2020-07-08',true),
('9900112','Gabriela','López','Vargas','Av. Este 777','77799001','gabriela.lopez@mail.com','profesor',NULL,'activo',8,'2017-11-15',true),
('1011121','Marcelo','Rojas','Pérez','Calle Oeste 888','77710111','marcelo.rojas@mail.com','profesor',NULL,'activo',10,'2015-05-20',true),
('1112131','Valentina','Méndez','Torres','Av. Principal 999','77711213','valentina.mendez@mail.com','profesor',NULL,'activo',3,'2022-01-10',true),
('1213141','Sebastián','Cortez','Ramírez','Calle Nueva 1010','77712131','sebastian.cortez@mail.com','profesor',NULL,'activo',4,'2021-09-01',true),
-- Administrativos (10 personas)
('4567890','Ana','Fernández','Martínez','Av. Luna 101','77745678','ana.fernandez@mail.com','administrativo',1,'activo',20,'2005-01-15',true),
('5566778','Fernando','Cordero','Vargas','Calle Tierra 333','77755667','fernando.cordero@mail.com','administrativo',2,'activo',18,'2007-03-10',true),
('2324252','Carmen','Gutierrez','Salazar','Av. Central 222','77723242','carmen.gutierrez@mail.com','administrativo',4,'activo',12,'2013-06-01',true),
('3425262','Luis','Herrera','Campos','Calle Paz 333','77734252','luis.herrera@mail.com','administrativo',5,'activo',8,'2017-02-20',true),
('4526272','Rosa','Jiménez','Vargas','Av. Libertad 444','77745262','rosa.jimenez@mail.com','administrativo',6,'activo',6,'2019-08-15',true),
('5627282','Alberto','Castro','Moreno','Calle Unión 555','77756272','alberto.castro@mail.com','administrativo',7,'activo',15,'2010-11-01',true),
('6728292','Silvia','Paredes','López','Av. Victoria 666','77767282','silvia.paredes@mail.com','administrativo',8,'activo',10,'2015-04-10',true),
('7829303','Javier','Ortiz','Ramírez','Calle Esperanza 777','77778293','javier.ortiz@mail.com','administrativo',9,'activo',7,'2018-09-05',true),
('8930313','Beatriz','Navarro','Torres','Av. Progreso 888','77789303','beatriz.navarro@mail.com','administrativo',10,'activo',9,'2016-12-01',true),
('9031323','Ricardo','Molina','García','Calle Futuro 999','77790313','ricardo.molina@mail.com','administrativo',5,'activo',5,'2020-03-15',true);

-- ========================================
-- 2. PROFESORES
-- ========================================
INSERT INTO profesores (id_persona, especialidad, titulo_academico, nivel_enseñanza, observaciones) VALUES
(1,'Matemáticas','Licenciado en Educación','primary',NULL),
(2,'Lengua y Literatura','Licenciada en Educación','primary',NULL),
(3,'Ciencias Naturales','Licenciado en Biología','secondary',NULL),
(4,'Historia','Licenciado en Ciencias Sociales','secondary',NULL),
(5,'Inglés','Licenciada en Lenguas','todos',NULL),
(6,'Educación Física','Licenciado en Deportes','todos',NULL),
(7,'Arte','Licenciada en Artes Plásticas','primary',NULL),
(8,'Música','Licenciado en Música','todos',NULL),
(9,'Informática','Ingeniero en Sistemas','secondary',NULL),
(10,'Religión','Licenciado en Teología','todos',NULL),
(11,'Geografía','Licenciada en Geografía','secondary',NULL),
(12,'Química','Licenciado en Química','secondary',NULL),
(13,'Física','Licenciada en Física','secondary',NULL),
(14,'Matemáticas Avanzadas','Licenciado en Matemáticas','secondary',NULL),
(15,'Literatura','Licenciada en Letras','secondary',NULL),
(16,'Biología','Licenciado en Biología','secondary',NULL),
(17,'Educación Inicial','Licenciada en Educación Inicial','foundation',NULL),
(18,'Psicomotricidad','Licenciado en Educación Física','foundation',NULL),
(19,'Lengua Extranjera','Licenciada en Idiomas','primary',NULL),
(20,'Ciencias Sociales','Licenciado en Historia','primary',NULL);

-- ========================================
-- 3. ADMINISTRATIVOS
-- ========================================
INSERT INTO administrativos (id_persona, id_cargo, horario_entrada, horario_salida, area_trabajo, observaciones) VALUES
(21,1,'07:30:00','16:30:00','Dirección','Director General de la institución'),
(22,2,'08:00:00','16:00:00','Regencia','Regente académico'),
(23,4,'08:00:00','16:00:00','Secretaría','Secretaria principal'),
(24,5,'08:00:00','16:00:00','Administración','Auxiliar administrativo'),
(25,6,'07:30:00','15:30:00','Recepción','Recepcionista turno mañana'),
(26,7,'08:00:00','16:00:00','Contabilidad','Contador principal'),
(27,8,'08:00:00','16:00:00','Gabinete Psicopedagógico','Psicólogo escolar'),
(28,9,'08:00:00','16:00:00','Enfermería','Enfermero escolar'),
(29,10,'08:00:00','16:00:00','Biblioteca','Bibliotecario'),
(30,5,'08:00:00','16:00:00','Administración','Auxiliar administrativo 2');

-- ========================================
-- 4. ROLES
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
-- 5. PERMISOS
-- ========================================
INSERT INTO permisos (nombre, descripcion, modulo) VALUES
-- Módulo de Usuarios
('Lectura', 'Puede ver información', 'usuarios'),
('Agregar', 'Puede agregar información', 'usuarios'),
('Modificar', 'Puede modificar información', 'usuarios'),
('Eliminar', 'Puede eliminar información', 'usuarios'),

-- Módulo de Esquelas
('Lectura', 'Puede ver información', 'esquelas'),
('Agregar', 'Puede agregar información', 'esquelas'),
('Modificar', 'Puede modificar información', 'esquelas'),
('Eliminar', 'Puede eliminar información', 'esquelas'),

-- Módulo de Incidentes
('Lectura', 'Puede ver información', 'incidentes'),
('Agregar', 'Puede agregar información', 'incidentes'),
('Modificar', 'Puede modificar información', 'incidentes'),
('Eliminar', 'Puede eliminar información', 'incidentes'),

-- Módulo de Retiros Tempranos
('Lectura', 'Puede ver información', 'retiros_tempranos'),
('Agregar', 'Puede agregar información', 'retiros_tempranos'),
('Modificar', 'Puede modificar información', 'retiros_tempranos'),
('Eliminar', 'Puede eliminar información', 'retiros_tempranos'),

-- Módulo de Reportes
('Lectura', 'Puede ver información', 'reportes'),
('Agregar', 'Puede agregar información', 'reportes'),
('Modificar', 'Puede modificar información', 'reportes'),
('Eliminar', 'Puede eliminar información', 'reportes'),

-- Módulo de Profesores
('Lectura', 'Puede ver información', 'profesores'),
('Agregar', 'Puede agregar información', 'profesores'),
('Modificar', 'Puede modificar información', 'profesores'),
('Eliminar', 'Puede eliminar información', 'profesores'),

-- Módulo Administración
('Lectura', 'Puede ver información', 'administracion'),
('Agregar', 'Puede agregar información', 'administracion'),
('Modificar', 'Puede modificar información', 'administracion'),
('Eliminar', 'Puede eliminar información', 'administracion');

-- ========================================
-- 6. ROL_PERMISOS
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
-- 7. USUARIOS
-- ========================================
INSERT INTO usuarios (id_persona, usuario, correo, password) VALUES
-- Profesores (20 usuarios)
(1,'cperez','carlos.perez@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(2,'mgonzalez','maria.gonzalez@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(3,'jramirez','juan.ramirez@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(4,'psanchez','pedro.sanchez@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(5,'lmorales','lucia.morales@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(6,'jflores','jorge.flores@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(7,'scastillo','sofia.castillo@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(8,'mramon','miguel.ramon@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(9,'evargas','elena.vargas@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(10,'rmeza','raul.meza@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(11,'itorrez','isabel.torrez@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(12,'amendoza','andres.mendoza@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(13,'ploayza','patricia.loayza@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(14,'rsilva','roberto.silva@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(15,'cquispe','claudia.quispe@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(16,'dfernandez','diego.fernandez@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(17,'glopez','gabriela.lopez@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(18,'mrojas','marcelo.rojas@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(19,'vmendez','valentina.mendez@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(20,'scortez','sebastian.cortez@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
-- Administrativos (10 usuarios)
(21,'afernandez','ana.fernandez@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(22,'fcordero','fernando.cordero@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(23,'cgutierrez','carmen.gutierrez@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(24,'lherrera','luis.herrera@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(25,'rjimenez','rosa.jimenez@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(26,'acastro','alberto.castro@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(27,'sparedes','silvia.paredes@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(28,'jortiz','javier.ortiz@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(29,'bnavarro','beatriz.navarro@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy'),
(30,'rmolina','ricardo.molina@mail.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILCPEMdLy');

-- ========================================
-- 8. USUARIO_ROLES
-- ========================================
INSERT INTO usuario_roles (id_usuario, id_rol, fecha_inicio, estado) VALUES
-- Profesores (20 roles)
(1,2,'2025-01-01','activo'),
(2,2,'2025-01-01','activo'),
(3,2,'2025-01-01','activo'),
(4,2,'2025-01-01','activo'),
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
(15,2,'2025-01-01','activo'),
(16,2,'2025-01-01','activo'),
(17,2,'2025-01-01','activo'),
(18,2,'2025-01-01','activo'),
(19,2,'2025-01-01','activo'),
(20,2,'2025-01-01','activo'),
-- Administrativos (10 roles)
(21,1,'2025-01-01','activo'), -- Director
(22,3,'2025-01-01','activo'), -- Regente
(23,6,'2025-01-01','activo'), -- Administrativo
(24,6,'2025-01-01','activo'), -- Administrativo
(25,7,'2025-01-01','activo'), -- Recepción
(26,6,'2025-01-01','activo'), -- Administrativo
(27,4,'2025-01-01','activo'), -- Gabinete Psicopedagógico
(28,6,'2025-01-01','activo'), -- Administrativo
(29,6,'2025-01-01','activo'), -- Administrativo
(30,6,'2025-01-01','activo'); -- Administrativo

-- ========================================
-- 9. LOGIN_LOGS
-- ========================================
INSERT INTO login_logs (id_usuario, fecha_hora, ip_address, user_agent, estado) VALUES
(1,'2025-09-01 08:00:00','192.168.1.101','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','exitoso'),
(2,'2025-09-01 08:05:00','192.168.1.102','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','exitoso'),
(3,'2025-09-01 08:10:00','192.168.1.103','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)','exitoso'),
(21,'2025-09-01 07:30:00','192.168.1.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','exitoso'),
(22,'2025-09-01 07:45:00','192.168.1.2','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','exitoso'),
(25,'2025-09-01 07:30:00','192.168.1.5','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','exitoso'),
(4,'2025-09-01 08:15:00','192.168.1.104','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)','exitoso'),
(5,'2025-09-01 08:20:00','192.168.1.105','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','exitoso'),
(1,'2025-09-02 08:00:00','192.168.1.101','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','exitoso'),
(2,'2025-09-02 08:05:00','192.168.1.102','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','exitoso'),
(21,'2025-09-02 07:30:00','192.168.1.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','exitoso'),
(3,'2025-09-02 08:15:00','192.168.1.103','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','fallido'),
(3,'2025-09-02 08:16:00','192.168.1.103','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','exitoso'),
(27,'2025-09-01 08:00:00','192.168.1.27','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','exitoso'),
(28,'2025-09-01 08:00:00','192.168.1.28','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','exitoso'),
(6,'2025-09-03 08:00:00','192.168.1.106','Mozilla/5.0 (X11; Linux x86_64)','exitoso'),
(7,'2025-09-03 08:05:00','192.168.1.107','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','exitoso'),
(8,'2025-09-03 08:10:00','192.168.1.108','Mozilla/5.0 (iPad; CPU OS 14_7_1 like Mac OS X)','exitoso'),
(9,'2025-09-03 08:15:00','192.168.1.109','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','exitoso'),
(10,'2025-09-03 08:20:00','192.168.1.110','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)','exitoso');

-- ========================================
-- 10. ESTUDIANTES
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
-- 11. CURSOS
-- ========================================
INSERT INTO cursos (nombre_curso, nivel, gestion) VALUES
-- Inicial (3 cursos)
('Inicial A','inicial','2025'),
('Inicial B','inicial','2025'),
('Inicial C','inicial','2025'),
-- Primaria (12 cursos)
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
('Primaria 6A','primaria','2025'),
('Primaria 6B','primaria','2025'),
-- Secundaria (12 cursos)
('Secundaria 1A','secundaria','2025'),
('Secundaria 1B','secundaria','2025'),
('Secundaria 2A','secundaria','2025'),
('Secundaria 2B','secundaria','2025'),
('Secundaria 3A','secundaria','2025'),
('Secundaria 3B','secundaria','2025'),
('Secundaria 4A','secundaria','2025'),
('Secundaria 4B','secundaria','2025'),
('Secundaria 5A','secundaria','2025'),
('Secundaria 5B','secundaria','2025'),
('Secundaria 6A','secundaria','2025'),
('Secundaria 6B','secundaria','2025');

-- ========================================
-- 12. ESTUDIANTES_CURSOS
-- ========================================
INSERT INTO estudiantes_cursos (id_estudiante, id_curso) VALUES
(1,4),(2,4),(3,5),(4,5),(5,6),(6,6),(7,7),(8,7),(9,8),(10,8),(11,9),(12,9),(13,10),(14,10),(15,11);

-- ========================================
-- 13. MATERIAS
-- ========================================
INSERT INTO materias (nombre_materia, nivel) VALUES
-- Inicial (5 materias)
('Psicomotricidad','inicial'),
('Lenguaje','inicial'),
('Matemática Inicial','inicial'),
('Arte y Creatividad','inicial'),
('Música y Expresión','inicial'),
-- Primaria (11 materias)
('Matemáticas','primaria'),
('Lengua y Literatura','primaria'),
('Ciencias Naturales','primaria'),
('Ciencias Sociales','primaria'),
('Inglés','primaria'),
('Educación Física','primaria'),
('Arte','primaria'),
('Música','primaria'),
('Informática','primaria'),
('Religión','primaria'),
('Valores y Ética','primaria'),
-- Secundaria (13 materias)
('Matemática Avanzada','secundaria'),
('Física','secundaria'),
('Química','secundaria'),
('Biología','secundaria'),
('Historia','secundaria'),
('Geografía','secundaria'),
('Literatura','secundaria'),
('Inglés Avanzado','secundaria'),
('Educación Física','secundaria'),
('Informática y Tecnología','secundaria'),
('Filosofía','secundaria'),
('Economía','secundaria'),
('Cívica y Ciudadanía','secundaria');

-- ========================================
-- 14. PROFESORES_CURSOS_MATERIAS
-- ========================================
INSERT INTO profesores_cursos_materias (id_profesor,id_curso,id_materia) VALUES
-- Primaria 1A y 1B (cursos 4 y 5)
(1,4,6),(1,5,6),   -- Matemáticas
(2,4,7),(2,5,7),   -- Lengua
(5,4,10),(5,5,10), -- Inglés
(6,4,11),(6,5,11), -- Ed. Física
(7,4,12),(7,5,12), -- Arte
-- Primaria 2A y 2B (cursos 6 y 7)
(1,6,6),(1,7,6),   -- Matemáticas
(2,6,7),(2,7,7),   -- Lengua
(3,6,8),(3,7,8),   -- Ciencias Naturales
(5,6,10),(5,7,10), -- Inglés
(8,6,13),(8,7,13), -- Música
-- Primaria 3A y 3B (cursos 8 y 9)
(1,8,6),(1,9,6),   -- Matemáticas
(2,8,7),(2,9,7),   -- Lengua
(3,8,8),(3,9,8),   -- Ciencias Naturales
(4,8,9),(4,9,9),   -- Ciencias Sociales
(9,8,14),(9,9,14), -- Informática
-- Primaria 4A y 4B (cursos 10 y 11)
(1,10,6),(1,11,6),  -- Matemáticas
(2,10,7),(2,11,7),  -- Lengua
(3,10,8),(3,11,8),  -- Ciencias Naturales
(8,10,13),(8,11,13), -- Música
(10,10,15),(10,11,15), -- Religión
-- Secundaria 1A y 1B (cursos 16 y 17)
(14,16,17),(14,17,17), -- Matemática Avanzada
(13,16,18),(13,17,18), -- Física
(12,16,19),(12,17,19), -- Química
(16,16,20),(16,17,20), -- Biología
(4,16,21),(4,17,21),   -- Historia
-- Secundaria 2A y 2B (cursos 18 y 19)
(14,18,17),(14,19,17), -- Matemática Avanzada
(16,18,20),(16,19,20), -- Biología
(11,18,22),(11,19,22), -- Geografía
(15,18,23),(15,19,23), -- Literatura
-- Secundaria 3A y 3B (cursos 20 y 21)
(13,20,18),(13,21,18), -- Física
(12,20,19),(12,21,19), -- Química
(11,20,22),(11,21,22), -- Geografía
(9,20,26),(9,21,26);   -- Informática y Tecnología

-- ========================================
-- 15. APODERADOS
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
-- 16. ESTUDIANTES_APODERADOS
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
-- 17. MOTIVOS_RETIRO
-- ========================================
INSERT INTO motivos_retiro (nombre, descripcion, severidad, activo) VALUES
('Cita Médica','Estudiante tiene cita médica programada','leve',true),
('Emergencia Familiar','Situación familiar urgente que requiere la presencia del estudiante','grave',true),
('Enfermedad','Estudiante presenta síntomas de enfermedad','grave',true),
('Trámite Urgente','Apoderado necesita realizar trámite con el estudiante','leve',true),
('Otro','Otros motivos no especificados','leve',true);

-- ========================================
-- 18. AREAS_INCIDENTE
-- ========================================
INSERT INTO areas_incidente (nombre_area, descripcion) VALUES
('Emocional','Problemas de ansiedad, estrés o autoestima'),
('Convivencia Escolar','Conflictos y bullying'),
('Familiar','Problemas en casa o con tutores'),
('Salud Integral','Conductas de riesgo'),
('Académica','Problemas de rendimiento');

-- ========================================
-- 19. SITUACIONES_INCIDENTE
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
-- 20. INCIDENTES
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
-- 21. INCIDENTES_ESTUDIANTES
-- ========================================
INSERT INTO incidentes_estudiantes (id_incidente, id_estudiante) VALUES
(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15);

-- ========================================
-- 22. INCIDENTES_PROFESORES
-- ========================================
INSERT INTO incidentes_profesores (id_incidente, id_profesor) VALUES
(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15);

-- ========================================
-- 23. INCIDENTES_SITUACIONES
-- ========================================
INSERT INTO incidentes_situaciones (id_incidente, id_situacion) VALUES
(1,1),(2,4),(3,14),(4,6),(5,13),(6,3),(7,7),(8,8),(9,12),(10,11),(11,2),(12,5),(13,9),(14,10),(15,15);

-- ========================================
-- 24. CODIGOS_ESQUELAS
-- ========================================
INSERT INTO codigos_esquelas (tipo, codigo, descripcion) VALUES
-- Reconocimientos (15 códigos)
('reconocimiento','R01','Buen rendimiento académico'),
('reconocimiento','R02','Entrega puntual de tareas'),
('reconocimiento','R03','Buena actitud en clase'),
('reconocimiento','R04','Respeto a compañeros'),
('reconocimiento','R05','Participación activa'),
('reconocimiento','R06','Ayuda a compañeros'),
('reconocimiento','R07','Excelente comportamiento'),
('reconocimiento','R08','Cumple con los reglamentos'),
('reconocimiento','R09','Liderazgo positivo'),
('reconocimiento','R10','Iniciativa propia'),
('reconocimiento','R11','Creatividad destacada'),
('reconocimiento','R12','Solidaridad con compañeros'),
('reconocimiento','R13','Presentación personal impecable'),
('reconocimiento','R14','Progreso académico notable'),
('reconocimiento','R15','Colaboración en actividades escolares'),
-- Orientaciones (15 códigos)
('orientacion','O01','No respetó normas'),
('orientacion','O02','Faltas frecuentes'),
('orientacion','O03','Problemas de convivencia'),
('orientacion','O04','Desinterés académico'),
('orientacion','O05','Falta de materiales'),
('orientacion','O06','Contestó mal al profesor'),
('orientacion','O07','Llegó tarde a clases'),
('orientacion','O08','No realizó tareas'),
('orientacion','O09','Uso inadecuado de celular'),
('orientacion','O10','Uniforme incompleto'),
('orientacion','O11','Distracción en clase'),
('orientacion','O12','Falta de respeto'),
('orientacion','O13','Vocabulario inapropiado'),
('orientacion','O14','No trajo materiales solicitados'),
('orientacion','O15','Desorden en el aula');

-- ========================================
-- 25. ESQUELAS
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
-- 26. ESQUELAS_CODIGOS
-- ========================================
INSERT INTO esquelas_codigos (id_esquela, id_codigo) VALUES
(1,1),(1,2),(2,2),(2,5),(3,6),(3,7),(4,3),(4,1),(5,4),(5,7),
(6,2),(6,8),(7,6),(7,13),(8,1),(8,6),(9,7),(9,4),(10,5),(10,2),
(11,4),(11,3),(12,1),(12,5),(13,7),(13,14),(14,8),(14,5),(15,1),(15,7);

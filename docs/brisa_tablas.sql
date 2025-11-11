CREATE TABLE `personas` (
  `id_persona` int PRIMARY KEY AUTO_INCREMENT,
  `ci` varchar(20) NOT NULL,
  `nombres` varchar(50) NOT NULL,
  `apellido_paterno` varchar(50) NOT NULL,
  `apellido_materno` varchar(50) NOT NULL,
  `direccion` varchar(100),
  `telefono` varchar(20),
  `correo` varchar(50) UNIQUE,
  `tipo_persona` ENUM ('profesor', 'administrativo') NOT NULL,
  `is_active` boolean NOT NULL DEFAULT true
);

CREATE TABLE `roles` (
  `id_rol` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(255),
  `is_active` boolean NOT NULL DEFAULT true,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `created_by` int,
  `updated_by` int
);

CREATE TABLE `permisos` (
  `id_permiso` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(255),
  `modulo` varchar(50) NOT NULL,
  `is_active` boolean NOT NULL DEFAULT true,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `created_by` int,
  `updated_by` int
);

CREATE TABLE `rol_permisos` (
  `id_rol` int NOT NULL,
  `id_permiso` int NOT NULL,
  PRIMARY KEY (`id_rol`, `id_permiso`)
);

CREATE TABLE `usuarios` (
  `id_usuario` int PRIMARY KEY AUTO_INCREMENT,
  `id_persona` int NOT NULL,
  `usuario` varchar(50) UNIQUE NOT NULL,
  `correo` varchar(50) UNIQUE NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_active` boolean NOT NULL DEFAULT true
);

CREATE TABLE `usuario_roles` (
  `id_usuario` int NOT NULL,
  `id_rol` int NOT NULL,
  `fecha_inicio` datetime NOT NULL,
  `fecha_fin` datetime,
  `estado` ENUM ('activo', 'inactivo') NOT NULL,
  PRIMARY KEY (`id_usuario`, `id_rol`, `fecha_inicio`)
);

CREATE TABLE `login_logs` (
  `id_log` int PRIMARY KEY AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `fecha_hora` datetime NOT NULL,
  `ip_address` varchar(45),
  `user_agent` varchar(255),
  `estado` ENUM ('exitoso', 'fallido') NOT NULL
);

CREATE TABLE `rol_historial` (
  `id_historial` int PRIMARY KEY AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `id_rol` int NOT NULL,
  `accion` ENUM ('asignado', 'revocado') NOT NULL,
  `razon` text,
  `created_at` datetime NOT NULL,
  `created_by` int
);

CREATE TABLE `bitacora` (
  `id_bitacora` int PRIMARY KEY AUTO_INCREMENT,
  `id_usuario_admin` int NOT NULL,
  `accion` varchar(50) NOT NULL,
  `descripcion` text,
  `id_objetivo` int,
  `tipo_objetivo` varchar(50),
  `fecha_hora` datetime 
);

CREATE TABLE `estudiantes` (
  `id_estudiante` int PRIMARY KEY AUTO_INCREMENT,
  `ci` varchar(20),
  `nombres` varchar(50) NOT NULL,
  `apellido_paterno` varchar(50) NOT NULL,
  `apellido_materno` varchar(50) NOT NULL,
  `fecha_nacimiento` date,
  `direccion` varchar(100),
  `nombre_padre` varchar(50),
  `apellido_paterno_padre` varchar(50),
  `apellido_materno_padre` varchar(50),
  `telefono_padre` varchar(20),
  `nombre_madre` varchar(50),
  `apellido_paterno_madre` varchar(50),
  `apellido_materno_madre` varchar(50),
  `telefono_madre` varchar(20)
);

CREATE TABLE `cursos` (
  `id_curso` int PRIMARY KEY AUTO_INCREMENT,
  `nombre_curso` varchar(50) NOT NULL,
  `nivel` ENUM ('inicial', 'primaria', 'secundaria') NOT NULL,
  `gestion` varchar(20) NOT NULL
);

CREATE TABLE `estudiantes_cursos` (
  `id_estudiante` int NOT NULL,
  `id_curso` int NOT NULL,
  PRIMARY KEY (`id_estudiante`, `id_curso`)
);

CREATE TABLE `apoderados` (
  `id_apoderado` int PRIMARY KEY AUTO_INCREMENT,
  `ci` varchar(20) UNIQUE NOT NULL,
  `nombres` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `telefono` varchar(20),
  `correo` varchar(50),
  `direccion` varchar(100)
);

CREATE TABLE `estudiantes_apoderados` (
  `id_estudiante` int NOT NULL,
  `id_apoderado` int NOT NULL,
  `parentesco` varchar(50) NOT NULL,
  `es_contacto_principal` boolean DEFAULT false,
  PRIMARY KEY (`id_estudiante`, `id_apoderado`)
);

CREATE TABLE `materias` (
  `id_materia` int PRIMARY KEY AUTO_INCREMENT,
  `nombre_materia` varchar(50) NOT NULL,
  `nivel` ENUM ('inicial', 'primaria', 'secundaria') NOT NULL
);

CREATE TABLE `profesores_cursos_materias` (
  `id_profesor` int NOT NULL,
  `id_curso` int NOT NULL,
  `id_materia` int NOT NULL,
  PRIMARY KEY (`id_profesor`, `id_curso`, `id_materia`)
);

CREATE TABLE `motivos_retiro` (
  `id_motivo` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(100) UNIQUE NOT NULL,
  `descripcion` varchar(255),
  `severidad` ENUM ('leve', 'grave', 'muy grave') NOT NULL,
  `activo` boolean NOT NULL DEFAULT true
);

CREATE TABLE `autorizaciones_retiro` (
  `id_autorizacion` int PRIMARY KEY AUTO_INCREMENT,
  `decidido_por` int NOT NULL,
  `decision` ENUM ('aprobado', 'rechazado', 'pendiente') NOT NULL,
  `motivo_decision` varchar(255),
  `fecha_decision` datetime NOT NULL
);

CREATE TABLE `solicitudes_retiro` (
  `id_solicitud` int PRIMARY KEY AUTO_INCREMENT,
  `id_estudiante` int NOT NULL,
  `id_apoderado` int NOT NULL,
  `id_motivo` int NOT NULL,
  `id_autorizacion` int,
  `fecha_hora_salida` datetime NOT NULL,
  `fecha_hora_retorno_previsto` datetime,
  `observacion` text,
  `foto_retirante_url` varchar(300),
  `fecha_creacion` datetime NOT NULL
);

CREATE TABLE `solicitudes_retiro_detalle` (
  `id_detalle` int PRIMARY KEY AUTO_INCREMENT,
  `id_solicitud` int NOT NULL,
  `id_curso` int NOT NULL,
  `id_materia` int NOT NULL
);

CREATE TABLE `registros_salida` (
  `id_registro` int PRIMARY KEY AUTO_INCREMENT,
  `id_solicitud` int UNIQUE NOT NULL,
  `id_estudiante` int NOT NULL,
  `fecha_hora_salida_real` datetime NOT NULL,
  `fecha_hora_retorno_real` datetime
);

CREATE TABLE `areas_incidente` (
  `id_area` int PRIMARY KEY AUTO_INCREMENT,
  `nombre_area` varchar(50) NOT NULL,
  `descripcion` varchar(255)
);

CREATE TABLE `situaciones_incidente` (
  `id_situacion` int PRIMARY KEY AUTO_INCREMENT,
  `id_area` int NOT NULL,
  `nombre_situacion` varchar(50) NOT NULL,
  `nivel_gravedad` ENUM ('leve', 'grave', 'muy grave') NOT NULL
);

CREATE TABLE `incidentes` (
  `id_incidente` int PRIMARY KEY AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `antecedentes` text,
  `acciones_tomadas` text,
  `seguimiento` text,
  `estado` ENUM ('provisional', 'derivado', 'cerrado') NOT NULL,
  `id_estado_catalogo` int
);

CREATE TABLE `incidentes_estudiantes` (
  `id_incidente` int NOT NULL,
  `id_estudiante` int NOT NULL,
  PRIMARY KEY (`id_incidente`, `id_estudiante`)
);

CREATE TABLE `incidentes_profesores` (
  `id_incidente` int NOT NULL,
  `id_profesor` int NOT NULL,
  PRIMARY KEY (`id_incidente`, `id_profesor`)
);

CREATE TABLE `incidentes_situaciones` (
  `id_incidente` int NOT NULL,
  `id_situacion` int NOT NULL,
  PRIMARY KEY (`id_incidente`, `id_situacion`)
);

CREATE TABLE `estados_incidente` (
  `id_estado` int PRIMARY KEY AUTO_INCREMENT,
  `nombre_estado` varchar(50) UNIQUE NOT NULL,
  `descripcion` varchar(255)
);

CREATE TABLE `derivaciones` (
  `id_derivacion` int PRIMARY KEY AUTO_INCREMENT,
  `id_incidente` int NOT NULL,
  `id_quien_deriva` int NOT NULL,
  `id_quien_recibe` int NOT NULL,
  `fecha_derivacion` datetime NOT NULL,
  `id_estado_anterior` int NOT NULL,
  `id_estado_nuevo` int NOT NULL,
  `observaciones` text
);

CREATE TABLE `historial_modificaciones` (
  `id_historial` int PRIMARY KEY AUTO_INCREMENT,
  `id_incidente` int NOT NULL,
  `id_usuario` int NOT NULL,
  `fecha_cambio` datetime NOT NULL,
  `campo_modificado` varchar(100) NOT NULL,
  `valor_anterior` text,
  `valor_nuevo` text
);

CREATE TABLE `adjuntos` (
  `id_adjunto` int PRIMARY KEY AUTO_INCREMENT,
  `id_incidente` int NOT NULL,
  `nombre_archivo` varchar(200) NOT NULL,
  `ruta` varchar(300) NOT NULL,
  `tipo_mime` varchar(50) NOT NULL,
  `tamanio_bytes` int,
  `subido_por` int NOT NULL,
  `fecha_subida` datetime NOT NULL
);

CREATE TABLE `codigos_esquelas` (
  `id_codigo` int PRIMARY KEY AUTO_INCREMENT,
  `tipo` ENUM ('reconocimiento', 'orientacion') NOT NULL,
  `codigo` varchar(10) NOT NULL,
  `descripcion` varchar(255) NOT NULL
);

CREATE TABLE `esquelas` (
  `id_esquela` int PRIMARY KEY AUTO_INCREMENT,
  `id_estudiante` int NOT NULL,
  `id_profesor` int NOT NULL,
  `id_registrador` int NOT NULL,
  `fecha` date NOT NULL,
  `observaciones` text
);

CREATE TABLE `esquelas_codigos` (
  `id_esquela` int NOT NULL,
  `id_codigo` int NOT NULL,
  PRIMARY KEY (`id_esquela`, `id_codigo`)
);

ALTER TABLE `rol_permisos` ADD FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);

ALTER TABLE `rol_permisos` ADD FOREIGN KEY (`id_permiso`) REFERENCES `permisos` (`id_permiso`);

ALTER TABLE `usuarios` ADD FOREIGN KEY (`id_persona`) REFERENCES `personas` (`id_persona`);

ALTER TABLE `usuario_roles` ADD FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

ALTER TABLE `usuario_roles` ADD FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);

ALTER TABLE `login_logs` ADD FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

ALTER TABLE `rol_historial` ADD FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

ALTER TABLE `rol_historial` ADD FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);

ALTER TABLE `rol_historial` ADD FOREIGN KEY (`created_by`) REFERENCES `usuarios` (`id_usuario`);

ALTER TABLE `bitacora` ADD FOREIGN KEY (`id_usuario_admin`) REFERENCES `usuarios` (`id_usuario`);

ALTER TABLE `estudiantes_cursos` ADD FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`);

ALTER TABLE `estudiantes_cursos` ADD FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`);

ALTER TABLE `estudiantes_apoderados` ADD FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`);

ALTER TABLE `estudiantes_apoderados` ADD FOREIGN KEY (`id_apoderado`) REFERENCES `apoderados` (`id_apoderado`);

ALTER TABLE `profesores_cursos_materias` ADD FOREIGN KEY (`id_profesor`) REFERENCES `personas` (`id_persona`);

ALTER TABLE `profesores_cursos_materias` ADD FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`);

ALTER TABLE `profesores_cursos_materias` ADD FOREIGN KEY (`id_materia`) REFERENCES `materias` (`id_materia`);

ALTER TABLE `autorizaciones_retiro` ADD FOREIGN KEY (`decidido_por`) REFERENCES `personas` (`id_persona`);

ALTER TABLE `solicitudes_retiro` ADD FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`);

ALTER TABLE `solicitudes_retiro` ADD FOREIGN KEY (`id_apoderado`) REFERENCES `apoderados` (`id_apoderado`);

ALTER TABLE `solicitudes_retiro` ADD FOREIGN KEY (`id_motivo`) REFERENCES `motivos_retiro` (`id_motivo`);

ALTER TABLE `solicitudes_retiro` ADD FOREIGN KEY (`id_autorizacion`) REFERENCES `autorizaciones_retiro` (`id_autorizacion`);

ALTER TABLE `solicitudes_retiro_detalle` ADD FOREIGN KEY (`id_solicitud`) REFERENCES `solicitudes_retiro` (`id_solicitud`);

ALTER TABLE `solicitudes_retiro_detalle` ADD FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`);

ALTER TABLE `solicitudes_retiro_detalle` ADD FOREIGN KEY (`id_materia`) REFERENCES `materias` (`id_materia`);

ALTER TABLE `registros_salida` ADD FOREIGN KEY (`id_solicitud`) REFERENCES `solicitudes_retiro` (`id_solicitud`);

ALTER TABLE `registros_salida` ADD FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`);

ALTER TABLE `situaciones_incidente` ADD FOREIGN KEY (`id_area`) REFERENCES `areas_incidente` (`id_area`);

ALTER TABLE `incidentes` ADD FOREIGN KEY (`id_estado_catalogo`) REFERENCES `estados_incidente` (`id_estado`);

ALTER TABLE `incidentes_estudiantes` ADD FOREIGN KEY (`id_incidente`) REFERENCES `incidentes` (`id_incidente`);

ALTER TABLE `incidentes_estudiantes` ADD FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`);

ALTER TABLE `incidentes_profesores` ADD FOREIGN KEY (`id_incidente`) REFERENCES `incidentes` (`id_incidente`);

ALTER TABLE `incidentes_profesores` ADD FOREIGN KEY (`id_profesor`) REFERENCES `personas` (`id_persona`);

ALTER TABLE `incidentes_situaciones` ADD FOREIGN KEY (`id_incidente`) REFERENCES `incidentes` (`id_incidente`);

ALTER TABLE `incidentes_situaciones` ADD FOREIGN KEY (`id_situacion`) REFERENCES `situaciones_incidente` (`id_situacion`);

ALTER TABLE `derivaciones` ADD FOREIGN KEY (`id_incidente`) REFERENCES `incidentes` (`id_incidente`);

ALTER TABLE `derivaciones` ADD FOREIGN KEY (`id_quien_deriva`) REFERENCES `personas` (`id_persona`);

ALTER TABLE `derivaciones` ADD FOREIGN KEY (`id_quien_recibe`) REFERENCES `personas` (`id_persona`);

ALTER TABLE `derivaciones` ADD FOREIGN KEY (`id_estado_anterior`) REFERENCES `estados_incidente` (`id_estado`);

ALTER TABLE `derivaciones` ADD FOREIGN KEY (`id_estado_nuevo`) REFERENCES `estados_incidente` (`id_estado`);

ALTER TABLE `historial_modificaciones` ADD FOREIGN KEY (`id_incidente`) REFERENCES `incidentes` (`id_incidente`);

ALTER TABLE `historial_modificaciones` ADD FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

ALTER TABLE `adjuntos` ADD FOREIGN KEY (`id_incidente`) REFERENCES `incidentes` (`id_incidente`);

ALTER TABLE `adjuntos` ADD FOREIGN KEY (`subido_por`) REFERENCES `personas` (`id_persona`);

ALTER TABLE `esquelas` ADD FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`);

ALTER TABLE `esquelas` ADD FOREIGN KEY (`id_profesor`) REFERENCES `personas` (`id_persona`);

ALTER TABLE `esquelas` ADD FOREIGN KEY (`id_registrador`) REFERENCES `personas` (`id_persona`);

ALTER TABLE `esquelas_codigos` ADD FOREIGN KEY (`id_esquela`) REFERENCES `esquelas` (`id_esquela`);

ALTER TABLE `esquelas_codigos` ADD FOREIGN KEY (`id_codigo`) REFERENCES `codigos_esquelas` (`id_codigo`);

CREATE INDEX `rol_historial_index_0` ON `rol_historial` (`id_usuario`);

CREATE INDEX `rol_historial_index_1` ON `rol_historial` (`id_rol`);

CREATE INDEX `rol_historial_index_2` ON `rol_historial` (`created_at`);

CREATE INDEX `bitacora_index_3` ON `bitacora` (`id_usuario_admin`);

CREATE INDEX `bitacora_index_4` ON `bitacora` (`fecha_hora`);

CREATE INDEX `bitacora_index_5` ON `bitacora` (`tipo_objetivo`);

CREATE UNIQUE INDEX `apoderados_index_6` ON `apoderados` (`ci`);

CREATE INDEX `solicitudes_retiro_index_7` ON `solicitudes_retiro` (`id_estudiante`);

CREATE INDEX `solicitudes_retiro_index_8` ON `solicitudes_retiro` (`id_apoderado`);

CREATE INDEX `solicitudes_retiro_index_9` ON `solicitudes_retiro` (`fecha_hora_salida`);

CREATE UNIQUE INDEX `solicitudes_retiro_detalle_index_10` ON `solicitudes_retiro_detalle` (`id_solicitud`, `id_curso`, `id_materia`);

CREATE UNIQUE INDEX `registros_salida_index_11` ON `registros_salida` (`id_solicitud`);

CREATE INDEX `registros_salida_index_12` ON `registros_salida` (`id_estudiante`);

CREATE INDEX `derivaciones_index_13` ON `derivaciones` (`id_incidente`);

CREATE INDEX `derivaciones_index_14` ON `derivaciones` (`fecha_derivacion`);

CREATE INDEX `historial_modificaciones_index_15` ON `historial_modificaciones` (`id_incidente`);

CREATE INDEX `historial_modificaciones_index_16` ON `historial_modificaciones` (`fecha_cambio`);

CREATE INDEX `adjuntos_index_17` ON `adjuntos` (`id_incidente`);

CREATE INDEX `adjuntos_index_18` ON `adjuntos` (`fecha_subida`);

ALTER TABLE `rol_historial` COMMENT = 'Tabla nueva. Registra cada vez que se asigna o revoca un rol a un usuario, con trazabilidad completa.';

ALTER TABLE `bitacora` COMMENT = 'Tabla nueva. Auditoría general del sistema. Registra acciones administrativas sobre cualquier entidad.';

ALTER TABLE `apoderados` COMMENT = 'Tabla nueva para gestionar apoderados de forma normalizada. Reemplaza los campos nombre_padre/madre en estudiantes.';

ALTER TABLE `estudiantes_apoderados` COMMENT = 'Tabla nueva. Permite que un estudiante tenga múltiples apoderados y que un apoderado tenga múltiples hijos.';

ALTER TABLE `motivos_retiro` COMMENT = 'Tabla nueva. Catálogo de motivos de retiro con niveles de severidad.';

ALTER TABLE `autorizaciones_retiro` COMMENT = 'Tabla nueva. Registra quién autorizó o rechazó cada solicitud de retiro.';

ALTER TABLE `solicitudes_retiro` COMMENT = 'Tabla nueva. Sistema mejorado de solicitudes de retiro con apoderados y autorizaciones.';

ALTER TABLE `solicitudes_retiro_detalle` COMMENT = 'Tabla nueva. Registra qué cursos y materias se verán afectados por el retiro.';

ALTER TABLE `registros_salida` COMMENT = 'Tabla nueva. Registra la hora real de salida y retorno del estudiante.';

ALTER TABLE `incidentes` COMMENT = 'Se agregó id_estado_catalogo para usar el catálogo de estados. El campo "estado" ENUM se mantiene por compatibilidad.';

ALTER TABLE `estados_incidente` COMMENT = 'Tabla nueva. Catálogo de estados de incidentes más flexible que el ENUM.';

ALTER TABLE `derivaciones` COMMENT = 'Tabla nueva. Registra el historial de derivaciones de incidentes entre personal.';

ALTER TABLE `historial_modificaciones` COMMENT = 'Tabla nueva. Auditoría de cambios realizados en los incidentes.';

ALTER TABLE `adjuntos` COMMENT = 'Tabla nueva. Gestión de archivos adjuntos a incidentes (documentos, imágenes, etc.).';

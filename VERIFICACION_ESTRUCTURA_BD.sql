-- ============================================================
-- QUERY PARA VERIFICAR ESTRUCTURA DE TABLAS - RETIROS TEMPRANOS
-- ============================================================

-- 1. Verificar estructura de solicitudes_retiro
DESCRIBE solicitudes_retiro;

-- 2. Verificar estructura de solicitudes_retiro_masivo
DESCRIBE solicitudes_retiro_masivo;

-- 3. Verificar estructura de autorizaciones_retiro
DESCRIBE autorizaciones_retiro;

-- 4. Verificar estructura de registros_salida
DESCRIBE registros_salida;

-- 5. Verificar estructura de estudiantes_apoderados
DESCRIBE estudiantes_apoderados;

-- 6. Verificar estructura de motivos_retiro
DESCRIBE motivos_retiro;

-- ============================================================
-- DATOS DE PRUEBA PARA VERIFICAR
-- ============================================================

-- Ver motivos disponibles
SELECT * FROM motivos_retiro WHERE es_activo = 1;

-- Ver relaciones estudiante-apoderado del apoderado 18
SELECT 
    ea.id_estudiante,
    ea.id_apoderado,
    ea.parentesco,
    ea.es_contacto_principal,
    e.nombre,
    e.apellido
FROM estudiantes_apoderados ea
JOIN estudiantes e ON e.id_estudiante = ea.id_estudiante
WHERE ea.id_apoderado = 18;

-- Ver datos del apoderado 18
SELECT 
    a.id_apoderado,
    a.id_persona,
    p.ci,
    p.nombres,
    p.apellidos
FROM apoderados a
JOIN personas p ON p.id_persona = a.id_persona
WHERE a.id_apoderado = 18;

-- Ver si hay solicitudes existentes
SELECT 
    s.id_solicitud,
    s.id_estudiante,
    s.id_apoderado,
    s.estado,
    s.fecha_creacion,
    s.tipo_solicitud
FROM solicitudes_retiro s
ORDER BY s.id_solicitud DESC
LIMIT 10;

-- ============================================================
-- ESTRUCTURA ESPERADA SEGÚN LA BD REAL
-- ============================================================

/*
TABLA: solicitudes_retiro
- id_solicitud (PK, auto_increment)
- id_estudiante (FK -> estudiantes.id_estudiante)
- id_apoderado (FK -> apoderados.id_apoderado)
- id_motivo (FK -> motivos_retiro.id_motivo)
- id_autorizacion (FK -> autorizaciones_retiro.id_autorizacion, nullable)
- fecha_hora_salida (datetime, NOT NULL)
- fecha_hora_retorno_previsto (datetime, nullable)
- observacion (text, nullable)
- tipo_solicitud (enum: 'individual', 'masiva', default 'individual')
- foto_evidencia (varchar(500), nullable)
- id_solicitante (FK -> usuarios.id_usuario, nullable)
- fecha_creacion (datetime, NOT NULL) *** NO fecha_hora_solicitud ***
- estado (enum: 'recibida','derivada','aprobada','rechazada','cancelada')
- id_recepcionista (FK -> usuarios.id_usuario, nullable)
- fecha_recepcion (datetime, nullable)
- id_regente (FK -> usuarios.id_usuario, nullable)
- fecha_derivacion (datetime, nullable)

TABLA: solicitudes_retiro_masivo
- id_solicitud_masiva (PK, auto_increment)
- id_solicitante (FK -> usuarios.id_usuario)
- id_motivo (FK -> motivos_retiro.id_motivo)
- fecha_hora_salida (datetime)
- fecha_hora_retorno_previsto (datetime, nullable)
- observacion (text, nullable)
- foto_evidencia (varchar(500), nullable)
- fecha_creacion (datetime)
- estado (enum: 'recibida','derivada','aprobada','rechazada','cancelada')
- id_recepcionista (FK -> usuarios.id_usuario, nullable)
- fecha_recepcion (datetime, nullable)
- id_regente (FK -> usuarios.id_usuario, nullable)
- fecha_derivacion (datetime, nullable)
- id_autorizacion (FK -> autorizaciones_retiro.id_autorizacion, nullable)

TABLA: autorizaciones_retiro
- id_autorizacion (PK, auto_increment)
- id_usuario_aprobador (FK -> usuarios.id_usuario) - Quien aprueba/rechaza
- decision (enum: 'aprobado','rechazado','pendiente')
- motivo_decision (varchar(255), nullable)
- fecha_decision (datetime)

TABLA: registros_salida
- id_registro (PK, auto_increment)
- id_solicitud (FK -> solicitudes_retiro.id_solicitud, nullable)
- id_estudiante (FK -> estudiantes.id_estudiante)
- tipo_registro (enum: 'individual','masivo')
- id_solicitud_masiva (FK -> solicitudes_retiro_masivo.id_solicitud_masiva, nullable)
- fecha_hora_salida_real (datetime)
- fecha_hora_retorno_real (datetime, nullable)
*/

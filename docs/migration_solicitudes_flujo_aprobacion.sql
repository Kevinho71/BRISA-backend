-- =====================================================
-- MIGRACIÓN: Mejora del Flujo de Aprobación de Solicitudes
-- Fecha: 2025-11-11
-- Descripción: Agrega estados, trazabilidad y relación 1:1 con autorizaciones
-- =====================================================

-- 1. Agregar columna de estado a solicitudes_retiro
ALTER TABLE `solicitudes_retiro` 
ADD COLUMN `estado` ENUM(
    'pendiente_recepcion',
    'recibida', 
    'derivada',
    'en_revision',
    'aprobada',
    'rechazada',
    'cancelada'
) NOT NULL DEFAULT 'pendiente_recepcion' 
COMMENT 'Estado actual en el flujo de aprobación'
AFTER `fecha_creacion`;

-- 2. Agregar columna para el recepcionista que recibe
ALTER TABLE `solicitudes_retiro` 
ADD COLUMN `recibido_por` INT NULL 
COMMENT 'ID de la persona (recepcionista) que recibió la solicitud'
AFTER `estado`;

-- 3. Agregar fecha de recepción
ALTER TABLE `solicitudes_retiro` 
ADD COLUMN `fecha_recepcion` DATETIME NULL 
COMMENT 'Fecha y hora en que el recepcionista recibió la solicitud'
AFTER `recibido_por`;

-- 4. Agregar columna para el regente al que se deriva
ALTER TABLE `solicitudes_retiro` 
ADD COLUMN `derivado_a` INT NULL 
COMMENT 'ID de la persona (regente) a quien se derivó la solicitud'
AFTER `fecha_recepcion`;

-- 5. Agregar fecha de derivación
ALTER TABLE `solicitudes_retiro` 
ADD COLUMN `fecha_derivacion` DATETIME NULL 
COMMENT 'Fecha y hora en que se derivó al regente'
AFTER `derivado_a`;

-- 6. Agregar restricción UNIQUE a id_autorizacion para relación 1:1
ALTER TABLE `solicitudes_retiro` 
ADD UNIQUE KEY `unique_autorizacion` (`id_autorizacion`);

-- 7. Agregar foreign keys para recibido_por y derivado_a
ALTER TABLE `solicitudes_retiro` 
ADD CONSTRAINT `fk_solicitud_recibido_por` 
    FOREIGN KEY (`recibido_por`) 
    REFERENCES `personas` (`id_persona`) 
    ON DELETE SET NULL;

ALTER TABLE `solicitudes_retiro` 
ADD CONSTRAINT `fk_solicitud_derivado_a` 
    FOREIGN KEY (`derivado_a`) 
    REFERENCES `personas` (`id_persona`) 
    ON DELETE SET NULL;

-- 8. Crear índices para optimizar consultas por estado
CREATE INDEX `idx_solicitudes_estado` ON `solicitudes_retiro` (`estado`);
CREATE INDEX `idx_solicitudes_recibido_por` ON `solicitudes_retiro` (`recibido_por`);
CREATE INDEX `idx_solicitudes_derivado_a` ON `solicitudes_retiro` (`derivado_a`);

-- 9. Actualizar solicitudes existentes al nuevo estado (si existen)
-- Si tienen autorización aprobada -> aprobada
UPDATE `solicitudes_retiro` sr
INNER JOIN `autorizaciones_retiro` ar ON sr.id_autorizacion = ar.id_autorizacion
SET sr.estado = 'aprobada'
WHERE ar.decision = 'aprobado';

-- Si tienen autorización rechazada -> rechazada
UPDATE `solicitudes_retiro` sr
INNER JOIN `autorizaciones_retiro` ar ON sr.id_autorizacion = ar.id_autorizacion
SET sr.estado = 'rechazada'
WHERE ar.decision = 'rechazado';

-- Si tienen autorización pendiente -> en_revision
UPDATE `solicitudes_retiro` sr
INNER JOIN `autorizaciones_retiro` ar ON sr.id_autorizacion = ar.id_autorizacion
SET sr.estado = 'en_revision'
WHERE ar.decision = 'pendiente';

-- =====================================================
-- VERIFICACIÓN
-- =====================================================

-- Verificar la estructura actualizada
DESCRIBE `solicitudes_retiro`;

-- Ver las solicitudes con sus estados
SELECT 
    sr.id_solicitud,
    sr.estado,
    sr.recibido_por,
    sr.fecha_recepcion,
    sr.derivado_a,
    sr.fecha_derivacion,
    ar.decision as decision_autorizacion
FROM `solicitudes_retiro` sr
LEFT JOIN `autorizaciones_retiro` ar ON sr.id_autorizacion = ar.id_autorizacion
ORDER BY sr.id_solicitud;

-- =====================================================
-- ROLLBACK (en caso de necesitar revertir)
-- =====================================================
/*
ALTER TABLE `solicitudes_retiro` 
DROP FOREIGN KEY `fk_solicitud_recibido_por`,
DROP FOREIGN KEY `fk_solicitud_derivado_a`,
DROP INDEX `unique_autorizacion`,
DROP INDEX `idx_solicitudes_estado`,
DROP INDEX `idx_solicitudes_recibido_por`,
DROP INDEX `idx_solicitudes_derivado_a`,
DROP COLUMN `estado`,
DROP COLUMN `recibido_por`,
DROP COLUMN `fecha_recepcion`,
DROP COLUMN `derivado_a`,
DROP COLUMN `fecha_derivacion`;
*/

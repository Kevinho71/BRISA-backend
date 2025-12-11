-- ============================================================================
-- SCRIPT DE MIGRACION - MODULO RETIROS TEMPRANOS
-- Fecha: 2025-12-10
-- Descripción: Adaptación del módulo de retiros tempranos para soportar
--              solicitudes individuales y masivas con foto evidencia obligatoria
-- ============================================================================

USE brisa;

-- ============================================================================
-- PASO 1: ELIMINAR TABLA OBSOLETA
-- ============================================================================

-- Eliminar tabla de detalles de solicitud individual (ya no se usa)
DROP TABLE IF EXISTS `solicitudes_retiro_detalle`;

-- ============================================================================
-- PASO 2: MODIFICAR TABLA SOLICITUDES_RETIRO (Individual)
-- ============================================================================

-- Agregar nuevas columnas a solicitudes_retiro
ALTER TABLE `solicitudes_retiro`
    ADD COLUMN `tipo_solicitud` ENUM('individual', 'masiva') NOT NULL DEFAULT 'individual' COMMENT 'Tipo de solicitud' AFTER `id_autorizacion`,
    ADD COLUMN `foto_evidencia` VARCHAR(500) NOT NULL COMMENT 'URL de foto evidencia obligatoria' AFTER `tipo_solicitud`,
    ADD COLUMN `id_solicitante` INT UNSIGNED NULL COMMENT 'Usuario que crea la solicitud' AFTER `foto_evidencia`,
    ADD INDEX `idx_tipo_solicitud` (`tipo_solicitud`),
    ADD INDEX `idx_solicitante` (`id_solicitante`);

-- Cambiar nombre de columna fecha_creacion a fecha_hora_solicitud (opcional, solo si no coincide)
-- Si ya existe fecha_hora_solicitud, omitir este paso
ALTER TABLE `solicitudes_retiro`
    CHANGE COLUMN `fecha_creacion` `fecha_hora_solicitud` DATETIME NOT NULL COMMENT 'Fecha y hora de creación';

-- Cambiar estado default de 'recibida' a 'pendiente'
ALTER TABLE `solicitudes_retiro`
    MODIFY COLUMN `estado` ENUM('pendiente', 'recibida', 'derivada', 'aprobada', 'rechazada', 'cancelada') NOT NULL DEFAULT 'pendiente';

-- Agregar relación con usuarios (solicitante)
ALTER TABLE `solicitudes_retiro`
    ADD CONSTRAINT `fk_solicitud_solicitante` FOREIGN KEY (`id_solicitante`) REFERENCES `usuarios`(`id_usuario`) ON DELETE SET NULL;

-- ============================================================================
-- PASO 3: CREAR TABLA SOLICITUDES_RETIRO_MASIVO
-- ============================================================================

CREATE TABLE IF NOT EXISTS `solicitudes_retiro_masivo` (
    `id_solicitud_masiva` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'ID único de solicitud masiva',
    `id_solicitante` INT UNSIGNED NOT NULL COMMENT 'Usuario que crea la solicitud (profesor/admin)',
    `id_motivo` INT UNSIGNED NOT NULL COMMENT 'Motivo del retiro',
    `id_autorizacion` INT UNSIGNED NULL UNIQUE COMMENT 'Autorización del regente',
    
    `fecha_hora_salida` DATETIME NOT NULL COMMENT 'Fecha y hora prevista de salida',
    `fecha_hora_retorno` DATETIME NULL COMMENT 'Fecha y hora prevista de retorno',
    `foto_evidencia` VARCHAR(500) NOT NULL COMMENT 'URL de foto evidencia obligatoria',
    `observacion` TEXT NULL COMMENT 'Observaciones generales',
    `fecha_hora_solicitud` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creación',
    
    `estado` ENUM('pendiente', 'recibida', 'derivada', 'aprobada', 'rechazada', 'cancelada') NOT NULL DEFAULT 'pendiente' COMMENT 'Estado de la solicitud',
    `id_recepcionista` INT UNSIGNED NULL COMMENT 'Recepcionista que recibe',
    `fecha_recepcion` DATETIME NULL COMMENT 'Fecha de recepción',
    `id_regente` INT UNSIGNED NULL COMMENT 'Regente asignado',
    `fecha_derivacion` DATETIME NULL COMMENT 'Fecha de derivación',
    
    INDEX `idx_solicitante` (`id_solicitante`),
    INDEX `idx_estado` (`estado`),
    INDEX `idx_fecha_salida` (`fecha_hora_salida`),
    INDEX `idx_recepcionista` (`id_recepcionista`),
    INDEX `idx_regente` (`id_regente`),
    
    CONSTRAINT `fk_solicitud_masiva_solicitante` FOREIGN KEY (`id_solicitante`) REFERENCES `usuarios`(`id_usuario`) ON DELETE SET NULL,
    CONSTRAINT `fk_solicitud_masiva_motivo` FOREIGN KEY (`id_motivo`) REFERENCES `motivos_retiro`(`id_motivo`) ON DELETE SET NULL,
    CONSTRAINT `fk_solicitud_masiva_autorizacion` FOREIGN KEY (`id_autorizacion`) REFERENCES `autorizaciones_retiro`(`id_autorizacion`) ON DELETE SET NULL,
    CONSTRAINT `fk_solicitud_masiva_recepcionista` FOREIGN KEY (`id_recepcionista`) REFERENCES `usuarios`(`id_usuario`) ON DELETE SET NULL,
    CONSTRAINT `fk_solicitud_masiva_regente` FOREIGN KEY (`id_regente`) REFERENCES `usuarios`(`id_usuario`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Solicitudes de retiro masivo (paseos, excursiones)';

-- ============================================================================
-- PASO 4: CREAR TABLA DETALLE_SOLICITUDES_RETIRO_MASIVO
-- ============================================================================

CREATE TABLE IF NOT EXISTS `detalle_solicitudes_retiro_masivo` (
    `id_detalle` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'ID único del detalle',
    `id_solicitud_masiva` INT UNSIGNED NOT NULL COMMENT 'Solicitud masiva padre',
    `id_estudiante` INT UNSIGNED NOT NULL COMMENT 'Estudiante incluido',
    `observacion_individual` TEXT NULL COMMENT 'Observación específica para este estudiante',
    
    INDEX `idx_solicitud_masiva` (`id_solicitud_masiva`),
    INDEX `idx_estudiante` (`id_estudiante`),
    
    CONSTRAINT `fk_detalle_masivo_solicitud` FOREIGN KEY (`id_solicitud_masiva`) REFERENCES `solicitudes_retiro_masivo`(`id_solicitud_masiva`) ON DELETE CASCADE,
    CONSTRAINT `fk_detalle_masivo_estudiante` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes`(`id_estudiante`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Detalles de solicitudes masivas (lista de estudiantes)';

-- ============================================================================
-- PASO 5: MODIFICAR TABLA REGISTROS_SALIDA
-- ============================================================================

-- Hacer id_solicitud nullable (puede ser NULL si es registro masivo)
ALTER TABLE `registros_salida`
    MODIFY COLUMN `id_solicitud` INT UNSIGNED NULL COMMENT 'ID de solicitud individual (NULL si es masivo)';

-- Agregar nuevas columnas para registros masivos
ALTER TABLE `registros_salida`
    ADD COLUMN `tipo_registro` ENUM('individual', 'masivo') NOT NULL DEFAULT 'individual' COMMENT 'Tipo de registro' AFTER `id_estudiante`,
    ADD COLUMN `id_solicitud_masiva` INT UNSIGNED NULL COMMENT 'ID de solicitud masiva (NULL si es individual)' AFTER `tipo_registro`,
    ADD INDEX `idx_tipo_registro` (`tipo_registro`),
    ADD INDEX `idx_solicitud_masiva` (`id_solicitud_masiva`);

-- Agregar relación con solicitudes masivas
ALTER TABLE `registros_salida`
    ADD CONSTRAINT `fk_registro_solicitud_masiva` FOREIGN KEY (`id_solicitud_masiva`) REFERENCES `solicitudes_retiro_masivo`(`id_solicitud_masiva`) ON DELETE CASCADE;

-- ============================================================================
-- PASO 6: ACTUALIZAR TABLA AUTORIZACIONES_RETIRO
-- ============================================================================

-- Agregar relación con solicitudes masivas
ALTER TABLE `autorizaciones_retiro`
    ADD COLUMN `id_solicitud_masiva` INT UNSIGNED NULL COMMENT 'Solicitud masiva autorizada' AFTER `id_solicitud`,
    ADD UNIQUE INDEX `uq_solicitud_masiva` (`id_solicitud_masiva`);

-- Hacer id_solicitud nullable (una autorización puede ser para individual O masiva, no ambas)
ALTER TABLE `autorizaciones_retiro`
    MODIFY COLUMN `id_solicitud` INT UNSIGNED NULL COMMENT 'Solicitud individual autorizada';

-- Agregar constraint
ALTER TABLE `autorizaciones_retiro`
    ADD CONSTRAINT `fk_autorizacion_solicitud_masiva` FOREIGN KEY (`id_solicitud_masiva`) REFERENCES `solicitudes_retiro_masivo`(`id_solicitud_masiva`) ON DELETE CASCADE;

-- ============================================================================
-- PASO 7: ACTUALIZAR DATOS EXISTENTES (si hay)
-- ============================================================================

-- Actualizar solicitudes existentes para agregar tipo y foto por defecto
UPDATE `solicitudes_retiro`
SET 
    `tipo_solicitud` = 'individual',
    `foto_evidencia` = 'placeholder.jpg',  -- CAMBIAR manualmente después
    `id_solicitante` = `id_apoderado`
WHERE `foto_evidencia` IS NULL OR `foto_evidencia` = '';

-- Actualizar registros existentes con tipo
UPDATE `registros_salida`
SET `tipo_registro` = 'individual'
WHERE `tipo_registro` IS NULL;

-- ============================================================================
-- PASO 8: VERIFICACIÓN
-- ============================================================================

-- Verificar estructura de solicitudes_retiro
DESCRIBE `solicitudes_retiro`;

-- Verificar estructura de solicitudes_retiro_masivo
DESCRIBE `solicitudes_retiro_masivo`;

-- Verificar estructura de detalle_solicitudes_retiro_masivo
DESCRIBE `detalle_solicitudes_retiro_masivo`;

-- Verificar estructura de registros_salida
DESCRIBE `registros_salida`;

-- Verificar estructura de autorizaciones_retiro
DESCRIBE `autorizaciones_retiro`;

-- ============================================================================
-- NOTAS IMPORTANTES:
-- ============================================================================
-- 1. Las solicitudes individuales requieren foto_evidencia OBLIGATORIA
-- 2. Las solicitudes masivas también requieren foto_evidencia OBLIGATORIA
-- 3. El estado inicial de TODAS las solicitudes es 'pendiente'
-- 4. Los registros de salida pueden ser individuales o masivos
-- 5. Una autorización puede ser para solicitud individual O masiva (no ambas)
-- ============================================================================

SELECT 'MIGRACIÓN COMPLETADA EXITOSAMENTE' AS Resultado;

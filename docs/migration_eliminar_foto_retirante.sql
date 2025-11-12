-- =====================================================
-- MIGRACIÓN: Eliminar columna foto_retirante_url
-- Fecha: 2025-11-12
-- Descripción: Elimina el campo foto_retirante_url de la tabla solicitudes_retiro
-- =====================================================

-- IMPORTANTE: Hacer backup antes de ejecutar
-- mysqldump -u avnadmin -p defaultdb solicitudes_retiro > backup_solicitudes_retiro_$(date +%Y%m%d_%H%M%S).sql

-- Eliminar columna foto_retirante_url
ALTER TABLE `solicitudes_retiro` 
DROP COLUMN `foto_retirante_url`;

-- =====================================================
-- VERIFICACIÓN
-- =====================================================

-- Verificar que la columna fue eliminada
DESCRIBE `solicitudes_retiro`;

-- Ver estructura actualizada
SHOW CREATE TABLE `solicitudes_retiro`;

-- =====================================================
-- ROLLBACK (en caso de necesitar revertir)
-- =====================================================
/*
-- ADVERTENCIA: Esto agregará la columna de nuevo pero sin los datos anteriores

ALTER TABLE `solicitudes_retiro` 
ADD COLUMN `foto_retirante_url` VARCHAR(300) NULL 
COMMENT 'URL de la foto del retirante'
AFTER `observacion`;
*/

-- =====================================================
-- NOTAS
-- =====================================================
/*
CAMBIO REALIZADO:
- Eliminada columna: foto_retirante_url VARCHAR(300)
- Razón: Campo no necesario para el flujo de retiros

IMPACTO:
- Se pierde permanentemente la información de fotos si existiera
- Los DTOs, Service y Model ya fueron actualizados
- La aplicación funcionará sin errores después de esta migración
*/

-- =====================================================
-- MIGRACIÓN: Simplificación del Flujo de Aprobación
-- Fecha: 2025-11-12
-- Descripción: Elimina estado 'en_revision' y 'pendiente_recepcion', ajusta flujo a 5 estados
-- =====================================================

-- IMPORTANTE: Hacer backup antes de ejecutar
-- mysqldump -u avnadmin -p defaultdb > backup_$(date +%Y%m%d_%H%M%S).sql

-- 1. Actualizar solicitudes existentes que estén en estados que se eliminarán
-- Convertir 'pendiente_recepcion' → 'recibida'
UPDATE `solicitudes_retiro` 
SET `estado` = 'recibida' 
WHERE `estado` = 'pendiente_recepcion';

-- Convertir 'en_revision' → 'derivada'
UPDATE `solicitudes_retiro` 
SET `estado` = 'derivada' 
WHERE `estado` = 'en_revision';

-- 2. Modificar el ENUM para eliminar los estados innecesarios
ALTER TABLE `solicitudes_retiro` 
MODIFY COLUMN `estado` ENUM(
    'recibida',
    'derivada',
    'aprobada',
    'rechazada',
    'cancelada'
) NOT NULL DEFAULT 'recibida' 
COMMENT 'Estado actual en el flujo de aprobación simplificado';

-- 3. Actualizar solicitudes que no tengan recibido_por (marcar con recepcionista fijo ID=1)
UPDATE `solicitudes_retiro` 
SET `recibido_por` = 1,
    `fecha_recepcion` = COALESCE(`fecha_recepcion`, `fecha_creacion`)
WHERE `recibido_por` IS NULL;

-- 4. Actualizar autorizaciones que no tengan decidido_por (marcar con regente fijo ID=2)
UPDATE `autorizaciones_retiro` 
SET `decidido_por` = 2
WHERE `decidido_por` IS NULL OR `decidido_por` != 2;

-- =====================================================
-- VERIFICACIÓN
-- =====================================================

-- Ver distribución de estados después del cambio
SELECT 
    estado,
    COUNT(*) as total,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM solicitudes_retiro), 2) as porcentaje
FROM `solicitudes_retiro`
GROUP BY estado
ORDER BY total DESC;

-- Verificar que todas las solicitudes tengan recibido_por
SELECT COUNT(*) as solicitudes_sin_recepcionista
FROM `solicitudes_retiro`
WHERE `recibido_por` IS NULL;

-- Verificar que todas las autorizaciones tengan decidido_por = 2
SELECT COUNT(*) as autorizaciones_sin_regente_correcto
FROM `autorizaciones_retiro`
WHERE `decidido_por` IS NULL OR `decidido_por` != 2;

-- Ver estructura actualizada
DESCRIBE `solicitudes_retiro`;

-- =====================================================
-- ROLLBACK (en caso de necesitar revertir)
-- =====================================================
/*
-- ADVERTENCIA: Este rollback NO recuperará los estados originales 
-- de 'pendiente_recepcion' y 'en_revision', solo restaura el ENUM

ALTER TABLE `solicitudes_retiro` 
MODIFY COLUMN `estado` ENUM(
    'pendiente_recepcion',
    'recibida',
    'derivada',
    'en_revision',
    'aprobada',
    'rechazada',
    'cancelada'
) NOT NULL DEFAULT 'pendiente_recepcion' 
COMMENT 'Estado actual en el flujo de aprobación';
*/

-- =====================================================
-- NOTAS
-- =====================================================
/*
CAMBIOS REALIZADOS:
1. Estados eliminados: 'pendiente_recepcion', 'en_revision'
2. Estados finales: recibida, derivada, aprobada, rechazada, cancelada
3. Estado inicial: 'recibida' (automático al crear)
4. recibido_por: Siempre ID=1 (recepcionista fijo)
5. derivado_a: Siempre ID=2 (regente fijo)
6. decidido_por: Siempre ID=2 (regente fijo)

FLUJO SIMPLIFICADO:
Crear → recibida (auto) → derivar → derivada → aprobar/rechazar → aprobada/rechazada
*/

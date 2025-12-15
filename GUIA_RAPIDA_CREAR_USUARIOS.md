# 🚀 Guía Rápida: Crear 3 Usuarios para Retiros Tempranos

## 📌 Resumen

Crearemos 3 usuarios usando:
1. **SQL** → Crear personas y sus relaciones
2. **POST /api/auth/usuarios** → Crear usuarios (genera contraseña automática)
3. **POST /api/auth/usuarios/{id}/roles/{id}** → Asignar roles
4. **POST /api/auth/login** → Probar acceso

---

## 🔐 Token Director

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMSIsInVzdWFyaW9faWQiOjIxLCJ1c3VhcmlvIjoiYWZlcm5hbmRleiIsImV4cCI6MTc2NTgxMzM1Mn0.WEEe2lj6PUsT01oafnhifpUtz1f-oSLwFpbwAcSJK4w
```

---

## 📝 PASO 1: Ejecutar SQL para Crear Personas

Ejecuta este script en tu gestor de base de datos:

```sql
-- ============================================================================
-- 1. CREAR RECEPCIONISTA
-- ============================================================================

-- Persona
INSERT INTO personas (ci, nombres, apellido_paterno, apellido_materno, telefono, correo, direccion, tipo_persona, is_active)
VALUES ('9876543', 'María', 'López', 'Rojas', '79812345', 'mlopez@colegio.edu.bo', 'Av. Siempre Viva 742', 'administrativo', 1);

SET @id_persona_recep = LAST_INSERT_ID();

-- Administrativo (cargo: Recepcionista id=6)
INSERT INTO administrativos (id_persona, id_cargo, horario_entrada, horario_salida, area_trabajo, observaciones)
VALUES (@id_persona_recep, 6, '07:30:00', '15:30:00', 'Recepción', 'Recepcionista turno mañana');

SELECT @id_persona_recep AS id_persona_recepcionista;

-- ============================================================================
-- 2. CREAR REGENTE
-- ============================================================================

-- Persona
INSERT INTO personas (ci, nombres, apellido_paterno, apellido_materno, telefono, correo, direccion, tipo_persona, is_active)
VALUES ('8765432', 'Carlos', 'Mendoza', 'Silva', '79823456', 'cmendoza@colegio.edu.bo', 'Calle Los Pinos 456', 'administrativo', 1);

SET @id_persona_regente = LAST_INSERT_ID();

-- Administrativo (cargo: Regente id=2)
INSERT INTO administrativos (id_persona, id_cargo, horario_entrada, horario_salida, area_trabajo, observaciones)
VALUES (@id_persona_regente, 2, '08:00:00', '16:00:00', 'Regencia', 'Regente académico');

SELECT @id_persona_regente AS id_persona_regente;

-- ============================================================================
-- 3. CREAR APODERADO
-- ============================================================================

-- Persona
INSERT INTO personas (ci, nombres, apellido_paterno, apellido_materno, telefono, correo, direccion, tipo_persona, is_active)
VALUES ('7654321', 'Ana', 'García', 'Morales', '79834567', 'agarcia@gmail.com', 'Zona Norte 789', 'apoderado', 1);

SET @id_persona_apod = LAST_INSERT_ID();

-- Apoderado
INSERT INTO apoderados (id_persona, ci, nombres, apellidos, telefono, correo, direccion)
VALUES (@id_persona_apod, '7654321', 'Ana', 'García Morales', '79834567', 'agarcia@gmail.com', 'Zona Norte 789');

SET @id_apoderado = LAST_INSERT_ID();

-- Asociar con estudiante (cambiar id_estudiante según tu BD)
INSERT INTO estudiantes_apoderados (id_estudiante, id_apoderado, parentesco, es_contacto_principal)
VALUES (1, @id_apoderado, 'Madre', 1);

SELECT @id_persona_apod AS id_persona_apoderado, @id_apoderado AS id_apoderado;

-- ============================================================================
-- CONSULTAR IDs CREADOS
-- ============================================================================

SELECT 
    p.id_persona,
    p.ci,
    p.nombres,
    p.apellido_paterno,
    p.tipo_persona,
    CASE 
        WHEN a.id_administrativo IS NOT NULL THEN CONCAT('Cargo: ', c.nombre_cargo)
        WHEN ap.id_apoderado IS NOT NULL THEN CONCAT('Apoderado ID: ', ap.id_apoderado)
        ELSE 'Sin relación'
    END AS info_adicional
FROM personas p
LEFT JOIN administrativos a ON p.id_persona = a.id_persona
LEFT JOIN cargos c ON a.id_cargo = c.id_cargo
LEFT JOIN apoderados ap ON p.id_persona = ap.id_persona
WHERE p.ci IN ('9876543', '8765432', '7654321')
ORDER BY p.id_persona;
```

**📋 Guarda los 3 `id_persona` que aparecen en los resultados:**
- Recepcionista: `id_persona = ___`
- Regente: `id_persona = ___`
- Apoderado: `id_persona = ___`

---

## 📝 PASO 2: Crear Usuarios con POST /api/auth/usuarios

### 2.1 Crear Usuario para Recepcionista

**POST** `http://localhost:8000/api/auth/usuarios`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Body:**
```json
{
  "id_persona": 31,
  "usuario": "mlopez",
  "correo": "mlopez@colegio.edu.bo"
}
```

**Respuesta:**
```json
{
  "status": "success",
  "data": {
    "usuario": {
      "id_usuario": 48,
      "usuario": "mlopez"
    },
    "password_temporal": "aB3$xY9!mQ2#"
  }
}
```

✅ **Guardar:** `id_usuario` y `password_temporal`

---

### 2.2 Crear Usuario para Regente

**POST** `http://localhost:8000/api/auth/usuarios`

**Body:**
```json
{
  "id_persona": 32,
  "usuario": "cmendoza",
  "correo": "cmendoza@colegio.edu.bo"
}
```

✅ **Guardar:** `id_usuario` y `password_temporal`

---

### 2.3 Crear Usuario para Apoderado

**POST** `http://localhost:8000/api/auth/usuarios`

**Body:**
```json
{
  "id_persona": 33,
  "usuario": "agarcia",
  "correo": "agarcia@gmail.com"
}
```

✅ **Guardar:** `id_usuario` y `password_temporal`

---

## 📝 PASO 3: Asignar Roles

### 3.1 Asignar Rol "Recepción" (id=7)

**POST** `http://localhost:8000/api/auth/usuarios/48/roles/7`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Sin body** (solo la URL)

---

### 3.2 Asignar Rol "Regente" (id=3)

**POST** `http://localhost:8000/api/auth/usuarios/49/roles/3`

---

### 3.3 Asignar Rol "Apoderado" (id=8)

**POST** `http://localhost:8000/api/auth/usuarios/50/roles/8`

---

## 🧪 PASO 4: Probar Login

### Login Recepcionista

**POST** `http://localhost:8000/api/auth/login`

**Body:**
```json
{
  "usuario": "mlopez",
  "password": "aB3$xY9!mQ2#"
}
```

✅ **Guardar token** para usar endpoints de recepción

---

### Login Regente

**Body:**
```json
{
  "usuario": "cmendoza",
  "password": "pQ7#mN2!vB9$"
}
```

✅ **Guardar token** para aprobar solicitudes

---

### Login Apoderado

**Body:**
```json
{
  "usuario": "agarcia",
  "password": "xK9$mL2!nP8#"
}
```

✅ **Guardar token** para crear solicitudes

---

## 📊 Resumen de IDs

| Rol | id_rol | Cargo | id_cargo |
|-----|--------|-------|----------|
| Recepción | 7 | Recepcionista | 6 |
| Regente | 3 | Regente | 2 |
| Apoderado | 8 | - | - |

---

## 🎯 Flujo Completo de Retiros Tempranos

### 1. Apoderado crea solicitud

**POST** `/api/retiros-tempranos/solicitudes/`  
**Token:** Apoderado

```json
{
  "id_estudiante": 1,
  "motivo": "Cita médica",
  "fecha_retiro": "2025-12-16",
  "hora_retiro": "14:00:00",
  "foto_evidencia": "base64..."
}
```

---

### 2. Regente aprueba

**PUT** `/api/retiros-tempranos/solicitudes-masivas/1/aprobar`  
**Token:** Regente

```json
{
  "observaciones_regente": "Aprobado"
}
```

---

### 3. Recepcionista registra salida

**POST** `/api/retiros-tempranos/registros-salida/individual`  
**Token:** Recepcionista

```json
{
  "id_solicitud": 1,
  "fecha_hora_salida_real": "2025-12-16T14:05:00"
}
```

---

## ✅ Checklist

- [ ] SQL ejecutado correctamente
- [ ] 3 usuarios creados (con contraseñas guardadas)
- [ ] 3 roles asignados
- [ ] Login exitoso con los 3 usuarios
- [ ] Tokens guardados para cada rol
- [ ] Flujo completo probado

---

## 📝 Notas

- Las contraseñas se generan automáticamente y **solo se muestran una vez**
- Token expira en 3600 segundos (1 hora)
- Para cambiar contraseña: `POST /api/auth/cambiar-password`
- Verificar usuarios: `GET /api/auth/usuarios` (requiere token Director)

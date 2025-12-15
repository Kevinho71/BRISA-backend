    # 🧪 GUÍA DE PRUEBAS - MÓDULO RETIROS TEMPRANOS

## 📋 ÍNDICE
1. [Autenticación](#autenticación)
2. [Motivos de Retiro](#motivos-de-retiro)
3. [Solicitudes Individuales - APODERADO](#solicitudes-individuales---apoderado)
4. [Solicitudes Individuales - RECEPCIONISTA](#solicitudes-individuales---recepcionista)
5. [Solicitudes Individuales - REGENTE](#solicitudes-individuales---regente)
6. [Solicitudes Masivas - PROFESOR](#solicitudes-masivas---profesor)
7. [Solicitudes Masivas - RECEPCIONISTA](#solicitudes-masivas---recepcionista)
8. [Solicitudes Masivas - REGENTE](#solicitudes-masivas---regente)
9. [Registros de Salida - RECEPCIONISTA](#registros-de-salida---recepcionista)
10. [Flujo Completo de Prueba](#flujo-completo-de-prueba)

---

## 🔐 AUTENTICACIÓN

### 1. Login de Usuarios

**Endpoint:** `POST /api/auth/login`

**Body para Recepcionista:**
```json
{
  "usuario": "recepcionista.test",
  "password": "password123"
}
```

**Body para Regente:**
```json
{
  "usuario": "regente.test",
  "password": "password123"
}
```

**Body para Apoderado:**
```json
{
  "usuario": "apoderado.test",
  "password": "password123"
}
```

**Respuesta Esperada:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "usuario": {
    "id_usuario": 1,
    "usuario": "recepcionista.test",
    "email": "recepcion@test.com"
  }
}
```

**⚠️ IMPORTANTE:** Copia el `access_token` y úsalo en todas las peticiones siguientes como:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📝 MOTIVOS DE RETIRO

### 1. Crear Motivo de Retiro
**Endpoint:** `POST /api/motivos-retiro/`  
**Roles:** `admin`, `regente`  
**Header:** `Authorization: Bearer {token}`

**Body:**
```json
{
  "nombre": "Cita médica",
  "descripcion": "Retiro por consulta médica programada",
  "severidad": "leve",
  "activo": true
}
```

**Valores permitidos para `severidad`:**
- `"leve"`
- `"grave"`
- `"muy grave"`

**Ejemplos adicionales:**
```json
{
  "nombre": "Emergencia familiar",
  "descripcion": "Retiro por emergencia en el hogar",
  "severidad": "grave",
  "activo": true
}
```

```json
{
  "nombre": "Paseo educativo",
  "descripcion": "Excursión programada con fines educativos",
  "severidad": "leve",
  "activo": true
}
```

### 2. Listar Motivos Activos
**Endpoint:** `GET /api/motivos-retiro/activos`  
**Roles:** `admin`, `regente`, `recepcion`, `profesor`, `apoderado` (cualquier usuario autenticado)  
**Header:** `Authorization: Bearer {token}`

**No requiere body**

### 3. Listar Todos los Motivos
**Endpoint:** `GET /api/motivos-retiro/?skip=0&limit=100`  
**Roles:** `admin`, `regente`, `recepcion`, `profesor`, `apoderado` (cualquier usuario autenticado)  
**Header:** `Authorization: Bearer {token}`

**No requiere body**

### 4. Obtener Motivo por ID
**Endpoint:** `GET /api/motivos-retiro/{id_motivo}`  
**Roles:** `admin`, `regente`, `recepcion`, `profesor`, `apoderado` (cualquier usuario autenticado)  
**Header:** `Authorization: Bearer {token}`

**Ejemplo:** `GET /api/motivos-retiro/1`

### 5. Actualizar Motivo
**Endpoint:** `PUT /api/motivos-retiro/{id_motivo}`  
**Roles:** `admin`, `regente`  
**Header:** `Authorization: Bearer {token}`

**Body (todos los campos opcionales):**
```json
{
  "nombre": "Cita médica especializada",
  "descripcion": "Consulta con especialista",
  "severidad": "grave",
  "activo": true
}
```

### 6. Eliminar Motivo
**Endpoint:** `DELETE /api/motivos-retiro/{id_motivo}`  
**Roles:** `admin`  
**Header:** `Authorization: Bearer {token}`

**No requiere body**

---

## 👨‍👩‍👧 SOLICITUDES INDIVIDUALES - APODERADO

### 1. Crear Solicitud Individual
**Endpoint:** `POST /api/retiros-tempranos/solicitudes/`  
**Roles:** `apoderado`  
**Header:** `Authorization: Bearer {token_apoderado}`

**Body:**
```json
{
  "id_estudiante": 1,
  "id_motivo": 1,
  "fecha_hora_salida": "2025-12-15T14:30:00",
  "fecha_hora_retorno_previsto": "2025-12-15T16:00:00",
  "foto_evidencia": "https://ejemplo.com/fotos/evidencia123.jpg",
  "observacion": "El estudiante tiene cita médica de control"
}
```

**Campos requeridos:**
- ✅ `id_estudiante`: ID del estudiante (debe estar relacionado con el apoderado)
- ✅ `id_motivo`: ID del motivo de retiro (debe existir y estar activo)
- ✅ `fecha_hora_salida`: Fecha y hora en formato ISO 8601
- ✅ `foto_evidencia`: URL o path de la foto (OBLIGATORIA)

**Campos opcionales:**
- `fecha_hora_retorno_previsto`: Hora estimada de retorno
- `observacion`: Observaciones adicionales

### 2. Listar Mis Solicitudes
**Endpoint:** `GET /api/retiros-tempranos/solicitudes/mis-solicitudes?skip=0&limit=100`  
**Roles:** `apoderado`  
**Header:** `Authorization: Bearer {token_apoderado}`

**No requiere body**

### 3. Cancelar Solicitud Propia
**Endpoint:** `PUT /api/retiros-tempranos/solicitudes/{id_solicitud}/cancelar`  
**Roles:** `apoderado`  
**Header:** `Authorization: Bearer {token_apoderado}`

**Body:**
```json
{
  "motivo_cancelacion": "Ya no será necesario el retiro, se reprogramó la cita"
}
```

**⚠️ RESTRICCIÓN:** Solo se puede cancelar si la solicitud aún NO ha sido aprobada/rechazada.

### 4. Eliminar Solicitud Propia
**Endpoint:** `DELETE /api/retiros-tempranos/solicitudes/{id_solicitud}`  
**Roles:** `apodeado`  
**Header:** `Authorization: Bearer {token_apoderado}`

**No requiere body**

**⚠️ RESTRICCIÓN:** Solo se puede eliminar si está en estado `"pendiente"`.

---

## 🏢 SOLICITUDES INDIVIDUALES - RECEPCIONISTA

### 1. Listar Solicitudes Pendientes
**Endpoint:** `GET /api/retiros-tempranos/solicitudes/pendientes?skip=0&limit=100`  
**Roles:** `recepcion`  
**Header:** `Authorization: Bearer {token_recepcionista}`

**No requiere body**

**Retorna:** Solicitudes en estado `"pendiente"` (recién creadas por apoderados)

### 2. Listar Solicitudes Recibidas
**Endpoint:** `GET /api/retiros-tempranos/solicitudes/recibidas?skip=0&limit=100`  
**Roles:** `recepcion`  
**Header:** `Authorization: Bearer {token_recepcionista}`

**No requiere body**

**Retorna:** Solicitudes que ya fueron recibidas pero aún no derivadas

### 3. Recibir Solicitud
**Endpoint:** `PUT /api/retiros-tempranos/solicitudes/{id_solicitud}/recibir`  
**Roles:** `recepcion`  
**Header:** `Authorization: Bearer {token_recepcionista}`

**Body:**
```json
{
  "fecha_hora_recepcion": "2025-12-15T10:30:00"
}
```

**Campos opcionales:**
- `fecha_hora_recepcion`: Si no se envía, usa la fecha/hora actual

**Cambio de estado:** `"pendiente"` → `"recibida"`

### 4. Derivar Solicitud al Regente
**Endpoint:** `PUT /api/retiros-tempranos/solicitudes/{id_solicitud}/derivar`  
**Roles:** `recepcion`  
**Header:** `Authorization: Bearer {token_recepcionista}`

**Body:**
```json
{
  "id_regente": 3,
  "observacion_derivacion": "Solicitud urgente, requiere autorización inmediata"
}
```

**Campos requeridos:**
- ✅ `id_regente`: ID del usuario con rol "Regente"

**Campos opcionales:**
- `observacion_derivacion`: Notas para el regente

**Cambio de estado:** `"recibida"` → `"derivada"`

---

## 👔 SOLICITUDES INDIVIDUALES - REGENTE

### 1. Listar Solicitudes Derivadas a Mí
**Endpoint:** `GET /api/retiros-tempranos/solicitudes/derivadas-a-mi?skip=0&limit=100`  
**Roles:** `regente`  
**Header:** `Authorization: Bearer {token_regente}`

**No requiere body**

**Retorna:** Solo solicitudes derivadas al regente autenticado

### 2. Aprobar/Rechazar Solicitud
**Endpoint:** `PUT /api/retiros-tempranos/solicitudes/{id_solicitud}/decision`  
**Roles:** `regente`  
**Header:** `Authorization: Bearer {token_regente}`

**Body para APROBAR:**
```json
{
  "decision": "aprobada",
  "motivo_rechazo": null
}
```

**Body para RECHAZAR:**
```json
{
  "decision": "rechazada",
  "motivo_rechazo": "El motivo presentado no justifica el retiro temprano"
}
```

**Campos requeridos:**
- ✅ `decision`: Debe ser `"aprobada"` o `"rechazada"`
- ✅ `motivo_rechazo`: OBLIGATORIO si decision es `"rechazada"`

**Cambio de estado:** `"derivada"` → `"aprobada"` o `"rechazada"`

### 3. Listar Todas las Solicitudes (General)
**Endpoint:** `GET /api/retiros-tempranos/solicitudes/?skip=0&limit=100`  
**Roles:** `recepcion`, `regente`, `admin`  
**Header:** `Authorization: Bearer {token_regente}`

**No requiere body**

**Retorna:** Todas las solicitudes del sistema

### 4. Obtener Solicitud por ID
**Endpoint:** `GET /api/retiros-tempranos/solicitudes/{id_solicitud}`  
**Roles:** `Sin restricción (público)`

**No requiere body**

**Ejemplo:** `GET /api/retiros-tempranos/solicitudes/1`

### 5. Listar por Estudiante
**Endpoint:** `GET /api/retiros-tempranos/solicitudes/estudiante/{id_estudiante}`  
**Roles:** `recepcion`, `regente`, `admin`, `apoderado`  
**Header:** `Authorization: Bearer {token}`

**No requiere body**

**Ejemplo:** `GET /api/retiros-tempranos/solicitudes/estudiante/1`

---

## 👨‍🏫 SOLICITUDES MASIVAS - PROFESOR

### 1. Crear Solicitud Masiva
**Endpoint:** `POST /api/retiros-tempranos/solicitudes-masivas/`  
**Roles:** `profesor`, `admin`, `recepcion`, `regente`  
**Header:** `Authorization: Bearer {token_profesor}`

**Body:**
```json
{
  "id_motivo": 3,
  "fecha_hora_salida": "2025-12-20T09:00:00",
  "fecha_hora_retorno": "2025-12-20T17:00:00",
  "foto_evidencia": "https://ejemplo.com/fotos/paseo_museo.jpg",
  "observacion": "Visita educativa al museo de ciencias naturales",
  "estudiantes": [
    {
      "id_estudiante": 1,
      "observacion_individual": "Alumno con necesidades especiales"
    },
    {
      "id_estudiante": 2,
      "observacion_individual": null
    },
    {
      "id_estudiante": 5,
      "observacion_individual": "Requiere medicamento a las 14:00"
    }
  ]
}
```

**Campos requeridos:**
- ✅ `id_motivo`: ID del motivo
- ✅ `fecha_hora_salida`: Fecha y hora de salida
- ✅ `foto_evidencia`: Foto de evidencia (OBLIGATORIA)
- ✅ `estudiantes`: Lista con mínimo 1 estudiante

**Campos opcionales:**
- `fecha_hora_retorno`: Hora de retorno estimada
- `observacion`: Observación general
- `estudiantes[].observacion_individual`: Observación por estudiante

### 2. Listar Mis Solicitudes Masivas
**Endpoint:** `GET /api/retiros-tempranos/solicitudes-masivas/mis-solicitudes?skip=0&limit=100`  
**Roles:** `profesor`, `admin`, `recepcion`, `regente`  
**Header:** `Authorization: Bearer {token_profesor}`

**No requiere body**

### 3. Cancelar Solicitud Masiva
**Endpoint:** `PUT /api/retiros-tempranos/solicitudes-masivas/{id_solicitud}/cancelar`  
**Roles:** `profesor`, `admin`, `recepcion`, `regente`  
**Header:** `Authorization: Bearer {token_profesor}`

**Body:**
```json
{
  "motivo_cancelacion": "El paseo se suspendió por condiciones climáticas adversas"
}
```

**⚠️ RESTRICCIÓN:** Solo si NO está aprobada/rechazada.

### 4. Eliminar Solicitud Masiva
**Endpoint:** `DELETE /api/retiros-tempranos/solicitudes-masivas/{id_solicitud}`  
**Roles:** `profesor`, `admin`, `recepcion`, `regente`  
**Header:** `Authorization: Bearer {token_profesor}`

**No requiere body**

**⚠️ RESTRICCIÓN:** Solo si está en estado `"pendiente"`.

---

## 🏢 SOLICITUDES MASIVAS - RECEPCIONISTA

### 1. Listar Pendientes
**Endpoint:** `GET /api/retiros-tempranos/solicitudes-masivas/pendientes?skip=0&limit=100`  
**Roles:** `recepcion`  
**Header:** `Authorization: Bearer {token_recepcionista}`

**No requiere body**

### 2. Listar Recibidas
**Endpoint:** `GET /api/retiros-tempranos/solicitudes-masivas/recibidas?skip=0&limit=100`  
**Roles:** `recepcion`  
**Header:** `Authorization: Bearer {token_recepcionista}`

**No requiere body**

### 3. Recibir Solicitud Masiva
**Endpoint:** `PUT /api/retiros-tempranos/solicitudes-masivas/{id_solicitud}/recibir`  
**Roles:** `recepcion`  
**Header:** `Authorization: Bearer {token_recepcionista}`

**Body:**
```json
{
  "fecha_hora_recepcion": "2025-12-15T11:00:00"
}
```

**Campos opcionales:**
- `fecha_hora_recepcion`: Por defecto usa fecha/hora actual

**Cambio de estado:** `"pendiente"` → `"recibida"`

### 4. Derivar Solicitud Masiva
**Endpoint:** `PUT /api/retiros-tempranos/solicitudes-masivas/{id_solicitud}/derivar`  
**Roles:** `recepcion`  
**Header:** `Authorization: Bearer {token_recepcionista}`

**Body:**
```json
{
  "id_regente": 3,
  "observacion_derivacion": "Solicitud masiva para 25 estudiantes, requiere autorización urgente"
}
```

**Cambio de estado:** `"recibida"` → `"derivada"`

---

## 👔 SOLICITUDES MASIVAS - REGENTE

### 1. Listar Derivadas a Mí
**Endpoint:** `GET /api/retiros-tempranos/solicitudes-masivas/derivadas-a-mi?skip=0&limit=100`  
**Roles:** `regente`  
**Header:** `Authorization: Bearer {token_regente}`

**No requiere body**

### 2. Aprobar/Rechazar Solicitud Masiva
**Endpoint:** `PUT /api/retiros-tempranos/solicitudes-masivas/{id_solicitud}/decision`  
**Roles:** `regente`  
**Header:** `Authorization: Bearer {token_regente}`

**Body para APROBAR:**
```json
{
  "decision": "aprobada",
  "motivo_rechazo": null
}
```

**Body para RECHAZAR:**
```json
{
  "decision": "rechazada",
  "motivo_rechazo": "No se cuenta con suficientes supervisores para la actividad"
}
```

**Cambio de estado:** `"derivada"` → `"aprobada"` o `"rechazada"`

### 3. Listar Todas (General)
**Endpoint:** `GET /api/retiros-tempranos/solicitudes-masivas/?skip=0&limit=100`  
**Roles:** `recepcion`, `regente`, `admin`  
**Header:** `Authorization: Bearer {token_regente}`

**No requiere body**

### 4. Obtener por ID
**Endpoint:** `GET /api/retiros-tempranos/solicitudes-masivas/{id_solicitud}`  
**Roles:** `Sin restricción`

**No requiere body**

**Retorna:** Solicitud con lista completa de estudiantes

---

## 📤 REGISTROS DE SALIDA - RECEPCIONISTA

### 1. Crear Registro de Salida Individual
**Endpoint:** `POST /api/retiros-tempranos/registros-salida/individual`  
**Roles:** `recepcion`  
**Header:** `Authorization: Bearer {token_recepcionista}`

**Body:**
```json
{
  "id_solicitud": 1,
  "fecha_hora_salida_real": "2025-12-15T14:35:00"
}
```

**Campos requeridos:**
- ✅ `id_solicitud`: ID de solicitud individual APROBADA

**Campos opcionales:**
- `fecha_hora_salida_real`: Por defecto usa fecha/hora actual

**⚠️ RESTRICCIÓN:** La solicitud debe estar en estado `"aprobada"`.

### 2. Crear Registros de Salida Masivos
**Endpoint:** `POST /api/retiros-tempranos/registros-salida/masivo`  
**Roles:** `recepcion`  
**Header:** `Authorization: Bearer {token_recepcionista}`

**Body:**
```json
{
  "id_solicitud_masiva": 1,
  "fecha_hora_salida_real": "2025-12-20T09:05:00"
}
```

**Campos requeridos:**
- ✅ `id_solicitud_masiva`: ID de solicitud masiva APROBADA

**Campos opcionales:**
- `fecha_hora_salida_real`: Por defecto usa fecha/hora actual

**⚠️ NOTA:** Crea automáticamente un registro para CADA estudiante de la solicitud masiva.

### 3. Registrar Retorno de Estudiante
**Endpoint:** `PUT /api/retiros-tempranos/registros-salida/{id_registro}/retorno`  
**Roles:** `recepcion`  
**Header:** `Authorization: Bearer {token_recepcionista}`

**Body:**
```json
{
  "fecha_hora_retorno_real": "2025-12-15T16:10:00"
}
```

**Campos requeridos:**
- ✅ `fecha_hora_retorno_real`: Hora real de retorno del estudiante

**⚠️ RESTRICCIÓN:** Solo se puede registrar una vez.

### 4. Listar Todos los Registros
**Endpoint:** `GET /api/retiros-tempranos/registros-salida/?skip=0&limit=100`  
**Roles:** `recepcion`, `regente`, `admin`  
**Header:** `Authorization: Bearer {token_recepcionista}`

**No requiere body**

### 5. Obtener Registro por ID
**Endpoint:** `GET /api/retiros-tempranos/registros-salida/{id_registro}`  
**Roles:** `Sin restricción`

**No requiere body**

### 6. Listar por Estudiante
**Endpoint:** `GET /api/retiros-tempranos/registros-salida/estudiante/{id_estudiante}`  
**Roles:** `recepcion`, `regente`, `admin`, `apoderado`  
**Header:** `Authorization: Bearer {token}`

**No requiere body**

**Ejemplo:** `GET /api/retiros-tempranos/registros-salida/estudiante/1`

### 7. Listar por Solicitud Individual
**Endpoint:** `GET /api/retiros-tempranos/registros-salida/solicitud/{id_solicitud}`  
**Roles:** `recepcion`, `regente`, `admin`  
**Header:** `Authorization: Bearer {token}`

**No requiere body**

### 8. Listar por Solicitud Masiva
**Endpoint:** `GET /api/retiros-tempranos/registros-salida/solicitud-masiva/{id_solicitud_masiva}`  
**Roles:** `recepcion`, `regente`, `admin`  
**Header:** `Authorization: Bearer {token}`

**No requiere body**

### 9. Eliminar Registro (Solo Admin)
**Endpoint:** `DELETE /api/retiros-tempranos/registros-salida/{id_registro}`  
**Roles:** `admin`  
**Header:** `Authorization: Bearer {token_admin}`

**No requiere body**

---

## 🔄 FLUJO COMPLETO DE PRUEBA

### 📌 Escenario 1: Retiro Individual (Cita Médica)

#### **Paso 1:** Crear un motivo
```
POST /api/motivos-retiro/
Body:
{
  "nombre": "Cita médica",
  "descripcion": "Consulta médica programada",
  "severidad": "leve",
  "activo": true
}
```
✅ **Resultado:** `id_motivo = 1`

#### **Paso 2:** Login como Apoderado
```
POST /api/auth/login
Body:
{
  "usuario": "apoderado.test",
  "password": "password123"
}
```
✅ **Resultado:** Guardar `access_token`

#### **Paso 3:** Crear solicitud individual
```
POST /api/retiros-tempranos/solicitudes/
Header: Authorization: Bearer {token_apoderado}
Body:
{
  "id_estudiante": 1,
  "id_motivo": 1,
  "fecha_hora_salida": "2025-12-15T14:30:00",
  "fecha_hora_retorno_previsto": "2025-12-15T16:00:00",
  "foto_evidencia": "https://ejemplo.com/foto.jpg",
  "observacion": "Consulta oftalmológica"
}
```
✅ **Resultado:** `id_solicitud = 1`, estado = `"pendiente"`

#### **Paso 4:** Login como Recepcionista
```
POST /api/auth/login
Body:
{
  "usuario": "recepcionista.test",
  "password": "password123"
}
```
✅ **Resultado:** Guardar `access_token`

#### **Paso 5:** Ver solicitudes pendientes
```
GET /api/retiros-tempranos/solicitudes/pendientes
Header: Authorization: Bearer {token_recepcionista}
```
✅ **Resultado:** Lista con solicitud id=1

#### **Paso 6:** Recibir la solicitud
```
PUT /api/retiros-tempranos/solicitudes/1/recibir
Header: Authorization: Bearer {token_recepcionista}
Body:
{
  "fecha_hora_recepcion": "2025-12-15T10:30:00"
}
```
✅ **Resultado:** estado = `"recibida"`

#### **Paso 7:** Derivar al regente
```
PUT /api/retiros-tempranos/solicitudes/1/derivar
Header: Authorization: Bearer {token_recepcionista}
Body:
{
  "id_regente": 3,
  "observacion_derivacion": "Solicitud urgente"
}
```
✅ **Resultado:** estado = `"derivada"`

#### **Paso 8:** Login como Regente
```
POST /api/auth/login
Body:
{
  "usuario": "regente.test",
  "password": "password123"
}
```
✅ **Resultado:** Guardar `access_token`

#### **Paso 9:** Ver solicitudes derivadas
```
GET /api/retiros-tempranos/solicitudes/derivadas-a-mi
Header: Authorization: Bearer {token_regente}
```
✅ **Resultado:** Lista con solicitud id=1

#### **Paso 10:** Aprobar la solicitud
```
PUT /api/retiros-tempranos/solicitudes/1/decision
Header: Authorization: Bearer {token_regente}
Body:
{
  "decision": "aprobada",
  "motivo_rechazo": null
}
```
✅ **Resultado:** estado = `"aprobada"`

#### **Paso 11:** Crear registro de salida (como Recepcionista)
```
POST /api/retiros-tempranos/registros-salida/individual
Header: Authorization: Bearer {token_recepcionista}
Body:
{
  "id_solicitud": 1,
  "fecha_hora_salida_real": "2025-12-15T14:35:00"
}
```
✅ **Resultado:** `id_registro = 1`

#### **Paso 12:** Registrar retorno del estudiante
```
PUT /api/retiros-tempranos/registros-salida/1/retorno
Header: Authorization: Bearer {token_recepcionista}
Body:
{
  "fecha_hora_retorno_real": "2025-12-15T16:05:00"
}
```
✅ **Resultado:** Registro completado con retorno

---

### 📌 Escenario 2: Retiro Masivo (Paseo Educativo)

#### **Paso 1:** Crear motivo
```
POST /api/motivos-retiro/
Body:
{
  "nombre": "Paseo educativo",
  "descripcion": "Excursión programada",
  "severidad": "leve",
  "activo": true
}
```
✅ **Resultado:** `id_motivo = 2`

#### **Paso 2:** Login como Profesor (crear manualmente o usar admin/recepcion/regente)
```
POST /api/auth/login
Body:
{
  "usuario": "profesor.test",
  "password": "password123"
}
```
✅ **Resultado:** Guardar `access_token`

#### **Paso 3:** Crear solicitud masiva
```
POST /api/retiros-tempranos/solicitudes-masivas/
Header: Authorization: Bearer {token_profesor}
Body:
{
  "id_motivo": 2,
  "fecha_hora_salida": "2025-12-20T09:00:00",
  "fecha_hora_retorno": "2025-12-20T17:00:00",
  "foto_evidencia": "https://ejemplo.com/paseo.jpg",
  "observacion": "Museo de ciencias",
  "estudiantes": [
    {"id_estudiante": 1, "observacion_individual": null},
    {"id_estudiante": 2, "observacion_individual": "Necesita medicamento"},
    {"id_estudiante": 5, "observacion_individual": null}
  ]
}
```
✅ **Resultado:** `id_solicitud_masiva = 1`, estado = `"pendiente"`

#### **Paso 4-7:** Recepcionista recibe y deriva (igual que individual)

#### **Paso 8-9:** Regente aprueba

#### **Paso 10:** Crear registros de salida masivos
```
POST /api/retiros-tempranos/registros-salida/masivo
Header: Authorization: Bearer {token_recepcionista}
Body:
{
  "id_solicitud_masiva": 1,
  "fecha_hora_salida_real": "2025-12-20T09:05:00"
}
```
✅ **Resultado:** 3 registros creados (uno por estudiante)

#### **Paso 11:** Registrar retorno de cada estudiante
```
PUT /api/retiros-tempranos/registros-salida/{id_registro_1}/retorno
PUT /api/retiros-tempranos/registros-salida/{id_registro_2}/retorno
PUT /api/retiros-tempranos/registros-salida/{id_registro_3}/retorno
```

---

## 📊 RESUMEN DE ROLES Y ACCESOS

| Endpoint | Apoderado | Recepcionista | Regente | Profesor | Admin |
|----------|-----------|---------------|---------|----------|-------|
| **Motivos** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Crear Solicitud Individual** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Mis Solicitudes Individuales** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Cancelar/Eliminar Individual** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Ver Pendientes** | ❌ | ✅ | ❌ | ❌ | ❌ |
| **Recibir Solicitud** | ❌ | ✅ | ❌ | ❌ | ❌ |
| **Derivar Solicitud** | ❌ | ✅ | ❌ | ❌ | ❌ |
| **Ver Derivadas a Mí** | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Aprobar/Rechazar** | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Crear Solicitud Masiva** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Registros de Salida** | ❌ | ✅ | ❌ | ❌ | ❌ |
| **Ver Registros** | 👁️ | ✅ | ✅ | ❌ | ✅ |

**Leyenda:**
- ✅ Acceso completo
- 👁️ Solo lectura (limitado a sus estudiantes)
- ❌ Sin acceso

---

## 🚨 ERRORES COMUNES

### 401 Unauthorized
```json
{
  "detail": "No autenticado"
}
```
**Solución:** Verifica que incluyas el header `Authorization: Bearer {token}`

### 403 Forbidden
```json
{
  "detail": "No tiene permisos suficientes"
}
```
**Solución:** Verifica que tu usuario tenga el rol correcto para el endpoint

### 404 Not Found
```json
{
  "detail": "Solicitud no encontrada"
}
```
**Solución:** Verifica que el ID existe y que tienes permiso para verlo

### 400 Bad Request (Estado incorrecto)
```json
{
  "detail": "Solo se pueden recibir solicitudes en estado 'pendiente'"
}
```
**Solución:** Verifica el flujo de estados:
- `pendiente` → `recibida` → `derivada` → `aprobada/rechazada`

---

## ✅ VALIDACIONES IMPORTANTES

1. **Foto de evidencia:** SIEMPRE obligatoria en solicitudes
2. **Estados:** No se puede saltar pasos en el flujo
3. **Apoderados:** Solo pueden ver/modificar sus propias solicitudes
4. **Regentes:** Solo ven solicitudes derivadas a ellos específicamente
5. **Solicitud aprobada:** Necesaria para crear registro de salida
6. **Retorno:** Solo se puede registrar UNA vez por estudiante

---

## 🎯 CHECKLIST DE PRUEBAS

- [ ] Login con cada tipo de usuario
- [ ] Crear motivos con diferentes severidades
- [ ] Crear solicitud individual como apoderado
- [ ] Crear solicitud masiva como profesor
- [ ] Recibir solicitudes como recepcionista
- [ ] Derivar a regente específico
- [ ] Aprobar solicitud como regente
- [ ] Rechazar solicitud como regente
- [ ] Cancelar solicitud propia
- [ ] Crear registro de salida individual
- [ ] Crear registros masivos
- [ ] Registrar retorno de estudiantes
- [ ] Verificar permisos (intentar acciones sin rol correcto)
- [ ] Verificar flujo de estados completo

---

**📅 Última actualización:** Diciembre 15, 2025  
**📧 Contacto:** desarrollo@brisa.com

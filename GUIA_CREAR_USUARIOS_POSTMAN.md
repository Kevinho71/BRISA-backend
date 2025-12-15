# 📋 GUÍA PASO A PASO: Crear Usuarios en Postman

## 🎯 Objetivo
Crear 3 usuarios con diferentes roles para probar el módulo de retiros tempranos:
1. **Recepcionista** - Registra entradas/salidas (Rol: Recepción id=7)
2. **Regente** - Aprueba solicitudes (Rol: Regente id=3)
3. **Apoderado** - Crea solicitudes de retiro (Rol: Apoderado id=8)

---

## 🔐 PASO PREVIO: Configurar Token de Autenticación

Ya iniciaste sesión como **Director (afernandez)**. Tu token es:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMSIsInVzdWFyaW9faWQiOjIxLCJ1c3VhcmlvIjoiYWZlcm5hbmRleiIsImV4cCI6MTc2NTgxMzM1Mn0.WEEe2lj6PUsT01oafnhifpUtz1f-oSLwFpbwAcSJK4w
```

### 🔹 Cómo configurar el token en Postman:

1. **En cada petición**, ve a la pestaña **Authorization**
2. Selecciona **Type: Bearer Token**
3. Pega el token en el campo **Token**:
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMSIsInVzdWFyaW9faWQiOjIxLCJ1c3VhcmlvIjoiYWZlcm5hbmRleiIsImV4cCI6MTc2NTgxMzM1Mn0.WEEe2lj6PUsT01oafnhifpUtz1f-oSLwFpbwAcSJK4w
   ```

---

## 🏗️ ARQUITECTURA DE TABLAS

### Estructura de la base de datos (según tus imágenes):

```
personas (tipo_persona: profesor/administrativo/apoderado)
    ├── profesores (id_persona + datos específicos)
    ├── administrativos (id_persona + id_cargo + horarios)
    └── apoderados (id_persona + datos de contacto)
            └── estudiantes_apoderados (relación con estudiantes)

usuarios (id_persona + credenciales)
    └── usuario_roles (asignación de roles)
```

### ⚠️ IMPORTANTE: Conceptos Clave

| Concepto | Descripción | Ejemplo |
|----------|-------------|---------|
| **personas.tipo_persona** | ENUM en BD (solo 3 valores) | `profesor`, `administrativo`, `apoderado` |
| **administrativos.id_cargo** | FK a tabla cargos | Recepcionista (id=6), Regente (id=2) |
| **roles.id_rol** | Permisos del usuario | Recepción (id=7), Regente (id=3), Apoderado (id=8) |
| **Recepcionista** | tipo_persona=`administrativo` + cargo=6 + rol=7 |
| **Regente** | tipo_persona=`administrativo` + cargo=2 + rol=3 |
| **Apoderado** | tipo_persona=`apoderado` (sin cargo) + rol=8 |

---

## 📝 FLUJO DE CREACIÓN

### Existen 2 métodos para crear usuarios:

#### **Método 1: Paso a Paso** (3 pasos separados)
1. Crear PERSONA (con endpoint específico: administrativos, profesores, etc.)
2. Crear USUARIO para esa persona
3. Asignar ROL al usuario

#### **Método 2: Todo en Uno** (1 solo endpoint) ✅ **RECOMENDADO**
- Usa `/api/auth/registro` que crea persona + usuario + asigna rol

---

## 🚀 MÉTODO RECOMENDADO: Registro Todo en Uno

Usaremos `/api/auth/registro` para crear las 3 personas con sus usuarios en un solo paso.

---

## 1️⃣ CREAR RECEPCIONISTA (Todo en Uno)

### **Paso 1.1: Crear Persona + Usuario + Asignar Rol**

**Método:** `POST`  
**URL:** `http://localhost:8000/api/auth/registro`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "ci": "9876543",
  "nombres": "María",
  "apellido_paterno": "López",
  "apellido_materno": "Rojas",
  "usuario": "mlopez",
  "correo": "mlopez@colegio.edu.bo",
  "password": "Recepcion123!",
  "telefono": "79812345",
  "direccion": "Av. Siempre Viva 742",
  "tipo_persona": "administrativo",
  "id_rol": 7
}
```

📥 **Respuesta esperada:**
```json
{
  "status": "success",
  "message": "Usuario registrado exitosamente",
  "data": {
    "id_usuario": 45,
    "usuario": "mlopez",
    "correo": "mlopez@colegio.edu.bo",
    "nombres": "María López",
    "mensaje": "Usuario registrado exitosamente"
  }
}
```

### **Paso 1.2: Crear registro en tabla `administrativos`**

⚠️ **IMPORTANTE:** El endpoint `/api/auth/registro` solo crea en tabla `personas` y `usuarios`. Para completar el perfil de administrativo, necesitas crear el registro en `administrativos`.

**Método:** `POST`  
**URL:** `http://localhost:8000/api/administrativos/`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "ci": "9876543",
  "nombres": "María",
  "apellido_paterno": "López",
  "apellido_materno": "Rojas",
  "correo": "mlopez@colegio.edu.bo",
  "telefono": "79812345",
  "direccion": "Av. Siempre Viva 742",
  "id_cargo": 6,
  "estado_laboral": "activo",
  "anos_experiencia": 3
}
```

**Explicación de campos importantes:**
- `id_cargo: 6` → Cargo "Recepcionista" (según tu tabla cargos)
- `estado_laboral`: activo/retirado/suspendido
- `anos_experiencia`: Años de experiencia laboral

📥 **Respuesta esperada:**
```json
{
  "status": "success",
  "message": "Administrativo creado exitosamente",
  "data": {
    "id_administrativo": 11,
    "id_persona": 31,
    "ci": "9876543",
    "nombre_completo": "María López Rojas",
    "cargo": "Recepcionista",
    "area_trabajo": "Recepción"
  }
}
```

✅ **RECEPCIONISTA CREADO CON ÉXITO**

**Credenciales para probar:**
```
Usuario: mlopez
Contraseña: Recepcion123!
```

---

## 2️⃣ CREAR REGENTE (Todo en Uno)

### **Paso 2.1: Crear Persona + Usuario + Asignar Rol**

**Método:** `POST`  
**URL:** `http://localhost:8000/api/auth/registro`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "ci": "8765432",
  "nombres": "Carlos",
  "apellido_paterno": "Mendoza",
  "apellido_materno": "Silva",
  "usuario": "cmendoza",
  "correo": "cmendoza@colegio.edu.bo",
  "password": "Regente123!",
  "telefono": "79823456",
  "direccion": "Calle Los Pinos 456",
  "tipo_persona": "administrativo",
  "id_rol": 3
}
```

**Explicación de campos importantes:**
- `tipo_persona: "administrativo"` → Para regente (NO existe tipo_persona "regente" en BD)
- `id_rol: 3` → Rol "Regente" (según tu tabla roles)

📥 **Guardar `id_usuario` de la respuesta**

### **Paso 2.2: Crear registro en tabla `administrativos`**

**Método:** `POST`  
**URL:** `http://localhost:8000/api/administrativos/`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "ci": "8765432",
  "nombres": "Carlos",
  "apellido_paterno": "Mendoza",
  "apellido_materno": "Silva",
  "correo": "cmendoza@colegio.edu.bo",
  "telefono": "79823456",
  "direccion": "Calle Los Pinos 456",
  "id_cargo": 2,
  "estado_laboral": "activo",
  "anos_experiencia": 8
}
```

**Explicación de campos importantes:**
- `id_cargo: 2` → Cargo "Regente" (según tu tabla cargos)

✅ **REGENTE CREADO CON ÉXITO**

**Credenciales para probar:**
```
Usuario: cmendoza
Contraseña: Regente123!
```

---

## 3️⃣ CREAR APODERADO (Flujo Completo)

⚠️ **IMPORTANTE:** Los apoderados tienen un flujo especial porque deben:
1. Tener registro en tabla `personas` (tipo_persona='apoderado')
2. Tener registro en tabla `apoderados` (con id_persona)
3. Estar asociados a estudiantes en `estudiantes_apoderados`

### **Paso 3.1: Crear Persona + Usuario + Asignar Rol**

**Método:** `POST`  
**URL:** `http://localhost:8000/api/auth/registro`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "ci": "7654321",
  "nombres": "Ana",
  "apellido_paterno": "García",
  "apellido_materno": "Morales",
  "usuario": "agarcia",
  "correo": "agarcia@gmail.com",
  "password": "Apoderado123!",
  "telefono": "79834567",
  "direccion": "Zona Norte 789",
  "tipo_persona": "apoderado",
  "id_rol": 8
}
```

**Explicación de campos importantes:**
- `tipo_persona: "apoderado"` → Crea registro en tabla personas como apoderado
- `id_rol: 8` → Rol "Apoderado" (según tu tabla roles)
- `password`: Contraseña que el apoderado usará para login

📥 **Respuesta esperada:**
```json
{
  "status": "success",
  "message": "Usuario registrado exitosamente",
  "data": {
    "id_usuario": 47,
    "usuario": "agarcia",
    "correo": "agarcia@gmail.com",
    "nombres": "Ana García",
    "mensaje": "Usuario registrado exitosamente"
  }
}
```

🔸 **GUARDA el `id_usuario`** (ejemplo: 47)

### **Paso 3.2: Obtener id_persona del usuario creado**

**Método:** `GET`  
**URL:** `http://localhost:8000/api/auth/usuarios/47`

*(Reemplaza `47` con el id_usuario obtenido)*

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

📥 **Respuesta esperada:**
```json
{
  "status": "success",
  "data": {
    "id_usuario": 47,
    "id_persona": 32,  // 👈 GUARDAR ESTE ID
    "usuario": "agarcia",
    "correo": "agarcia@gmail.com"
  }
}
```

🔸 **GUARDA el `id_persona`** (ejemplo: 32)

### **Paso 3.3: Crear registro en tabla `apoderados`**

⚠️ **CRÍTICO:** Necesitas ejecutar SQL directo o usar un endpoint específico (si existe).

**Opción A: SQL Directo** (en tu gestor de base de datos)

```sql
INSERT INTO apoderados (id_persona, ci, nombres, apellidos, telefono, correo, direccion)
VALUES (32, '7654321', 'Ana', 'García Morales', '79834567', 'agarcia@gmail.com', 'Zona Norte 789');
```

**Opción B: Si existe endpoint /api/retiros-tempranos/apoderados**

*(Este endpoint probablemente NO existe, necesitarías crearlo)*

```
POST http://localhost:8000/api/retiros-tempranos/apoderados/
Body: {
  "id_persona": 32,
  "ci": "7654321",
  "nombres": "Ana",
  "apellidos": "García Morales",
  "telefono": "79834567",
  "correo": "agarcia@gmail.com",
  "direccion": "Zona Norte 789"
}
```

📥 **Ejecuta el SQL y obtén el id_apoderado** (ejemplo: 18)

### **Paso 3.4: Asociar apoderado con un estudiante**

**Método:** `POST`  
**URL:** `http://localhost:8000/api/estudiantes-apoderados/`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "id_estudiante": 1,
  "id_apoderado": 18,
  "parentesco": "Padre",
  "es_contacto_principal": 1
}
```

**Explicación de campos:**
- `id_estudiante`: ID de un estudiante existente en tu BD (revisa tabla estudiantes)
- `id_apoderado`: ID del apoderado recién creado (18 en el ejemplo)
- `parentesco`: "Padre", "Madre", "Tío", "Abuelo", "Tutor Legal", etc.
- `es_contacto_principal`: 1 (sí) o 0 (no)

📥 **Respuesta esperada:**
```json
{
  "id_estudiante": 1,
  "id_apoderado": 18,
  "parentesco": "Padre",
  "es_contacto_principal": 1
}
```

✅ **APODERADO CREADO CON ÉXITO Y ASOCIADO A ESTUDIANTE**

**Credenciales para probar:**
```
Usuario: agarcia
Contraseña: Apoderado123!
```

---

## 🔍 PASO 4: VERIFICAR USUARIOS CREADOS

### **4.1: Listar todos los usuarios**

**Método:** `GET`  
**URL:** `http://localhost:8000/api/auth/usuarios`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

📥 **Respuesta esperada:**
```json
{
  "status": "success",
  "message": "Usuarios obtenidos",
  "data": [
    {
      "id_usuario": 45,
      "usuario": "mlopez",
      "correo": "mlopez@colegio.edu.bo",
      "persona_nombre": "María López Rojas"
    },
    {
      "id_usuario": 46,
      "usuario": "cmendoza",
      "correo": "cmendoza@colegio.edu.bo",
      "persona_nombre": "Carlos Mendoza Silva"
    },
    {
      "id_usuario": 47,
      "usuario": "agarcia",
      "correo": "agarcia@gmail.com",
      "persona_nombre": "Ana García Morales"
    }
  ]
}
```

---

### **4.2: Verificar roles asignados**

**Método:** `GET`  
**URL:** `http://localhost:8000/api/auth/roles/7/usuarios`

*(Reemplaza `7` con el `id_rol` que quieras consultar)*

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

📥 **Respuesta esperada:**
```json
{
  "status": "success",
  "message": "Usuarios del rol obtenidos (1 usuarios)",
  "data": [
    {
      "id_usuario": 45,
      "usuario": "mlopez",
      "nombre_completo": "María López Rojas",
      "tipo_persona": "administrativo"
    }
  ]
}
```

---

### **4.3: Verificar administrativos creados**

**Método:** `GET`  
**URL:** `http://localhost:8000/api/administrativos/`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

📥 **Debe mostrar a mlopez y cmendoza en la lista**

---

### **4.4: Verificar relación estudiante-apoderado**

**Método:** `GET`  
**URL:** `http://localhost:8000/api/estudiantes-apoderados/apoderado/18`

*(Reemplaza `18` con el id_apoderado)*

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

📥 **Debe mostrar los estudiantes asociados al apoderado**

---

## 🧪 PASO 5: PROBAR LOGIN CON LOS NUEVOS USUARIOS

### **5.1: Login como Recepcionista**

**Método:** `POST`  
**URL:** `http://localhost:8000/api/auth/login`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "usuario": "mlopez",
  "password": "Recepcion123!"
}
```

📥 **Respuesta esperada:**
```json
{
  "status": "success",
  "message": "Inicio de sesión exitoso",
  "data": {
    "access_token": "eyJhbGciOiJIUz...",
    "token_type": "bearer",
    "expires_in": 3600,
    "usuario": {
      "id_usuario": 45,
      "usuario": "mlopez",
      "roles": ["Recepción"],
      "permisos": ["ver_registros", "crear_registros", ...]
    }
  }
}
```

✅ **GUARDAR EL TOKEN** para usar en endpoints de recepcionista

---

### **5.2: Login como Regente**

**Método:** `POST`  
**URL:** `http://localhost:8000/api/auth/login`

**Body (JSON):**
```json
{
  "usuario": "cmendoza",
  "password": "Regente123!"
}
```

📥 **Debe mostrar roles: ["Regente"]**

✅ **GUARDAR EL TOKEN** para aprobar solicitudes

---

### **5.3: Login como Apoderado**

**Método:** `POST`  
**URL:** `http://localhost:8000/api/auth/login`

**Body (JSON):**
```json
{
  "usuario": "agarcia",
  "password": "Apoderado123!"
}
```

📥 **Debe mostrar roles: ["Apoderado"]**

✅ **GUARDAR EL TOKEN** para crear solicitudes

---

## 🎯 PASO 6: PROBAR FLUJO COMPLETO DE RETIROS TEMPRANOS

### **6.1: Apoderado crea solicitud**

**Método:** `POST`  
**URL:** `http://localhost:8000/api/retiros-tempranos/solicitudes/`

**Headers:**
```
Authorization: Bearer <token_apoderado>
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "id_estudiante": 1,
  "motivo": "Cita médica",
  "fecha_retiro": "2025-12-16",
  "hora_retiro": "14:00:00",
  "foto_evidencia": "base64_string_aqui"
}
```

📥 **Respuesta: estado = "pendiente"**

---

### **6.2: Regente aprueba solicitud**

**Método:** `PUT`  
**URL:** `http://localhost:8000/api/retiros-tempranos/solicitudes-masivas/1/aprobar`

**Headers:**
```
Authorization: Bearer <token_regente>
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "observaciones_regente": "Aprobado por motivo médico válido"
}
```

📥 **Respuesta: estado = "aprobada"**

---

### **6.3: Recepcionista registra salida**

**Método:** `POST`  
**URL:** `http://localhost:8000/api/retiros-tempranos/registros-salida/individual`

**Headers:**
```
Authorization: Bearer <token_recepcionista>
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "id_solicitud": 1,
  "fecha_hora_salida_real": "2025-12-16T14:05:00"
}
```

📥 **Respuesta: registro creado con hora de salida**

---

## 📊 RESUMEN DE IDS IMPORTANTES

### Roles (tabla `roles`)
| Rol | id_rol | Descripción |
|-----|--------|-------------|
| Director | 1 | Permisos totales |
| Profesor | 2 | Gestión de clases y esquelas |
| Regente | 3 | Aprobación de solicitudes |
| Recepción | 7 | Registro de entradas/salidas |
| Apoderado | 8 | Crear solicitudes de retiro |

### Cargos (tabla `cargos`)
| Cargo | id_cargo | Nivel Jerárquico |
|-------|----------|------------------|
| Director General | 1 | 1 |
| Regente | 2 | 2 |
| Coordinador Académico | 3 | 3 |
| Secretaria | 4 | 4 |
| Auxiliar Administrativo | 5 | 5 |
| Recepcionista | 6 | 5 |
| Contador | 7 | 4 |
| Psicólogo | 8 | 3 |
| Enfermero | 9 | 4 |
| Bibliotecario | 10 | 5 |

### Tipos de Persona (ENUM en BD)
- `profesor` → Para docentes
- `administrativo` → Para personal administrativo (recepcionista, regente, secretaria, etc.)
- `apoderado` → Para padres/tutores de estudiantes

---

## ⚠️ PROBLEMAS COMUNES Y SOLUCIONES

### 🔴 Error: "tipo_persona debe ser uno de: profesor, administrativo, apoderado"

**Causa:** Intentaste usar tipo_persona='regente' o 'recepcionista'  
**Solución:** Usa `"tipo_persona": "administrativo"` para ambos, diferéncialos con `id_cargo` y `id_rol`

---

### 🔴 Error: "CI ya registrado"

**Causa:** Ya existe una persona con ese CI  
**Solución:** Cambia el CI o verifica con:
```sql
SELECT * FROM personas WHERE ci = '9876543';
```

---

### 🔴 Error: "Usuario o correo ya existe"

**Causa:** Ya existe un usuario con ese nombre o email  
**Solución:** Usa otro nombre de usuario o correo único

---

### 🔴 Error: "Persona con ID X no encontrada"

**Causa:** No existe la persona antes de crear el usuario  
**Solución:** Verifica que completaste el paso 3.1 antes del 3.2

---

### 🔴 Error: "Usuario no tiene perfil de apoderado" al crear solicitud

**Causa:** Falta registro en tabla `apoderados` con `id_persona`  
**Solución:** Completa el Paso 3.3 (crear registro en apoderados)

---

### 🔴 Error al crear relación estudiante-apoderado

**Causa:** `id_estudiante` no existe o `id_apoderado` incorrecto  
**Solución:** Verifica IDs con:
```sql
SELECT id_estudiante FROM estudiantes LIMIT 10;
SELECT id_apoderado FROM apoderados WHERE ci = '7654321';
```

---

## 📝 SCRIPT SQL COMPLETO (ALTERNATIVA RÁPIDA)

Si prefieres crear todo por SQL directo:

```sql
-- 1. CREAR RECEPCIONISTA
-- Persona
INSERT INTO personas (ci, nombres, apellido_paterno, apellido_materno, telefono, correo, direccion, tipo_persona, is_active)
VALUES ('9876543', 'María', 'López', 'Rojas', '79812345', 'mlopez@colegio.edu.bo', 'Av. Siempre Viva 742', 'administrativo', 1);

SET @id_persona_recep = LAST_INSERT_ID();

-- Administrativo
INSERT INTO administrativos (id_persona, id_cargo, horario_entrada, horario_salida, area_trabajo, observaciones)
VALUES (@id_persona_recep, 6, '07:30:00', '15:30:00', 'Recepción', 'Recepcionista turno mañana');

-- Usuario
INSERT INTO usuarios (id_persona, usuario, correo, password, is_active)
VALUES (@id_persona_recep, 'mlopez', 'mlopez@colegio.edu.bo', '$2b$12$hashed_password_aqui', 1);

SET @id_usuario_recep = LAST_INSERT_ID();

-- Asignar rol
INSERT INTO usuario_roles (id_usuario, id_rol)
VALUES (@id_usuario_recep, 7);

-- 2. CREAR REGENTE
INSERT INTO personas (ci, nombres, apellido_paterno, apellido_materno, telefono, correo, direccion, tipo_persona, is_active)
VALUES ('8765432', 'Carlos', 'Mendoza', 'Silva', '79823456', 'cmendoza@colegio.edu.bo', 'Calle Los Pinos 456', 'administrativo', 1);

SET @id_persona_regente = LAST_INSERT_ID();

INSERT INTO administrativos (id_persona, id_cargo, horario_entrada, horario_salida, area_trabajo, observaciones)
VALUES (@id_persona_regente, 2, '08:00:00', '16:00:00', 'Regencia', 'Regente académico');

INSERT INTO usuarios (id_persona, usuario, correo, password, is_active)
VALUES (@id_persona_regente, 'cmendoza', 'cmendoza@colegio.edu.bo', '$2b$12$hashed_password_aqui', 1);

SET @id_usuario_regente = LAST_INSERT_ID();

INSERT INTO usuario_roles (id_usuario, id_rol)
VALUES (@id_usuario_regente, 3);

-- 3. CREAR APODERADO
INSERT INTO personas (ci, nombres, apellido_paterno, apellido_materno, telefono, correo, direccion, tipo_persona, is_active)
VALUES ('7654321', 'Ana', 'García', 'Morales', '79834567', 'agarcia@gmail.com', 'Zona Norte 789', 'apoderado', 1);

SET @id_persona_apod = LAST_INSERT_ID();

INSERT INTO apoderados (id_persona, ci, nombres, apellidos, telefono, correo, direccion)
VALUES (@id_persona_apod, '7654321', 'Ana', 'García Morales', '79834567', 'agarcia@gmail.com', 'Zona Norte 789');

SET @id_apoderado = LAST_INSERT_ID();

INSERT INTO usuarios (id_persona, usuario, correo, password, is_active)
VALUES (@id_persona_apod, 'agarcia', 'agarcia@gmail.com', '$2b$12$hashed_password_aqui', 1);

SET @id_usuario_apod = LAST_INSERT_ID();

INSERT INTO usuario_roles (id_usuario, id_rol)
VALUES (@id_usuario_apod, 8);

-- Asociar apoderado con estudiante (cambiar id_estudiante según tu BD)
INSERT INTO estudiantes_apoderados (id_estudiante, id_apoderado, parentesco, es_contacto_principal)
VALUES (1, @id_apoderado, 'Padre', 1);
```

⚠️ **NOTA:** Debes generar las contraseñas hasheadas con bcrypt. Usa Python:
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd_context.hash("Recepcion123!"))
print(pwd_context.hash("Regente123!"))
print(pwd_context.hash("Apoderado123!"))
```

---

## ✅ CHECKLIST FINAL

- [ ] Recepcionista creado (mlopez) - Usuario + Administrativo + Rol
- [ ] Regente creado (cmendoza) - Usuario + Administrativo + Rol
- [ ] Apoderado creado (agarcia) - Usuario + Apoderado + Rol + Relación estudiante
- [ ] Login exitoso con Recepcionista → Token obtenido
- [ ] Login exitoso con Regente → Token obtenido
- [ ] Login exitoso con Apoderado → Token obtenido
- [ ] Roles verificados en `/api/auth/roles/{id_rol}/usuarios`
- [ ] Administrativos verificados en `/api/administrativos/`
- [ ] Relación estudiante-apoderado verificada
- [ ] Flujo completo probado: Apoderado crea → Regente aprueba → Recepcionista registra

---

**🎉 ¡Listo! Ahora puedes probar el flujo completo de retiros tempranos con los 3 roles.**

---

## 📞 AYUDA ADICIONAL

**Si necesitas ayuda con:**
- Generar contraseñas hasheadas → Usa el script Python con bcrypt
- Ver estudiantes disponibles → `SELECT * FROM estudiantes LIMIT 10;`
- Ver apoderados → `SELECT * FROM apoderados;`
- Ver relaciones → `SELECT * FROM estudiantes_apoderados;`

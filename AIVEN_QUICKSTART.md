# 🚀 GUÍA RÁPIDA - AIVEN CLOUD

## ✅ Configuración Completada

Las credenciales de Aiven Cloud ya están configuradas en `.env`

**Host:** bienestarestudiantil-hola.e.aivencloud.com  
**Puerto:** 19241  
**Base de datos:** defaultdb  
**Usuario:** avnadmin  

---

## 📋 PASOS PARA INICIAR

### 1️⃣ **Probar la Conexión**

```powershell
python scripts/test_aiven_connection.py
```

Esto verificará que puedes conectarte a Aiven Cloud.

---

### 2️⃣ **Crear las Tablas (Ejecutar Esquema)**

```powershell
python scripts/setup_aiven_schema.py
```

Esto creará todas las tablas del esquema en la base de datos Aiven.

---

### 3️⃣ **Cargar Datos de Prueba**

```powershell
python scripts/load_aiven_data.py
```

Esto insertará los datos de prueba (estudiantes, apoderados, cursos, etc.)

---

### 4️⃣ **Iniciar la Aplicación**

```powershell
python run.py
```

La API estará disponible en:
- 🌐 **API**: http://localhost:8000
- 📖 **Swagger Docs**: http://localhost:8000/docs
- ❤️ **Health Check**: http://localhost:8000/api/health

---

## 🎯 COMANDOS RÁPIDOS (TODO EN UNO)

```powershell
# 1. Probar conexión
python scripts/test_aiven_connection.py

# 2. Si la conexión es exitosa, crear tablas
python scripts/setup_aiven_schema.py

# 3. Cargar datos de prueba
python scripts/load_aiven_data.py

# 4. Iniciar aplicación
python run.py
```

---

## 🔒 INFORMACIÓN DE SEGURIDAD

- ✅ La conexión usa **SSL automáticamente** (Aiven requiere SSL)
- ✅ El archivo `.env` está en `.gitignore` (no se subirá a Git)
- ⚠️ **NUNCA compartas tus credenciales públicamente**

---

## ❌ Solución de Problemas

### Error: "SSL connection required"
**Solución:** Ya está configurado automáticamente en `extensions.py`

### Error: "Access denied"
**Solución:** Verifica que las credenciales en `.env` sean correctas

### Error: "No module named 'cryptography'"
**Solución:** 
```powershell
pip install cryptography
```

### Error: "Can't connect to MySQL server"
**Solución:** Verifica tu conexión a internet

---

## 📊 Datos de Prueba Incluidos

Después de ejecutar `load_aiven_data.py`:
- ✅ 7 Personas (profesores/admin)
- ✅ 10 Estudiantes
- ✅ 5 Cursos
- ✅ 8 Materias
- ✅ 8 Apoderados
- ✅ 15 Relaciones estudiante-apoderado
- ✅ 5 Motivos de retiro

---

## 🎉 ¡Listo para Probar!

Una vez iniciada la aplicación, abre:

**http://localhost:8000/docs**

Y prueba los endpoints de Retiros Tempranos:
- `POST /api/solicitudes-retiro`
- `GET /api/estudiantes-apoderados/estudiante/{id}`
- `POST /api/autorizaciones-retiro`

---

## 💡 Nota Importante

La base de datos **defaultdb** en Aiven Cloud es compartida.  
Si necesitas usar otra base de datos, créala desde el panel de Aiven.

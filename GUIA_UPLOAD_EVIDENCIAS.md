# 📸 Guía: Upload de Fotos de Evidencia

## 🎯 Resumen

El sistema de retiros tempranos requiere una **foto de evidencia** para cada solicitud. Este documento explica cómo manejar las fotos en **desarrollo (Postman)** y **producción (Frontend)**.

---

## 🧪 OPCIÓN 1: Testing en Postman (Desarrollo)

### Método A: Usar URLs de Prueba (Más Rápido)

Para testing rápido, usa URLs de imágenes públicas:

```json
{
  "id_estudiante": 123,
  "id_motivo": 5,
  "fecha_hora_salida": "2025-12-15T16:00:00",
  "foto_evidencia": "https://via.placeholder.com/400x300?text=Evidencia+Retiro",
  "observacion": "Cita médica"
}
```

**Otras URLs de prueba:**
- `https://picsum.photos/400/300` (foto aleatoria)
- `https://via.placeholder.com/400x300?text=Mi+Evidencia`
- `https://dummyimage.com/400x300/000/fff&text=Retiro`

### Método B: Subir Foto Real (Recomendado)

**Paso 1: Subir la foto**

```http
POST http://localhost:8000/api/retiros-tempranos/upload/evidencia
Authorization: Bearer {tu_token}
Content-Type: multipart/form-data

file: [selecciona un archivo de tu computadora]
```

**En Postman:**
1. Método: `POST`
2. URL: `http://localhost:8000/api/retiros-tempranos/upload/evidencia`
3. Tab **Authorization**: Bearer Token (tu token de login)
4. Tab **Body**: 
   - Selecciona `form-data`
   - Key: `file` (cambiar tipo a "File")
   - Value: Click "Select Files" y elige una imagen

**Respuesta esperada:**
```json
{
  "success": true,
  "message": "Foto de evidencia subida exitosamente",
  "data": {
    "url": "/uploads/retiros_tempranos/evidencias/2025-12-15_15-30-45_abc12345.jpg",
    "filename": "2025-12-15_15-30-45_abc12345.jpg",
    "original_filename": "foto.jpg",
    "size_bytes": 245678,
    "uploaded_by": 41,
    "uploaded_at": "2025-12-15T15:30:45.123456"
  }
}
```

**Paso 2: Crear la solicitud usando la URL**

Copia la URL del campo `data.url` y úsala en la solicitud:

```json
POST http://localhost:8000/api/retiros-tempranos/solicitudes/
Authorization: Bearer {tu_token_apoderado}

{
  "id_estudiante": 123,
  "id_motivo": 5,
  "fecha_hora_salida": "2025-12-15T16:00:00",
  "foto_evidencia": "/uploads/retiros_tempranos/evidencias/2025-12-15_15-30-45_abc12345.jpg",
  "observacion": "Cita médica"
}
```

---

## 🌐 OPCIÓN 2: Frontend (Producción)

### Flujo Completo

```javascript
// 1. Usuario selecciona foto en el formulario
const handleFileChange = async (event) => {
  const file = event.target.files[0];
  
  // Validaciones antes de subir
  if (!file) return;
  
  if (file.size > 5 * 1024 * 1024) {
    alert('La foto no puede pesar más de 5MB');
    return;
  }
  
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
  if (!allowedTypes.includes(file.type)) {
    alert('Solo se permiten imágenes JPG, PNG, GIF o WEBP');
    return;
  }
  
  // 2. Subir foto al servidor
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    const uploadResponse = await fetch('/api/retiros-tempranos/upload/evidencia', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: formData  // No poner Content-Type, FormData lo maneja
    });
    
    const uploadData = await uploadResponse.json();
    
    if (uploadData.success) {
      // 3. Guardar la URL para usar en la solicitud
      const fotoUrl = uploadData.data.url;
      setFotoEvidencia(fotoUrl);  // Estado de React/Vue
      
      console.log('Foto subida:', fotoUrl);
    }
  } catch (error) {
    console.error('Error al subir foto:', error);
    alert('Error al subir la foto');
  }
};

// 4. Al crear la solicitud, incluir la URL
const crearSolicitud = async () => {
  const solicitudData = {
    id_estudiante: estudianteSeleccionado,
    id_motivo: motivoSeleccionado,
    fecha_hora_salida: fechaHoraSalida,
    foto_evidencia: fotoEvidencia,  // La URL obtenida del upload
    observacion: observaciones
  };
  
  const response = await fetch('/api/retiros-tempranos/solicitudes/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(solicitudData)
  });
  
  // Manejar respuesta...
};
```

### Ejemplo con React

```jsx
import React, { useState } from 'react';

function SolicitudRetiroForm() {
  const [fotoEvidencia, setFotoEvidencia] = useState('');
  const [uploading, setUploading] = useState(false);
  
  const handleUploadFoto = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const res = await fetch('/api/retiros-tempranos/upload/evidencia', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });
      
      const data = await res.json();
      setFotoEvidencia(data.data.url);
    } catch (err) {
      alert('Error al subir foto');
    } finally {
      setUploading(false);
    }
  };
  
  return (
    <div>
      <input 
        type="file" 
        accept="image/*" 
        onChange={handleUploadFoto}
        disabled={uploading}
      />
      {uploading && <p>Subiendo...</p>}
      {fotoEvidencia && <img src={fotoEvidencia} alt="Preview" width="200" />}
    </div>
  );
}
```

---

## 📋 Especificaciones Técnicas

### Formatos Permitidos
- ✅ JPG / JPEG
- ✅ PNG
- ✅ GIF
- ✅ WEBP

### Limitaciones
- **Tamaño máximo:** 5MB
- **Nombres:** Se generan automáticamente con timestamp + UUID único

### Estructura de Almacenamiento

```
uploads/
└── retiros_tempranos/
    └── evidencias/
        ├── 2025-12-15_15-30-45_abc12345.jpg
        ├── 2025-12-15_16-20-10_def67890.png
        └── ...
```

### Acceso a Archivos

Las fotos se sirven como archivos estáticos:

```
http://localhost:8000/uploads/retiros_tempranos/evidencias/2025-12-15_15-30-45_abc12345.jpg
```

---

## 🔒 Seguridad

1. **Autenticación requerida:** Solo usuarios autenticados pueden subir fotos
2. **Validación de tipo:** Solo se aceptan imágenes
3. **Validación de tamaño:** Máximo 5MB
4. **Nombres únicos:** Previene colisiones y sobrescrituras
5. **Path traversal protection:** El endpoint de eliminación valida que el archivo esté en el directorio correcto

---

## ❌ Errores Comunes

### Error: "Formato no permitido"
```json
{
  "detail": "Formato no permitido. Use: .jpg, .jpeg, .png, .gif, .webp"
}
```
**Solución:** Convertir la imagen a un formato permitido.

### Error: "Archivo muy grande"
```json
{
  "detail": "Archivo muy grande. Tamaño máximo: 5.0MB"
}
```
**Solución:** Reducir el tamaño/calidad de la imagen.

### Error: 401 Unauthorized
```json
{
  "detail": "Usuario no autenticado - token inválido o no proporcionado"
}
```
**Solución:** Incluir el token de autenticación en el header.

---

## 🚀 Endpoints Disponibles

### 1. Subir Foto
```
POST /api/retiros-tempranos/upload/evidencia
Authorization: Bearer {token}
Content-Type: multipart/form-data

Permisos: apoderado, profesor, recepcion, regente
```

### 2. Eliminar Foto
```
DELETE /api/retiros-tempranos/upload/evidencia/{filename}
Authorization: Bearer {token}

Permisos: admin, regente, recepcion
```

---

## 💡 Mejoras Futuras (Opcional)

Para producción avanzada, podrías:

1. **Usar servicios cloud:**
   - AWS S3
   - Google Cloud Storage
   - Cloudinary
   - Supabase Storage

2. **Compresión automática:**
   - Reducir peso sin perder calidad
   - Generar thumbnails

3. **Validación de contenido:**
   - Verificar que sea realmente una imagen
   - Detectar contenido inapropiado

4. **CDN:**
   - Servir imágenes más rápido
   - Caché distribuido

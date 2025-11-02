CREATE DATABASE IF NOT EXISTS bienestar_estudiantil;
USE bienestar_estudiantil;

-- ================================
-- MÓDULO 1: USUARIOS, ROLES Y PERMISOS
-- ================================

CREATE TABLE IF NOT EXISTS personas (
    id_persona INT AUTO_INCREMENT PRIMARY KEY,
    ci VARCHAR(20) NOT NULL,
    nombres VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50) NOT NULL,
    direccion VARCHAR(100),
    telefono VARCHAR(20),
    correo VARCHAR(50),
    tipo_persona ENUM('profesor','administrativo') NOT NULL
);

CREATE TABLE IF NOT EXISTS roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS permisos (
    id_permiso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS rol_permisos (
    id_rol INT NOT NULL,
    id_permiso INT NOT NULL,
    PRIMARY KEY (id_rol, id_permiso),
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol),
    FOREIGN KEY (id_permiso) REFERENCES permisos(id_permiso)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_persona INT NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    correo VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_persona) REFERENCES personas(id_persona)
);

CREATE TABLE IF NOT EXISTS usuario_roles (
    id_usuario INT NOT NULL,
    id_rol INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    estado ENUM('activo','inactivo') NOT NULL,
    PRIMARY KEY (id_usuario, id_rol, fecha_inicio),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

CREATE TABLE IF NOT EXISTS login_logs (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE IF NOT EXISTS bitacora (
    id_bitacora INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario_admin INT NOT NULL,
    accion VARCHAR(50) NOT NULL,
    descripcion TEXT,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_objetivo INT NULL,
    tipo_objetivo VARCHAR(50) NULL,
    FOREIGN KEY (id_usuario_admin) REFERENCES usuarios(id_usuario)
);

-- ================================
-- MÓDULO 2: ESTUDIANTES Y CURSOS
-- ================================

CREATE TABLE IF NOT EXISTS estudiantes (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    ci VARCHAR(20),
    nombres VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE,
    direccion VARCHAR(100),
    nombre_padre VARCHAR(50),
    apellido_paterno_padre VARCHAR(50),
    apellido_materno_padre VARCHAR(50),
    telefono_padre VARCHAR(20),
    nombre_madre VARCHAR(50),
    apellido_paterno_madre VARCHAR(50),
    apellido_materno_madre VARCHAR(50),
    telefono_madre VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS cursos (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    nombre_curso VARCHAR(50) NOT NULL,
    nivel ENUM('inicial','primaria','secundaria') NOT NULL,
    gestion VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS estudiantes_cursos (
    id_estudiante INT NOT NULL,
    id_curso INT NOT NULL,
    PRIMARY KEY (id_estudiante, id_curso),
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
);

-- ================================
-- MÓDULO 3: PROFESORES Y MATERIAS
-- ================================

CREATE TABLE IF NOT EXISTS materias (
    id_materia INT AUTO_INCREMENT PRIMARY KEY,
    nombre_materia VARCHAR(50) NOT NULL,
    nivel ENUM('inicial','primaria','secundaria') NOT NULL
);

CREATE TABLE IF NOT EXISTS profesores_cursos_materias (
    id_profesor INT NOT NULL,
    id_curso INT NOT NULL,
    id_materia INT NOT NULL,
    PRIMARY KEY (id_profesor, id_curso, id_materia),
    FOREIGN KEY (id_profesor) REFERENCES personas(id_persona),
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso),
    FOREIGN KEY (id_materia) REFERENCES materias(id_materia)
);

-- ================================
-- MÓDULO 4: RETIROS TEMPRANOS
-- ================================

CREATE TABLE IF NOT EXISTS retiros_tempranos (
    id_retiro INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    motivo VARCHAR(255),
    quien_retiro VARCHAR(50),
    fotografia BLOB,
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante)
);

-- ================================
-- MÓDULO 5: INCIDENTES / BIENESTAR ESTUDIANTIL
-- ================================

CREATE TABLE IF NOT EXISTS areas_incidente (
    id_area INT AUTO_INCREMENT PRIMARY KEY,
    nombre_area VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS situaciones_incidente (
    id_situacion INT AUTO_INCREMENT PRIMARY KEY,
    id_area INT NOT NULL,
    nombre_situacion VARCHAR(50) NOT NULL,
    nivel_gravedad ENUM('leve','grave','muy grave') NOT NULL,
    FOREIGN KEY (id_area) REFERENCES areas_incidente(id_area)
);

CREATE TABLE IF NOT EXISTS incidentes (
    id_incidente INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME NOT NULL,
    antecedentes TEXT,
    acciones_tomadas TEXT,
    seguimiento TEXT,
    estado ENUM('provisional','derivado','cerrado') NOT NULL
);

CREATE TABLE IF NOT EXISTS incidentes_estudiantes (
    id_incidente INT NOT NULL,
    id_estudiante INT NOT NULL,
    PRIMARY KEY (id_incidente, id_estudiante),
    FOREIGN KEY (id_incidente) REFERENCES incidentes(id_incidente),
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante)
);

CREATE TABLE IF NOT EXISTS incidentes_profesores (
    id_incidente INT NOT NULL,
    id_profesor INT NOT NULL,
    PRIMARY KEY (id_incidente, id_profesor),
    FOREIGN KEY (id_incidente) REFERENCES incidentes(id_incidente),
    FOREIGN KEY (id_profesor) REFERENCES personas(id_persona)
);

CREATE TABLE IF NOT EXISTS incidentes_situaciones (
    id_incidente INT NOT NULL,
    id_situacion INT NOT NULL,
    PRIMARY KEY (id_incidente, id_situacion),
    FOREIGN KEY (id_incidente) REFERENCES incidentes(id_incidente),
    FOREIGN KEY (id_situacion) REFERENCES situaciones_incidente(id_situacion)
);

-- ================================
-- MÓDULO 6: ESCUELAS / ESQUELAS
-- ================================

CREATE TABLE IF NOT EXISTS codigos_esquelas (
    id_codigo INT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('reconocimiento','orientacion') NOT NULL,
    codigo VARCHAR(10) NOT NULL,
    descripcion VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS esquelas (
    id_esquela INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    id_profesor INT NOT NULL,
    id_registrador INT NOT NULL,
    fecha DATE NOT NULL,
    observaciones TEXT,
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
    FOREIGN KEY (id_profesor) REFERENCES personas(id_persona),
    FOREIGN KEY (id_registrador) REFERENCES personas(id_persona)
);

CREATE TABLE IF NOT EXISTS esquelas_codigos (
    id_esquela INT NOT NULL,
    id_codigo INT NOT NULL,
    PRIMARY KEY (id_esquela, id_codigo),
    FOREIGN KEY (id_esquela) REFERENCES esquelas(id_esquela),
    FOREIGN KEY (id_codigo) REFERENCES codigos_esquelas(id_codigo)
);

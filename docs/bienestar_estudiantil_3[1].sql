-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-12-2025 a las 03:33:14
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bienestar_estudiantil_3`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `adjuntos`
--

CREATE TABLE `adjuntos` (
  `id_adjunto` int(11) NOT NULL,
  `id_incidente` int(11) NOT NULL,
  `nombre_archivo` varchar(200) DEFAULT NULL,
  `ruta` varchar(300) DEFAULT NULL,
  `tipo_mime` varchar(50) DEFAULT NULL,
  `id_subido_por` int(11) DEFAULT NULL,
  `fecha_subida` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `adjuntos`
--

INSERT INTO `adjuntos` (`id_adjunto`, `id_incidente`, `nombre_archivo`, `ruta`, `tipo_mime`, `id_subido_por`, `fecha_subida`) VALUES
(1, 1, '1200x630wa.jpg', 'uploads/incidentes/1/1200x630wa.jpg', 'image/jpeg', 1, '2025-11-23 23:37:49'),
(5, 3, 'images.png', 'uploads/incidentes/3/images.png', 'image/png', NULL, '2025-11-25 04:41:08'),
(6, 1, '4461.pdf', 'uploads/incidentes/1/4461.pdf', 'application/pdf', 1, '2025-11-25 22:52:54');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `areas_incidente`
--

CREATE TABLE `areas_incidente` (
  `id_area` int(11) NOT NULL,
  `nombre_area` varchar(50) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `areas_incidente`
--

INSERT INTO `areas_incidente` (`id_area`, `nombre_area`, `descripcion`) VALUES
(1, 'emocional', 'Aspectos emocionales del estudiante'),
(2, 'convivencia', 'Problemas de convivencia y disciplina'),
(3, 'familiar', 'Problemas en el entorno familiar'),
(4, 'salud integral', 'Aspectos relacionados a salud física o mental'),
(5, 'académica', 'Rendimiento académico'),
(9, 'hola', 'mundo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `codigos_esquelas`
--

CREATE TABLE `codigos_esquelas` (
  `id_codigo` int(11) NOT NULL,
  `tipo` enum('reconocimiento','orientacion') NOT NULL,
  `codigo` varchar(10) NOT NULL,
  `descripcion` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cursos`
--

CREATE TABLE `cursos` (
  `id_curso` int(11) NOT NULL,
  `nombre_curso` varchar(50) NOT NULL,
  `nivel` enum('inicial','primaria','secundaria') NOT NULL,
  `gestion` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cursos`
--

INSERT INTO `cursos` (`id_curso`, `nombre_curso`, `nivel`, `gestion`) VALUES
(1, '1A', 'primaria', '2025'),
(2, '1B', 'primaria', '2025'),
(3, '2A', 'primaria', '2025'),
(4, '2B', 'primaria', '2025'),
(5, '3A', 'primaria', '2025'),
(6, '3B', 'primaria', '2025'),
(7, '4A', 'primaria', '2025'),
(8, '4B', 'primaria', '2025'),
(9, 'Kínder A', 'inicial', '2025'),
(10, 'Kínder B', 'inicial', '2025');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `derivaciones`
--

CREATE TABLE `derivaciones` (
  `id_derivacion` int(11) NOT NULL,
  `id_incidente` int(11) NOT NULL,
  `id_quien_deriva` int(11) NOT NULL,
  `id_quien_recibe` int(11) NOT NULL,
  `fecha_derivacion` datetime NOT NULL DEFAULT current_timestamp(),
  `observaciones` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `derivaciones`
--

INSERT INTO `derivaciones` (`id_derivacion`, `id_incidente`, `id_quien_deriva`, `id_quien_recibe`, `fecha_derivacion`, `observaciones`) VALUES
(1, 1, 1, 2, '2025-11-25 02:58:17', 'hola mundo'),
(3, 3, 2, 10, '2025-11-25 04:41:30', 'viendo si funciona'),
(4, 1, 2, 10, '2025-11-25 14:52:20', 'Hola mundo'),
(5, 4, 2, 10, '2025-11-25 21:02:11', 'Derivaciones'),
(6, 3, 10, 5, '2025-11-25 22:33:49', 'nose'),
(7, 5, 10, 6, '2025-11-27 03:49:19', 'Es tu tema man'),
(8, 7, 10, 1, '2025-11-27 20:29:37', 'nio'),
(9, 8, 1, 10, '2025-11-28 00:21:53', 'Prueba de carlos'),
(10, 8, 10, 1, '2025-11-28 01:43:14', 'Prueba de notificacioens'),
(11, 11, 10, 1, '2025-12-01 03:32:35', 'No es muy complejo encargase usted');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `esquelas`
--

CREATE TABLE `esquelas` (
  `id_esquela` int(11) NOT NULL,
  `id_estudiante` int(11) NOT NULL,
  `id_profesor` int(11) NOT NULL,
  `id_registrador` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `observaciones` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `esquelas_codigos`
--

CREATE TABLE `esquelas_codigos` (
  `id_esquela` int(11) NOT NULL,
  `id_codigo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes`
--

CREATE TABLE `estudiantes` (
  `id_estudiante` int(11) NOT NULL,
  `ci` varchar(20) DEFAULT NULL,
  `nombres` varchar(50) NOT NULL,
  `apellido_paterno` varchar(50) NOT NULL,
  `apellido_materno` varchar(50) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `nombre_padre` varchar(50) DEFAULT NULL,
  `apellido_paterno_padre` varchar(50) DEFAULT NULL,
  `apellido_materno_padre` varchar(50) DEFAULT NULL,
  `telefono_padre` varchar(20) DEFAULT NULL,
  `nombre_madre` varchar(50) DEFAULT NULL,
  `apellido_paterno_madre` varchar(50) DEFAULT NULL,
  `apellido_materno_madre` varchar(50) DEFAULT NULL,
  `telefono_madre` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estudiantes`
--

INSERT INTO `estudiantes` (`id_estudiante`, `ci`, `nombres`, `apellido_paterno`, `apellido_materno`, `fecha_nacimiento`, `direccion`, `nombre_padre`, `apellido_paterno_padre`, `apellido_materno_padre`, `telefono_padre`, `nombre_madre`, `apellido_paterno_madre`, `apellido_materno_madre`, `telefono_madre`) VALUES
(1, '90001', 'Luis', 'Mendoza', 'Rojas', '2010-04-10', 'San Jorge', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(2, '90002', 'Andrea', 'Salazar', 'Vega', '2011-06-15', 'San Blas', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(3, '90003', 'Sofía', 'Guzmán', 'Torres', '2010-09-20', 'Tabladita', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(4, '90004', 'Diego', 'García', 'Mamani', '2012-01-12', 'Aranjuez', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(5, '90005', 'Daniela', 'Flores', 'Lopez', '2011-03-08', 'Miraflores', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(6, '90006', 'Jhon', 'Quispe', 'Suárez', '2010-11-22', 'Moto Méndez', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(7, '90007', 'Marcos', 'Vera', 'Choque', '2012-02-14', 'San Luis', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(8, '90008', 'Paola', 'Rivera', 'Ortiz', '2011-08-05', 'La Loma', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(9, '90009', 'Rafael', 'Ríos', 'Gutiérrez', '2010-07-17', 'San Bernardo', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(10, '90010', 'Camila', 'López', 'Cruz', '2011-12-29', 'Miguelito', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes_cursos`
--

CREATE TABLE `estudiantes_cursos` (
  `id_estudiante` int(11) NOT NULL,
  `id_curso` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial_de_modificaciones`
--

CREATE TABLE `historial_de_modificaciones` (
  `id_historial` int(11) NOT NULL,
  `id_incidente` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `fecha_cambio` datetime DEFAULT current_timestamp(),
  `campo_modificado` varchar(100) DEFAULT NULL,
  `valor_anterior` text DEFAULT NULL,
  `valor_nuevo` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `historial_de_modificaciones`
--

INSERT INTO `historial_de_modificaciones` (`id_historial`, `id_incidente`, `id_usuario`, `fecha_cambio`, `campo_modificado`, `valor_anterior`, `valor_nuevo`) VALUES
(1, 1, 1, '2025-11-23 21:07:43', 'antecedentes', NULL, 'Incidente1'),
(2, 1, 1, '2025-11-23 21:07:43', 'acciones_tomadas', NULL, NULL),
(3, 1, 1, '2025-11-23 21:07:43', 'seguimiento', NULL, NULL),
(4, 1, 1, '2025-11-23 21:07:43', 'estado', NULL, 'abierto'),
(5, 1, 1, '2025-11-23 21:07:43', 'id_responsable', NULL, '1'),
(6, 1, 1, '2025-11-23 21:29:30', 'antecedentes', 'Incidente1', 'Incidnetes1'),
(7, 1, 1, '2025-11-23 21:29:30', 'acciones_tomadas', NULL, ''),
(8, 1, 1, '2025-11-23 21:29:30', 'seguimiento', NULL, 'string'),
(9, 1, 1, '2025-11-23 21:30:21', 'estado', 'abierto', 'derivado'),
(10, 1, 2, '2025-11-23 21:53:24', 'acciones_tomadas', NULL, 'Preubas'),
(11, 2, 2, '2025-11-25 00:03:02', 'antecedentes', NULL, ''),
(12, 2, 2, '2025-11-25 00:03:02', 'acciones_tomadas', NULL, NULL),
(13, 2, 2, '2025-11-25 00:03:02', 'seguimiento', NULL, NULL),
(14, 2, 2, '2025-11-25 00:03:02', 'estado', NULL, 'abierto'),
(15, 2, 2, '2025-11-25 00:03:02', 'id_responsable', NULL, '2'),
(16, 2, 10, '2025-11-25 00:47:20', 'antecedentes', NULL, 'PruebadeModificacion'),
(17, 2, 10, '2025-11-25 00:47:20', 'acciones_tomadas', NULL, ''),
(18, 2, 10, '2025-11-25 00:47:20', 'seguimiento', NULL, ''),
(19, 1, 1, '2025-11-25 02:58:17', 'derivación', 'estado=derivado, id_responsable=1', 'estado=derivado, id_responsable=2'),
(20, 2, 10, '2025-11-25 03:14:56', 'derivación', 'estado=abierto, id_responsable=2', 'estado=derivado, id_responsable=10'),
(21, 1, 2, '2025-11-25 04:19:06', 'estado', 'derivado', 'cerrado'),
(22, 2, 10, '2025-11-25 04:22:10', 'estado', 'derivado', 'cerrado'),
(23, 1, 2, '2025-11-25 04:38:31', 'estado', 'cerrado', 'abierto'),
(24, 3, 2, '2025-11-25 04:40:32', 'antecedentes', NULL, 'Prueba de numero 3'),
(25, 3, 2, '2025-11-25 04:40:32', 'acciones_tomadas', NULL, 'resuelto'),
(26, 3, 2, '2025-11-25 04:40:32', 'seguimiento', NULL, NULL),
(27, 3, 2, '2025-11-25 04:40:32', 'estado', NULL, 'abierto'),
(28, 3, 2, '2025-11-25 04:40:32', 'id_responsable', NULL, '2'),
(29, 3, 2, '2025-11-25 04:40:40', 'seguimiento', NULL, 'funciona'),
(30, 3, 2, '2025-11-25 04:41:30', 'derivación', 'estado=abierto, id_responsable=2', 'estado=derivado, id_responsable=10'),
(31, 1, 2, '2025-11-25 14:51:50', 'estado', 'abierto', 'cerrado'),
(32, 1, 2, '2025-11-25 14:51:56', 'estado', 'cerrado', 'abierto'),
(33, 1, 2, '2025-11-25 14:52:20', 'derivación', 'estado=abierto, id_responsable=2', 'estado=derivado, id_responsable=10'),
(34, 4, 2, '2025-11-25 21:01:58', 'antecedentes', NULL, 'Derivaciones'),
(35, 4, 2, '2025-11-25 21:01:58', 'acciones_tomadas', NULL, NULL),
(36, 4, 2, '2025-11-25 21:01:58', 'seguimiento', NULL, NULL),
(37, 4, 2, '2025-11-25 21:01:58', 'estado', NULL, 'abierto'),
(38, 4, 2, '2025-11-25 21:01:58', 'id_responsable', NULL, '2'),
(39, 4, 2, '2025-11-25 21:02:11', 'derivación', 'estado=abierto, id_responsable=2', 'estado=derivado, id_responsable=10'),
(40, 1, 10, '2025-11-25 21:02:28', 'estado', 'derivado', 'cerrado'),
(41, 1, 10, '2025-11-25 21:02:32', 'estado', 'cerrado', 'abierto'),
(42, 4, 10, '2025-11-25 21:27:34', 'estado', 'derivado', 'cerrado'),
(43, 3, 10, '2025-11-25 22:33:49', 'derivación', 'estado=derivado, id_responsable=10', 'estado=derivado, id_responsable=5'),
(44, 1, 10, '2025-11-25 22:34:17', 'estado', 'abierto', 'cerrado'),
(45, 1, 10, '2025-11-25 22:34:25', 'estado', 'cerrado', 'abierto'),
(46, 5, 10, '2025-11-25 22:35:34', 'antecedentes', NULL, 'la niña estaba triste en el salón'),
(47, 5, 10, '2025-11-25 22:35:34', 'acciones_tomadas', NULL, NULL),
(48, 5, 10, '2025-11-25 22:35:34', 'seguimiento', NULL, NULL),
(49, 5, 10, '2025-11-25 22:35:34', 'estado', NULL, 'abierto'),
(50, 5, 10, '2025-11-25 22:35:34', 'id_responsable', NULL, '10'),
(51, 6, 1, '2025-11-25 22:42:44', 'antecedentes', NULL, 'Presentación'),
(52, 6, 1, '2025-11-25 22:42:44', 'acciones_tomadas', NULL, 'DeLaCreación'),
(53, 6, 1, '2025-11-25 22:42:44', 'seguimiento', NULL, 'DeUnIncidente'),
(54, 6, 1, '2025-11-25 22:42:44', 'estado', NULL, 'abierto'),
(55, 6, 1, '2025-11-25 22:42:44', 'id_responsable', NULL, '1'),
(56, 6, 3, '2025-11-25 22:47:17', 'antecedentes', 'Presentación', 'string'),
(57, 6, 3, '2025-11-25 22:47:17', 'acciones_tomadas', 'DeLaCreación', 'string'),
(58, 6, 3, '2025-11-25 22:47:17', 'seguimiento', 'DeUnIncidente', 'string'),
(59, 6, 3, '2025-11-25 22:47:17', 'id_responsable', '1', '3'),
(60, 5, 10, '2025-11-27 03:40:11', 'estado', 'abierto', 'cerrado'),
(61, 5, 10, '2025-11-27 03:49:02', 'estado', 'cerrado', 'abierto'),
(62, 5, 10, '2025-11-27 03:49:19', 'derivación', 'estado=abierto, id_responsable=10', 'estado=derivado, id_responsable=6'),
(63, 4, 10, '2025-11-27 03:51:08', 'estado', 'cerrado', 'abierto'),
(64, 4, 10, '2025-11-27 03:51:11', 'estado', 'abierto', 'cerrado'),
(65, 7, 10, '2025-11-27 18:15:45', 'acciones_tomadas', NULL, 'Prueba de modificaciones'),
(66, 7, 10, '2025-11-27 18:15:45', 'seguimiento', NULL, 'Prueba de modificaciones'),
(67, 7, 10, '2025-11-27 20:29:37', 'derivación', 'estado=abierto, id_responsable=10', 'estado=derivado, id_responsable=1'),
(68, 2, 10, '2025-11-28 00:20:40', 'estado', 'cerrado', 'abierto'),
(69, 8, 1, '2025-11-28 00:21:53', 'derivación', 'estado=abierto, id_responsable=1', 'estado=derivado, id_responsable=10'),
(70, 8, 10, '2025-11-28 01:43:14', 'derivación', 'estado=derivado, id_responsable=10', 'estado=derivado, id_responsable=1'),
(71, 8, 1, '2025-11-28 02:09:47', 'estado', 'derivado', 'cerrado'),
(72, 8, 1, '2025-11-28 02:10:00', 'estado', 'cerrado', 'abierto'),
(73, 10, 6, '2025-11-28 02:18:32', 'antecedentes', 'orem ipsum es el texto que se usa habitualmente en diseño gráfico en demostraciones de tipografías o de bocetos para diseños para probar el arte visual antes de insertar el texto final.\n\nAunque no posee actualmente fuentes para justificar sus hipótesis, el profesor de filología clásica Richard McClintock asegura que su uso se remonta a los impresores de comienzos del siglo XVI.[1]​ Su uso en algunos editores de texto muy conocidos en la actualidad ha dado al texto lorem ipsum nueva popularidad.\n\nEl texto en sí no tiene sentido aparente, aunque no es aleatorio, sino que deriva de un texto de Cicerón en lengua latina, a cuyas palabras se les han eliminado sílabas o letras. El significado del mismo no tiene importancia, ya que solo es una demostración o prueba. El texto procede de la obra De finibus bonorum et malorum (Sobre los límites del bien y del mal) que comienza con:\n\nNeque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit\nA nadie le gusta el dolor para sí mismo, o lo busca y desea tenerlo, apenas porque es dolor...\nDe finibus bonorum et malorum, de Marco Tulio Cicerón\nA pesar de estar extraído de ese escrito, el texto usado habitualmente[cita requerida] es:\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\nExisten múltiples variantes del texto original, algunas casi sin parecido con este. Estas versiones incluyen letras adicionales que no son comunes en latín (como la k, w y z) o palabras sin sentido como zzril, takimata y gubeergren que intentan hacer la distribución aún más parecida al inglés.\n\nVarios editores de texto proveen la funcionalidad de generación de lorem ipsum.\n\nVéase también', 'hola'),
(74, 10, 6, '2025-11-28 02:18:32', 'acciones_tomadas', 'orem ipsum es el texto que se usa habitualmente en diseño gráfico en demostraciones de tipografías o de bocetos para diseños para probar el arte visual antes de insertar el texto final.\n\nAunque no posee actualmente fuentes para justificar sus hipótesis, el profesor de filología clásica Richard McClintock asegura que su uso se remonta a los impresores de comienzos del siglo XVI.[1]​ Su uso en algunos editores de texto muy conocidos en la actualidad ha dado al texto lorem ipsum nueva popularidad.\n\nEl texto en sí no tiene sentido aparente, aunque no es aleatorio, sino que deriva de un texto de Cicerón en lengua latina, a cuyas palabras se les han eliminado sílabas o letras. El significado del mismo no tiene importancia, ya que solo es una demostración o prueba. El texto procede de la obra De finibus bonorum et malorum (Sobre los límites del bien y del mal) que comienza con:\n\nNeque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit\nA nadie le gusta el dolor para sí mismo, o lo busca y desea tenerlo, apenas porque es dolor...\nDe finibus bonorum et malorum, de Marco Tulio Cicerón\nA pesar de estar extraído de ese escrito, el texto usado habitualmente[cita requerida] es:\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\nExisten múltiples variantes del texto original, algunas casi sin parecido con este. Estas versiones incluyen letras adicionales que no son comunes en latín (como la k, w y z) o palabras sin sentido como zzril, takimata y gubeergren que intentan hacer la distribución aún más parecida al inglés.\n\nVarios editores de texto proveen la funcionalidad de generación de lorem ipsum.\n\nVéase también', 'mundo'),
(75, 10, 6, '2025-11-28 02:18:32', 'seguimiento', NULL, 'pancho'),
(76, 11, 10, '2025-12-01 03:31:19', 'acciones_tomadas', NULL, 'Llamar a los padres'),
(77, 11, 10, '2025-12-01 03:31:37', 'seguimiento', NULL, 'No volvio a ocurrir'),
(78, 11, 10, '2025-12-01 03:32:35', 'derivación', 'estado=abierto, id_responsable=10', 'estado=derivado, id_responsable=1'),
(79, 4, 10, '2025-12-01 03:33:24', 'estado', 'cerrado', 'abierto');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `incidentes`
--

CREATE TABLE `incidentes` (
  `id_incidente` int(11) NOT NULL,
  `fecha` datetime NOT NULL,
  `antecedentes` text DEFAULT NULL,
  `acciones_tomadas` text DEFAULT NULL,
  `seguimiento` text DEFAULT NULL,
  `estado` enum('abierto','derivado','cerrado') NOT NULL,
  `id_responsable` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `incidentes`
--

INSERT INTO `incidentes` (`id_incidente`, `fecha`, `antecedentes`, `acciones_tomadas`, `seguimiento`, `estado`, `id_responsable`) VALUES
(1, '2025-11-23 21:07:43', 'Incidnetes1', 'Preubas', 'string', 'abierto', 10),
(2, '2025-11-25 00:03:02', 'PruebadeModificacion', '', '', 'abierto', 10),
(3, '2025-11-25 04:40:32', 'Prueba de numero 3', 'resuelto', 'funciona', 'derivado', 5),
(4, '2025-11-25 21:01:58', 'Derivaciones', NULL, NULL, 'abierto', 10),
(5, '2025-11-25 22:35:34', 'la niña estaba triste en el salón', NULL, NULL, 'derivado', 6),
(6, '2025-11-25 21:16:36', 'string', 'string', 'string', 'abierto', 3),
(7, '2025-11-27 18:14:47', 'Prueba27', 'Prueba de modificaciones', 'Prueba de modificaciones', 'derivado', 1),
(8, '2025-11-28 00:21:07', 'Prueba para carlos', NULL, NULL, 'abierto', 1),
(9, '2025-11-28 02:11:58', 'PruebaDeTesteo', 'Acciones Tomadas', NULL, 'abierto', 1),
(10, '2025-11-28 02:17:42', 'hola', 'mundo', 'pancho', 'abierto', 6),
(11, '2025-12-01 03:30:38', 'Presentacion de incidente', 'Llamar a los padres', 'No volvio a ocurrir', 'derivado', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `incidentes_estudiantes`
--

CREATE TABLE `incidentes_estudiantes` (
  `id_incidente` int(11) NOT NULL,
  `id_estudiante` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `incidentes_estudiantes`
--

INSERT INTO `incidentes_estudiantes` (`id_incidente`, `id_estudiante`) VALUES
(1, 1),
(1, 2),
(2, 1),
(2, 2),
(3, 1),
(3, 2),
(4, 1),
(4, 2),
(5, 8),
(6, 1),
(6, 2),
(6, 3),
(7, 1),
(7, 2),
(8, 1),
(9, 1),
(9, 2),
(10, 1),
(10, 2),
(10, 3),
(10, 5),
(10, 6),
(10, 8),
(10, 9),
(10, 10),
(11, 1),
(11, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `incidentes_profesores`
--

CREATE TABLE `incidentes_profesores` (
  `id_incidente` int(11) NOT NULL,
  `id_profesor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `incidentes_profesores`
--

INSERT INTO `incidentes_profesores` (`id_incidente`, `id_profesor`) VALUES
(2, 2),
(2, 3),
(3, 6),
(3, 8),
(4, 2),
(6, 2),
(6, 3),
(7, 2),
(8, 3),
(9, 3),
(9, 6),
(10, 2),
(10, 3),
(10, 6),
(10, 8);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `incidentes_situaciones`
--

CREATE TABLE `incidentes_situaciones` (
  `id_incidente` int(11) NOT NULL,
  `id_situacion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `incidentes_situaciones`
--

INSERT INTO `incidentes_situaciones` (`id_incidente`, `id_situacion`) VALUES
(1, 4),
(2, 2),
(3, 1),
(3, 2),
(4, 2),
(5, 1),
(6, 2),
(6, 3),
(6, 4),
(7, 1),
(8, 1),
(9, 1),
(9, 2),
(9, 9),
(9, 10),
(10, 1),
(10, 2),
(10, 3),
(10, 6),
(10, 7),
(10, 10),
(11, 1),
(11, 2),
(11, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `login_logs`
--

CREATE TABLE `login_logs` (
  `id_log` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `fecha_hora` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materias`
--

CREATE TABLE `materias` (
  `id_materia` int(11) NOT NULL,
  `nombre_materia` varchar(50) NOT NULL,
  `nivel` enum('inicial','primaria','secundaria') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `materias`
--

INSERT INTO `materias` (`id_materia`, `nombre_materia`, `nivel`) VALUES
(1, 'Matemática', 'primaria'),
(2, 'Lenguaje', 'primaria'),
(3, 'Ciencias Naturales', 'primaria'),
(4, 'Sociales', 'primaria'),
(5, 'Inglés', 'primaria'),
(6, 'Física', 'secundaria'),
(7, 'Química', 'secundaria'),
(8, 'Biología', 'secundaria'),
(9, 'Arte', 'primaria'),
(10, 'Música', 'primaria');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notificaciones`
--

CREATE TABLE `notificaciones` (
  `id_notificacion` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_incidente` int(11) DEFAULT NULL,
  `id_derivacion` int(11) DEFAULT NULL,
  `titulo` varchar(150) NOT NULL,
  `mensaje` text NOT NULL,
  `leido` tinyint(1) DEFAULT 0,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `notificaciones`
--

INSERT INTO `notificaciones` (`id_notificacion`, `id_usuario`, `id_incidente`, `id_derivacion`, `titulo`, `mensaje`, `leido`, `fecha`) VALUES
(1, 1, 8, 10, 'Incidente derivado', 'Se le ha derivado el incidente #8 para su atención.', 0, '2025-11-28 01:43:14'),
(2, 1, 11, 11, 'Incidente derivado', 'No es muy complejo encargase usted', 0, '2025-12-01 03:32:35');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permisos`
--

CREATE TABLE `permisos` (
  `id_permiso` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `permisos`
--

INSERT INTO `permisos` (`id_permiso`, `nombre`, `descripcion`) VALUES
(1, 'crear_incidente', 'Puede crear incidentes'),
(2, 'editar_incidente', 'Puede modificar incidentes'),
(3, 'ver_incidente', 'Puede ver incidentes'),
(4, 'derivar_incidente', 'Puede derivar incidentes'),
(5, 'cerrar_incidente', 'Puede cerrar incidentes'),
(6, 'gestionar_estudiantes', 'Puede gestionar estudiantes'),
(7, 'subir_adjuntos', 'Puede adjuntar archivos'),
(8, 'ver_historial', 'Puede ver historial'),
(9, 'ver_reportes', 'Puede ver reportes'),
(10, 'admin_total', 'Administrador total');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `personas`
--

CREATE TABLE `personas` (
  `id_persona` int(11) NOT NULL,
  `ci` varchar(20) NOT NULL,
  `nombres` varchar(50) NOT NULL,
  `apellido_paterno` varchar(50) NOT NULL,
  `apellido_materno` varchar(50) NOT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `tipo_persona` enum('profesor','administrativo') NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `personas`
--

INSERT INTO `personas` (`id_persona`, `ci`, `nombres`, `apellido_paterno`, `apellido_materno`, `direccion`, `telefono`, `correo`, `tipo_persona`, `is_active`) VALUES
(1, '1234561', 'Carlos', 'Gonzales', 'Mamani', 'Barrio La Loma', '72811111', 'carlos@correo.com', 'administrativo', 1),
(2, '1234562', 'Juan', 'Flores', 'Perez', 'San Roque', '72822222', 'juan@correo.com', 'profesor', 1),
(3, '1234563', 'María', 'Rojas', 'Gutiérrez', 'San Bernardo', '72833333', 'maria@correo.com', 'profesor', 1),
(4, '1234564', 'Jorge', 'Vargas', 'Rivera', 'Moto Mendez', '72844444', 'jorge@correo.com', 'administrativo', 1),
(5, '1234565', 'Lucía', 'Suarez', 'Ortiz', 'Méndez Arcos', '72855555', 'lucia@correo.com', 'administrativo', 1),
(6, '1234566', 'Pedro', 'Carvajal', 'López', 'San Blas', '72866666', 'pedro@correo.com', 'profesor', 1),
(7, '1234567', 'Ana', 'Fernández', 'Choque', 'San Jorge', '72877777', 'ana@correo.com', 'administrativo', 1),
(8, '1234568', 'Miguel', 'Paredes', 'Molina', 'Tabladita', '72888888', 'miguel@correo.com', 'profesor', 1),
(9, '1234569', 'Laura', 'Torrez', 'Castillo', 'Aranjuez', '72899999', 'laura@correo.com', 'administrativo', 1),
(10, '1234570', 'Elena', 'Mamani', 'Cruz', 'Miraflores', '72900000', 'elena@correo.com', 'profesor', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profesores_cursos_materias`
--

CREATE TABLE `profesores_cursos_materias` (
  `id_profesor` int(11) NOT NULL,
  `id_curso` int(11) NOT NULL,
  `id_materia` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `profesores_cursos_materias`
--

INSERT INTO `profesores_cursos_materias` (`id_profesor`, `id_curso`, `id_materia`) VALUES
(2, 1, 1),
(2, 6, 6),
(3, 2, 2),
(3, 7, 7),
(6, 3, 3),
(6, 8, 8),
(8, 4, 4),
(8, 9, 9),
(10, 5, 5),
(10, 10, 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `retiros_tempranos`
--

CREATE TABLE `retiros_tempranos` (
  `id_retiro` int(11) NOT NULL,
  `id_estudiante` int(11) NOT NULL,
  `fecha_hora` datetime NOT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  `quien_retiro` varchar(50) DEFAULT NULL,
  `fotografia` blob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `nombre`, `descripcion`) VALUES
(1, 'gerente_profesores', 'Gerente o profesor responsable'),
(2, 'bienestar_estudiantil', 'Equipo de bienestar estudiantil'),
(3, 'director_de_nivel', 'Dirección de nivel académico'),
(4, 'director_general', 'Dirección general');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol_permisos`
--

CREATE TABLE `rol_permisos` (
  `id_rol` int(11) NOT NULL,
  `id_permiso` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `rol_permisos`
--

INSERT INTO `rol_permisos` (`id_rol`, `id_permiso`) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 6),
(2, 1),
(2, 2),
(2, 3),
(2, 4),
(2, 5),
(2, 6),
(3, 1),
(3, 2),
(3, 3),
(3, 4),
(3, 5),
(3, 6),
(3, 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `situaciones_incidente`
--

CREATE TABLE `situaciones_incidente` (
  `id_situacion` int(11) NOT NULL,
  `id_area` int(11) NOT NULL,
  `nombre_situacion` varchar(50) NOT NULL,
  `nivel_gravedad` enum('leve','grave','muy grave') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `situaciones_incidente`
--

INSERT INTO `situaciones_incidente` (`id_situacion`, `id_area`, `nombre_situacion`, `nivel_gravedad`) VALUES
(1, 1, 'tristeza persistente', 'leve'),
(2, 1, 'llanto en clase', 'grave'),
(3, 2, 'discusión entre compañeros', 'leve'),
(4, 2, 'agresión física', 'muy grave'),
(5, 3, 'problemas en casa', 'grave'),
(6, 3, 'violencia intrafamiliar', 'muy grave'),
(7, 4, 'dolor de cabeza frecuente', 'leve'),
(8, 4, 'desmayo en clase', 'grave'),
(9, 5, 'bajo rendimiento', 'leve'),
(10, 5, 'copia en examen', 'grave'),
(12, 5, 'hola mundo', 'grave'),
(14, 2, 'Pruebasdesituacion', 'leve');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `id_persona` int(11) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `id_persona`, `usuario`, `correo`, `password`) VALUES
(1, 1, 'carlos', 'carlos@correo.com', '1234'),
(2, 2, 'juan', 'juan@correo.com', '1234'),
(3, 3, 'maria', 'maria@correo.com', '1234'),
(4, 4, 'jorge', 'jorge@correo.com', '1234'),
(5, 5, 'lucia', 'lucia@correo.com', '1234'),
(6, 6, 'pedro', 'pedro@correo.com', '1234'),
(7, 7, 'ana', 'ana@correo.com', '1234'),
(8, 8, 'miguel', 'miguel@correo.com', '1234'),
(9, 9, 'laura', 'laura@correo.com', '1234'),
(10, 10, 'elena', 'elena@correo.com', '1234');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_roles`
--

CREATE TABLE `usuario_roles` (
  `id_usuario` int(11) NOT NULL,
  `id_rol` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date DEFAULT NULL,
  `estado` enum('activo','inactivo') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario_roles`
--

INSERT INTO `usuario_roles` (`id_usuario`, `id_rol`, `fecha_inicio`, `fecha_fin`, `estado`) VALUES
(1, 1, '2025-01-01', NULL, 'activo'),
(2, 1, '2025-01-01', NULL, 'activo'),
(3, 1, '2025-01-01', NULL, 'activo'),
(4, 2, '2025-01-01', NULL, 'activo'),
(5, 2, '2025-01-01', NULL, 'activo'),
(6, 2, '2025-01-01', NULL, 'activo'),
(7, 3, '2025-01-01', NULL, 'activo'),
(8, 3, '2025-01-01', NULL, 'activo'),
(9, 3, '2025-01-01', NULL, 'activo'),
(10, 3, '2025-01-01', NULL, 'activo');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `adjuntos`
--
ALTER TABLE `adjuntos`
  ADD PRIMARY KEY (`id_adjunto`),
  ADD KEY `id_subido_por` (`id_subido_por`),
  ADD KEY `adjuntos_ibfk_1` (`id_incidente`);

--
-- Indices de la tabla `areas_incidente`
--
ALTER TABLE `areas_incidente`
  ADD PRIMARY KEY (`id_area`);

--
-- Indices de la tabla `codigos_esquelas`
--
ALTER TABLE `codigos_esquelas`
  ADD PRIMARY KEY (`id_codigo`);

--
-- Indices de la tabla `cursos`
--
ALTER TABLE `cursos`
  ADD PRIMARY KEY (`id_curso`);

--
-- Indices de la tabla `derivaciones`
--
ALTER TABLE `derivaciones`
  ADD PRIMARY KEY (`id_derivacion`),
  ADD KEY `id_incidente` (`id_incidente`),
  ADD KEY `id_quien_deriva` (`id_quien_deriva`),
  ADD KEY `id_quien_recibe` (`id_quien_recibe`);

--
-- Indices de la tabla `esquelas`
--
ALTER TABLE `esquelas`
  ADD PRIMARY KEY (`id_esquela`),
  ADD KEY `id_estudiante` (`id_estudiante`),
  ADD KEY `id_profesor` (`id_profesor`),
  ADD KEY `id_registrador` (`id_registrador`);

--
-- Indices de la tabla `esquelas_codigos`
--
ALTER TABLE `esquelas_codigos`
  ADD PRIMARY KEY (`id_esquela`,`id_codigo`),
  ADD KEY `id_codigo` (`id_codigo`);

--
-- Indices de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD PRIMARY KEY (`id_estudiante`);

--
-- Indices de la tabla `estudiantes_cursos`
--
ALTER TABLE `estudiantes_cursos`
  ADD PRIMARY KEY (`id_estudiante`,`id_curso`),
  ADD KEY `id_curso` (`id_curso`);

--
-- Indices de la tabla `historial_de_modificaciones`
--
ALTER TABLE `historial_de_modificaciones`
  ADD PRIMARY KEY (`id_historial`),
  ADD KEY `id_incidente` (`id_incidente`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `incidentes`
--
ALTER TABLE `incidentes`
  ADD PRIMARY KEY (`id_incidente`),
  ADD KEY `fk_incidentes_responsable` (`id_responsable`);

--
-- Indices de la tabla `incidentes_estudiantes`
--
ALTER TABLE `incidentes_estudiantes`
  ADD PRIMARY KEY (`id_incidente`,`id_estudiante`),
  ADD KEY `id_estudiante` (`id_estudiante`);

--
-- Indices de la tabla `incidentes_profesores`
--
ALTER TABLE `incidentes_profesores`
  ADD PRIMARY KEY (`id_incidente`,`id_profesor`),
  ADD KEY `id_profesor` (`id_profesor`);

--
-- Indices de la tabla `incidentes_situaciones`
--
ALTER TABLE `incidentes_situaciones`
  ADD PRIMARY KEY (`id_incidente`,`id_situacion`),
  ADD KEY `id_situacion` (`id_situacion`);

--
-- Indices de la tabla `login_logs`
--
ALTER TABLE `login_logs`
  ADD PRIMARY KEY (`id_log`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `materias`
--
ALTER TABLE `materias`
  ADD PRIMARY KEY (`id_materia`);

--
-- Indices de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD PRIMARY KEY (`id_notificacion`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_incidente` (`id_incidente`),
  ADD KEY `id_derivacion` (`id_derivacion`);

--
-- Indices de la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD PRIMARY KEY (`id_permiso`);

--
-- Indices de la tabla `personas`
--
ALTER TABLE `personas`
  ADD PRIMARY KEY (`id_persona`);

--
-- Indices de la tabla `profesores_cursos_materias`
--
ALTER TABLE `profesores_cursos_materias`
  ADD PRIMARY KEY (`id_profesor`,`id_curso`,`id_materia`),
  ADD KEY `id_curso` (`id_curso`),
  ADD KEY `id_materia` (`id_materia`);

--
-- Indices de la tabla `retiros_tempranos`
--
ALTER TABLE `retiros_tempranos`
  ADD PRIMARY KEY (`id_retiro`),
  ADD KEY `id_estudiante` (`id_estudiante`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `rol_permisos`
--
ALTER TABLE `rol_permisos`
  ADD PRIMARY KEY (`id_rol`,`id_permiso`),
  ADD KEY `id_permiso` (`id_permiso`);

--
-- Indices de la tabla `situaciones_incidente`
--
ALTER TABLE `situaciones_incidente`
  ADD PRIMARY KEY (`id_situacion`),
  ADD KEY `id_area` (`id_area`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `usuario` (`usuario`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD KEY `id_persona` (`id_persona`);

--
-- Indices de la tabla `usuario_roles`
--
ALTER TABLE `usuario_roles`
  ADD PRIMARY KEY (`id_usuario`,`id_rol`,`fecha_inicio`),
  ADD KEY `id_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `adjuntos`
--
ALTER TABLE `adjuntos`
  MODIFY `id_adjunto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `areas_incidente`
--
ALTER TABLE `areas_incidente`
  MODIFY `id_area` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `codigos_esquelas`
--
ALTER TABLE `codigos_esquelas`
  MODIFY `id_codigo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cursos`
--
ALTER TABLE `cursos`
  MODIFY `id_curso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `derivaciones`
--
ALTER TABLE `derivaciones`
  MODIFY `id_derivacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `esquelas`
--
ALTER TABLE `esquelas`
  MODIFY `id_esquela` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  MODIFY `id_estudiante` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `historial_de_modificaciones`
--
ALTER TABLE `historial_de_modificaciones`
  MODIFY `id_historial` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=80;

--
-- AUTO_INCREMENT de la tabla `incidentes`
--
ALTER TABLE `incidentes`
  MODIFY `id_incidente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `login_logs`
--
ALTER TABLE `login_logs`
  MODIFY `id_log` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `materias`
--
ALTER TABLE `materias`
  MODIFY `id_materia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  MODIFY `id_notificacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `permisos`
--
ALTER TABLE `permisos`
  MODIFY `id_permiso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `personas`
--
ALTER TABLE `personas`
  MODIFY `id_persona` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `retiros_tempranos`
--
ALTER TABLE `retiros_tempranos`
  MODIFY `id_retiro` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `situaciones_incidente`
--
ALTER TABLE `situaciones_incidente`
  MODIFY `id_situacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `adjuntos`
--
ALTER TABLE `adjuntos`
  ADD CONSTRAINT `adjuntos_ibfk_1` FOREIGN KEY (`id_incidente`) REFERENCES `incidentes` (`id_incidente`) ON DELETE CASCADE,
  ADD CONSTRAINT `adjuntos_ibfk_2` FOREIGN KEY (`id_subido_por`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `derivaciones`
--
ALTER TABLE `derivaciones`
  ADD CONSTRAINT `derivaciones_ibfk_1` FOREIGN KEY (`id_incidente`) REFERENCES `incidentes` (`id_incidente`),
  ADD CONSTRAINT `derivaciones_ibfk_2` FOREIGN KEY (`id_quien_deriva`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `derivaciones_ibfk_3` FOREIGN KEY (`id_quien_recibe`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `esquelas`
--
ALTER TABLE `esquelas`
  ADD CONSTRAINT `esquelas_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`),
  ADD CONSTRAINT `esquelas_ibfk_2` FOREIGN KEY (`id_profesor`) REFERENCES `personas` (`id_persona`),
  ADD CONSTRAINT `esquelas_ibfk_3` FOREIGN KEY (`id_registrador`) REFERENCES `personas` (`id_persona`);

--
-- Filtros para la tabla `esquelas_codigos`
--
ALTER TABLE `esquelas_codigos`
  ADD CONSTRAINT `esquelas_codigos_ibfk_1` FOREIGN KEY (`id_esquela`) REFERENCES `esquelas` (`id_esquela`),
  ADD CONSTRAINT `esquelas_codigos_ibfk_2` FOREIGN KEY (`id_codigo`) REFERENCES `codigos_esquelas` (`id_codigo`);

--
-- Filtros para la tabla `estudiantes_cursos`
--
ALTER TABLE `estudiantes_cursos`
  ADD CONSTRAINT `estudiantes_cursos_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`),
  ADD CONSTRAINT `estudiantes_cursos_ibfk_2` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`);

--
-- Filtros para la tabla `historial_de_modificaciones`
--
ALTER TABLE `historial_de_modificaciones`
  ADD CONSTRAINT `historial_de_modificaciones_ibfk_1` FOREIGN KEY (`id_incidente`) REFERENCES `incidentes` (`id_incidente`),
  ADD CONSTRAINT `historial_de_modificaciones_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `incidentes`
--
ALTER TABLE `incidentes`
  ADD CONSTRAINT `fk_incidentes_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `incidentes_estudiantes`
--
ALTER TABLE `incidentes_estudiantes`
  ADD CONSTRAINT `incidentes_estudiantes_ibfk_1` FOREIGN KEY (`id_incidente`) REFERENCES `incidentes` (`id_incidente`),
  ADD CONSTRAINT `incidentes_estudiantes_ibfk_2` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`);

--
-- Filtros para la tabla `incidentes_profesores`
--
ALTER TABLE `incidentes_profesores`
  ADD CONSTRAINT `incidentes_profesores_ibfk_1` FOREIGN KEY (`id_incidente`) REFERENCES `incidentes` (`id_incidente`),
  ADD CONSTRAINT `incidentes_profesores_ibfk_2` FOREIGN KEY (`id_profesor`) REFERENCES `personas` (`id_persona`);

--
-- Filtros para la tabla `incidentes_situaciones`
--
ALTER TABLE `incidentes_situaciones`
  ADD CONSTRAINT `incidentes_situaciones_ibfk_1` FOREIGN KEY (`id_incidente`) REFERENCES `incidentes` (`id_incidente`),
  ADD CONSTRAINT `incidentes_situaciones_ibfk_2` FOREIGN KEY (`id_situacion`) REFERENCES `situaciones_incidente` (`id_situacion`);

--
-- Filtros para la tabla `login_logs`
--
ALTER TABLE `login_logs`
  ADD CONSTRAINT `login_logs_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD CONSTRAINT `notificaciones_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `notificaciones_ibfk_2` FOREIGN KEY (`id_incidente`) REFERENCES `incidentes` (`id_incidente`),
  ADD CONSTRAINT `notificaciones_ibfk_3` FOREIGN KEY (`id_derivacion`) REFERENCES `derivaciones` (`id_derivacion`);

--
-- Filtros para la tabla `profesores_cursos_materias`
--
ALTER TABLE `profesores_cursos_materias`
  ADD CONSTRAINT `profesores_cursos_materias_ibfk_1` FOREIGN KEY (`id_profesor`) REFERENCES `personas` (`id_persona`),
  ADD CONSTRAINT `profesores_cursos_materias_ibfk_2` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`),
  ADD CONSTRAINT `profesores_cursos_materias_ibfk_3` FOREIGN KEY (`id_materia`) REFERENCES `materias` (`id_materia`);

--
-- Filtros para la tabla `retiros_tempranos`
--
ALTER TABLE `retiros_tempranos`
  ADD CONSTRAINT `retiros_tempranos_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`);

--
-- Filtros para la tabla `rol_permisos`
--
ALTER TABLE `rol_permisos`
  ADD CONSTRAINT `rol_permisos_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`),
  ADD CONSTRAINT `rol_permisos_ibfk_2` FOREIGN KEY (`id_permiso`) REFERENCES `permisos` (`id_permiso`);

--
-- Filtros para la tabla `situaciones_incidente`
--
ALTER TABLE `situaciones_incidente`
  ADD CONSTRAINT `situaciones_incidente_ibfk_1` FOREIGN KEY (`id_area`) REFERENCES `areas_incidente` (`id_area`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_persona`) REFERENCES `personas` (`id_persona`);

--
-- Filtros para la tabla `usuario_roles`
--
ALTER TABLE `usuario_roles`
  ADD CONSTRAINT `usuario_roles_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `usuario_roles_ibfk_2` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

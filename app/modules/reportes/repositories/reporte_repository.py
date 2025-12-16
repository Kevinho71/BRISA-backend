# app/modules/reportes/repositories/reporte_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import func, case, or_, and_
from app.modules.esquelas.models.esquela_models import Esquela, CodigoEsquela, EsquelaCodigo
from app.modules.administracion.models.persona_models import (
    Estudiante, estudiantes_cursos, profesores_cursos_materias
)
from app.modules.estudiantes.models import Curso, Materia
from app.shared.models.persona import Persona
from datetime import date, datetime
from typing import Optional, Literal, List


from app.shared.models.profesor_curso_materia import ProfesorCursoMateria


class ReporteRepository:

    @staticmethod
    def get_ranking_estudiantes(
        db: Session,
        tipo: Optional[str] = None,
        limit: int = 10,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        id_registrador: Optional[int] = None
    ):
        """
        Obtiene ranking de estudiantes por cantidad de esquelas
        """
        # Join con esquelas_codigos explícitamente
        query = db.query(
            Estudiante.id_estudiante,
            Estudiante.nombres,
            Estudiante.apellido_paterno,
            Estudiante.apellido_materno,
            func.count(func.distinct(Esquela.id_esquela)).label('total'),
            func.sum(
                case((CodigoEsquela.tipo == 'reconocimiento', 1), else_=0)
            ).label('reconocimiento'),
            func.sum(
                case((CodigoEsquela.tipo == 'orientacion', 1), else_=0)
            ).label('orientacion')
        ).join(
            Esquela, Estudiante.id_estudiante == Esquela.id_estudiante
        ).join(
            EsquelaCodigo, Esquela.id_esquela == EsquelaCodigo.id_esquela
        ).join(
            CodigoEsquela, EsquelaCodigo.id_codigo == CodigoEsquela.id_codigo
        )

        # Filtros de fecha
        if fecha_desde:
            query = query.filter(Esquela.fecha >= fecha_desde)
        if fecha_hasta:
            query = query.filter(Esquela.fecha <= fecha_hasta)

        # Filtro por tipo
        if tipo:
            query = query.filter(CodigoEsquela.tipo == tipo)

        # Filtro por registrador (quien asignó la esquela)
        if id_registrador:
            query = query.filter(Esquela.id_registrador == id_registrador)

        query = query.group_by(
            Estudiante.id_estudiante,
            Estudiante.nombres,
            Estudiante.apellido_paterno,
            Estudiante.apellido_materno
        ).order_by(func.count(func.distinct(Esquela.id_esquela)).desc()).limit(limit)

        results = query.all()

        # Formatear resultados
        ranking = []
        for idx, (id_est, nombres, ap_pat, ap_mat, total, reconocimiento, orientacion) in enumerate(results, 1):
            apellidos = f"{ap_pat} {ap_mat or ''}".strip()
            nombre_completo = f"{nombres} {apellidos}"
            ranking.append({
                "id": id_est,
                "nombre": nombre_completo,
                "total": int(total or 0),
                "reconocimiento": int(reconocimiento or 0),
                "orientacion": int(orientacion or 0),
                "posicion": idx
            })

        return ranking

    @staticmethod
    def get_ranking_cursos(
        db: Session,
        tipo: Optional[str] = None,
        limit: int = 10,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None
    ):
        """
        Obtiene ranking de cursos por cantidad de esquelas
        NOTA: Join a través de estudiantes_cursos porque no hay id_curso en esquelas
        """
        query = db.query(
            Curso.id_curso,
            Curso.nombre_curso,
            func.count(func.distinct(Esquela.id_esquela)).label('total'),
            func.sum(
                case((CodigoEsquela.tipo == 'reconocimiento', 1), else_=0)
            ).label('reconocimiento'),
            func.sum(
                case((CodigoEsquela.tipo == 'orientacion', 1), else_=0)
            ).label('orientacion')
        ).select_from(Curso).join(
            estudiantes_cursos, Curso.id_curso == estudiantes_cursos.c.id_curso
        ).join(
            Estudiante, Estudiante.id_estudiante == estudiantes_cursos.c.id_estudiante
        ).join(
            Esquela, Esquela.id_estudiante == Estudiante.id_estudiante
        ).join(
            EsquelaCodigo, Esquela.id_esquela == EsquelaCodigo.id_esquela
        ).join(
            CodigoEsquela, EsquelaCodigo.id_codigo == CodigoEsquela.id_codigo
        )

        # Filtros de fecha
        if fecha_desde:
            query = query.filter(Esquela.fecha >= fecha_desde)
        if fecha_hasta:
            query = query.filter(Esquela.fecha <= fecha_hasta)

        # Filtro por tipo
        if tipo:
            query = query.filter(CodigoEsquela.tipo == tipo)

        query = query.group_by(
            Curso.id_curso,
            Curso.nombre_curso
        ).order_by(func.count(func.distinct(Esquela.id_esquela)).desc()).limit(limit)

        results = query.all()

        # Formatear resultados
        ranking = []
        for idx, (id_curso, nombre_curso, total, reconocimiento, orientacion) in enumerate(results, 1):
            ranking.append({
                "id": id_curso,
                "nombre": nombre_curso,
                "total": int(total or 0),
                "reconocimiento": int(reconocimiento or 0),
                "orientacion": int(orientacion or 0),
                "posicion": idx
            })

        return ranking

    # ================================
    # Métodos para Reportes de Estudiantes
    # ================================

    @staticmethod
    def get_estudiantes_por_filtros(
        db: Session,
        id_curso: Optional[int] = None,
        nivel: Optional[str] = None,
        gestion: Optional[str] = None
    ):
        """
        Obtiene listado de estudiantes filtrado por curso, nivel y/o gestión
        """
        query = db.query(Estudiante).join(
            estudiantes_cursos, Estudiante.id_estudiante == estudiantes_cursos.c.id_estudiante
        ).join(
            Curso, Curso.id_curso == estudiantes_cursos.c.id_curso
        )

        if id_curso:
            query = query.filter(Curso.id_curso == id_curso)
        if nivel:
            query = query.filter(Curso.nivel == nivel)
        if gestion:
            query = query.filter(Curso.gestion == gestion)

        # Obtener estudiantes únicos
        estudiantes = query.distinct().all()

        # Formatear resultados con sus cursos
        resultado = []
        for est in estudiantes:
            # Calcular edad si hay fecha de nacimiento
            edad = None
            if est.fecha_nacimiento:
                hoy = date.today()
                edad = hoy.year - est.fecha_nacimiento.year
                if hoy.month < est.fecha_nacimiento.month or (
                    hoy.month == est.fecha_nacimiento.month and hoy.day < est.fecha_nacimiento.day
                ):
                    edad -= 1

            # Obtener cursos del estudiante (filtrados si aplica)
            cursos_query = db.query(Curso).join(
                estudiantes_cursos, Curso.id_curso == estudiantes_cursos.c.id_curso
            ).filter(estudiantes_cursos.c.id_estudiante == est.id_estudiante)

            if nivel:
                cursos_query = cursos_query.filter(Curso.nivel == nivel)
            if gestion:
                cursos_query = cursos_query.filter(Curso.gestion == gestion)

            cursos = cursos_query.all()
            cursos_nombres = [
                f"{c.nombre_curso} ({c.gestion})" for c in cursos]

            resultado.append({
                "id_estudiante": est.id_estudiante,
                "ci": est.ci,
                "nombre_completo": est.nombre_completo,
                "fecha_nacimiento": est.fecha_nacimiento,
                "edad": edad,
                "cursos": cursos_nombres
            })

        return resultado

    @staticmethod
    def get_estudiantes_por_apoderados(
        db: Session,
        con_apoderados: Optional[bool] = None
    ):
        """
        Obtiene estudiantes con o sin apoderados registrados
        con_apoderados: True (con apoderados), False (sin apoderados), None (todos)
        """
        query = db.query(Estudiante)

        estudiantes = query.all()
        resultado = []

        for est in estudiantes:
            # Verificar si tiene apoderados
            tiene_padre = bool(est.nombre_padre and est.nombre_padre.strip())
            tiene_madre = bool(est.nombre_madre and est.nombre_madre.strip())
            tiene_apoderados = tiene_padre or tiene_madre

            # Aplicar filtro si se especificó
            if con_apoderados is not None and tiene_apoderados != con_apoderados:
                continue

            # Construir lista de apoderados
            apoderados = []

            if tiene_padre:
                nombre_padre = f"{est.nombre_padre or ''} {est.apellido_paterno_padre or ''} {
                    est.apellido_materno_padre or ''}".strip()
                apoderados.append({
                    "tipo": "padre",
                    "nombre_completo": nombre_padre if nombre_padre else None,
                    "telefono": est.telefono_padre
                })

            if tiene_madre:
                nombre_madre = f"{est.nombre_madre or ''} {est.apellido_paterno_madre or ''} {
                    est.apellido_materno_madre or ''}".strip()
                apoderados.append({
                    "tipo": "madre",
                    "nombre_completo": nombre_madre if nombre_madre else None,
                    "telefono": est.telefono_madre
                })

            resultado.append({
                "id_estudiante": est.id_estudiante,
                "ci": est.ci,
                "nombre_completo": est.nombre_completo,
                "apoderados": apoderados,
                "tiene_apoderados": tiene_apoderados
            })

        return resultado

    @staticmethod
    def get_contactos_apoderados(
        db: Session,
        id_curso: Optional[int] = None,
        nivel: Optional[str] = None,
        gestion: Optional[str] = None
    ):
        """
        Obtiene datos de contacto de apoderados con filtros opcionales
        """
        query = db.query(Estudiante)

        # Aplicar filtros si se especifican
        if id_curso or nivel or gestion:
            query = query.join(
                estudiantes_cursos, Estudiante.id_estudiante == estudiantes_cursos.c.id_estudiante
            ).join(
                Curso, Curso.id_curso == estudiantes_cursos.c.id_curso
            )

            if id_curso:
                query = query.filter(Curso.id_curso == id_curso)
            if nivel:
                query = query.filter(Curso.nivel == nivel)
            if gestion:
                query = query.filter(Curso.gestion == gestion)

            query = query.distinct()

        estudiantes = query.all()
        contactos = []

        for est in estudiantes:
            # Agregar contacto del padre si existe
            if est.nombre_padre and est.telefono_padre:
                nombre_padre = f"{est.nombre_padre or ''} {est.apellido_paterno_padre or ''} {
                    est.apellido_materno_padre or ''}".strip()
                contactos.append({
                    "id_estudiante": est.id_estudiante,
                    "estudiante_nombre": est.nombre_completo,
                    "estudiante_ci": est.ci,
                    "tipo_apoderado": "padre",
                    "apoderado_nombre": nombre_padre,
                    "telefono": est.telefono_padre
                })

            # Agregar contacto de la madre si existe
            if est.nombre_madre and est.telefono_madre:
                nombre_madre = f"{est.nombre_madre or ''} {est.apellido_paterno_madre or ''} {
                    est.apellido_materno_madre or ''}".strip()
                contactos.append({
                    "id_estudiante": est.id_estudiante,
                    "estudiante_nombre": est.nombre_completo,
                    "estudiante_ci": est.ci,
                    "tipo_apoderado": "madre",
                    "apoderado_nombre": nombre_madre,
                    "telefono": est.telefono_madre
                })

        return contactos

    @staticmethod
    def get_distribucion_por_edad(
        db: Session,
        id_curso: Optional[int] = None,
        nivel: Optional[str] = None,
        gestion: Optional[str] = None
    ):
        """
        Obtiene distribución de estudiantes por rangos de edad
        """
        query = db.query(Estudiante)

        # Aplicar filtros si se especifican
        if id_curso or nivel or gestion:
            query = query.join(
                estudiantes_cursos, Estudiante.id_estudiante == estudiantes_cursos.c.id_estudiante
            ).join(
                Curso, Curso.id_curso == estudiantes_cursos.c.id_curso
            )

            if id_curso:
                query = query.filter(Curso.id_curso == id_curso)
            if nivel:
                query = query.filter(Curso.nivel == nivel)
            if gestion:
                query = query.filter(Curso.gestion == gestion)

            query = query.distinct()

        estudiantes = query.all()

        # Calcular edades y agrupar por rangos
        rangos = {
            "0-4 años": 0,
            "5-7 años": 0,
            "8-10 años": 0,
            "11-13 años": 0,
            "14-16 años": 0,
            "17+ años": 0,
            "Sin fecha": 0
        }

        for est in estudiantes:
            if est.fecha_nacimiento:
                hoy = date.today()
                edad = hoy.year - est.fecha_nacimiento.year
                if hoy.month < est.fecha_nacimiento.month or (
                    hoy.month == est.fecha_nacimiento.month and hoy.day < est.fecha_nacimiento.day
                ):
                    edad -= 1

                if edad < 5:
                    rangos["0-4 años"] += 1
                elif edad <= 7:
                    rangos["5-7 años"] += 1
                elif edad <= 10:
                    rangos["8-10 años"] += 1
                elif edad <= 13:
                    rangos["11-13 años"] += 1
                elif edad <= 16:
                    rangos["14-16 años"] += 1
                else:
                    rangos["17+ años"] += 1
            else:
                rangos["Sin fecha"] += 1

        total = len(estudiantes)
        distribucion = []

        for rango, cantidad in rangos.items():
            if cantidad > 0:  # Solo incluir rangos con estudiantes
                porcentaje = (cantidad / total * 100) if total > 0 else 0
                distribucion.append({
                    "rango_edad": rango,
                    "cantidad": cantidad,
                    "porcentaje": round(porcentaje, 2)
                })

        return {
            "distribucion": distribucion,
            "total_estudiantes": total
        }

    @staticmethod
    def get_historial_cursos_estudiante(
        db: Session,
        id_estudiante: Optional[int] = None
    ):
        """
        Obtiene historial de cursos por estudiante
        Si no se especifica id_estudiante, retorna historial de todos
        """
        query = db.query(Estudiante)

        if id_estudiante:
            query = query.filter(Estudiante.id_estudiante == id_estudiante)

        estudiantes = query.all()
        historiales = []

        for est in estudiantes:
            # Obtener cursos del estudiante ordenados por gestión
            cursos = db.query(Curso).join(
                estudiantes_cursos, Curso.id_curso == estudiantes_cursos.c.id_curso
            ).filter(
                estudiantes_cursos.c.id_estudiante == est.id_estudiante
            ).order_by(Curso.gestion.desc(), Curso.nivel).all()

            cursos_lista = []
            for curso in cursos:
                cursos_lista.append({
                    "id_curso": curso.id_curso,
                    "nombre_curso": curso.nombre_curso,
                    "nivel": curso.nivel,
                    "gestion": curso.gestion
                })

            historiales.append({
                "id_estudiante": est.id_estudiante,
                "nombre_completo": est.nombre_completo,
                "ci": est.ci,
                "cursos": cursos_lista,
                "total_cursos": len(cursos_lista)
            })

        return historiales

    # ================================
    # Métodos para Reportes Académicos
    # ================================

    @staticmethod
    def get_profesores_asignados(
        db: Session,
        id_curso: Optional[int] = None,
        id_materia: Optional[int] = None,
        nivel: Optional[str] = None,
        gestion: Optional[str] = None
    ):
        """
        Obtiene profesores asignados por curso y materia
        """
        query = db.query(
            Persona.id_persona,
            Persona.ci,
            Persona.nombres,
            Persona.apellido_paterno,
            Persona.apellido_materno,
            Persona.telefono,
            Persona.correo,
            Curso.nombre_curso,
            Curso.gestion,
            Materia.nombre_materia
        ).select_from(Persona).join(
            ProfesorCursoMateria,
            Persona.id_persona == ProfesorCursoMateria.id_profesor
        ).join(
            Curso,
            Curso.id_curso == ProfesorCursoMateria.id_curso
        ).join(
            Materia,
            Materia.id_materia == ProfesorCursoMateria.id_materia
        ).filter(
            Persona.tipo_persona == 'profesor'
        )

        # Aplicar filtros
        if id_curso:
            query = query.filter(Curso.id_curso == id_curso)
        if id_materia:
            query = query.filter(Materia.id_materia == id_materia)
        if nivel:
            query = query.filter(Curso.nivel == nivel)
        if gestion:
            query = query.filter(Curso.gestion == gestion)

        resultados = query.all()

        profesores = []
        for id_p, ci, nombres, ap_pat, ap_mat, tel, correo, nom_curso, gest, nom_mat in resultados:
            nombre_completo = f"{nombres} {ap_pat} {ap_mat or ''}".strip()
            profesores.append({
                "id_profesor": id_p,
                "ci": ci,
                "nombre_completo": nombre_completo,
                "telefono": tel,
                "correo": correo,
                "curso": f"{nom_curso} ({gest})",
                "materia": nom_mat
            })

        return profesores

    @staticmethod
    def get_materias_por_nivel(
        db: Session,
        nivel: Optional[str] = None
    ):
        """
        Obtiene materias filtradas por nivel educativo
        """
        query = db.query(Materia)

        if nivel:
            query = query.filter(Materia.nivel == nivel)

        materias = query.order_by(Materia.nivel, Materia.nombre_materia).all()

        resultado = []
        for mat in materias:
            resultado.append({
                "id_materia": mat.id_materia,
                "nombre_materia": mat.nombre_materia,
                "nivel": mat.nivel
            })

        return resultado

    @staticmethod
    def get_carga_academica_profesores(
        db: Session,
        id_profesor: Optional[int] = None,
        gestion: Optional[str] = None
    ):
        """
        Obtiene carga académica de profesores
        """
        query = db.query(Persona).filter(Persona.tipo_persona == 'profesor')

        if id_profesor:
            query = query.filter(Persona.id_persona == id_profesor)

        profesores = query.all()
        resultado = []

        for prof in profesores:
            from app.modules.profesores.models.profesor_models import Profesor
            profesor_row = db.query(Profesor).filter(
                Profesor.id_persona == prof.id_persona).first()
            if not profesor_row:
                continue

            # Obtener asignaciones del profesor
            asig_query = db.query(
                Curso.nombre_curso,
                Curso.nivel,
                Curso.gestion,
                Materia.nombre_materia
            ).join(
                profesores_cursos_materias,
                Curso.id_curso == profesores_cursos_materias.c.id_curso
            ).join(
                Materia,
                Materia.id_materia == profesores_cursos_materias.c.id_materia
            ).filter(
                profesores_cursos_materias.c.id_profesor == profesor_row.id_profesor
            )

            if gestion:
                asig_query = asig_query.filter(Curso.gestion == gestion)

            asignaciones = asig_query.all()

            asignaciones_lista = []
            cursos_set = set()
            materias_set = set()

            for nom_curso, nivel, gest, nom_mat in asignaciones:
                asignaciones_lista.append({
                    "curso": nom_curso,
                    "nivel": nivel,
                    "gestion": gest,
                    "materia": nom_mat
                })
                cursos_set.add(f"{nom_curso}-{gest}")
                materias_set.add(nom_mat)

            nombre_completo = f"{prof.nombres} {prof.apellido_paterno} {
                prof.apellido_materno or ''}".strip()

            resultado.append({
                "id_profesor": profesor_row.id_profesor,
                "ci": prof.ci,
                "nombre_completo": nombre_completo,
                "telefono": prof.telefono,
                "correo": prof.correo,
                "asignaciones": asignaciones_lista,
                "total_asignaciones": len(asignaciones_lista),
                "cursos_distintos": len(cursos_set),
                "materias_distintas": len(materias_set)
            })

        return resultado

    @staticmethod
    def get_cursos_por_gestion(
        db: Session,
        gestion: Optional[str] = None,
        nivel: Optional[str] = None
    ):
        """
        Obtiene cursos por gestión con conteo de estudiantes
        """
        query = db.query(
            Curso.id_curso,
            Curso.nombre_curso,
            Curso.nivel,
            Curso.gestion,
            func.count(estudiantes_cursos.c.id_estudiante).label(
                'total_estudiantes')
        ).outerjoin(
            estudiantes_cursos,
            Curso.id_curso == estudiantes_cursos.c.id_curso
        )

        if gestion:
            query = query.filter(Curso.gestion == gestion)
        if nivel:
            query = query.filter(Curso.nivel == nivel)

        query = query.group_by(
            Curso.id_curso,
            Curso.nombre_curso,
            Curso.nivel,
            Curso.gestion
        ).order_by(Curso.gestion.desc(), Curso.nivel, Curso.nombre_curso)

        resultados = query.all()

        cursos = []
        for id_c, nom_c, niv, gest, total_est in resultados:
            cursos.append({
                "id_curso": id_c,
                "nombre_curso": nom_c,
                "nivel": niv,
                "gestion": gest,
                "total_estudiantes": int(total_est or 0)
            })

        return cursos

    # ================================
    # Métodos para Reportes de Esquelas
    # ================================

    @staticmethod
    def get_esquelas_por_profesor(
        db: Session,
        # en realidad es por emisor, falta refactorizar los nombres
        id_profesor: Optional[int] = None,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None
    ):
        """
        Obtiene esquelas agrupadas por profesor emisor
        """
        query = db.query(Persona).filter((Persona.tipo_persona == 'profesor') | (
            Persona.tipo_persona == 'regente') | (Persona.tipo_persona == 'administrativo'))

        if id_profesor:
            query = query.filter(Persona.ci == id_profesor)

        profesores = query.all()
        resultado = []

        for prof in profesores:
            # Obtener esquelas del profesor
            esq_query = db.query(Esquela).filter(
                Esquela.id_profesor == prof.id_persona
            )

            if fecha_desde:
                esq_query = esq_query.filter(Esquela.fecha >= fecha_desde)
            if fecha_hasta:
                esq_query = esq_query.filter(Esquela.fecha <= fecha_hasta)

            esquelas = esq_query.all()

            if not esquelas:  # Solo incluir profesores con esquelas
                continue

            esquelas_lista = []
            reconocimientos = 0
            orientaciones = 0

            for esq in esquelas:
                # Obtener estudiante
                estudiante = esq.estudiante
                est_nombre = f"{estudiante.nombres} {estudiante.apellido_paterno} {
                    estudiante.apellido_materno or ''}".strip()

                # Obtener registrador
                # Obtener registrador desde Persona
                registrador = db.query(Persona).filter(
                    Persona.id_persona == esq.id_registrador).first()
                if registrador:
                    reg_nombre = f"{registrador.nombres} {registrador.apellido_paterno} {
                        registrador.apellido_materno or ''}".strip()
                else:
                    reg_nombre = "Sin registrador"               # Obtener códigos

                codigos_query = db.query(CodigoEsquela).join(
                    EsquelaCodigo,
                    CodigoEsquela.id_codigo == EsquelaCodigo.id_codigo
                ).filter(EsquelaCodigo.id_esquela == esq.id_esquela)

                codigos_objs = codigos_query.all()
                codigos = []

                for cod in codigos_objs:
                    codigos.append(f"{cod.codigo} - {cod.descripcion}")
                    if cod.tipo == 'reconocimiento':
                        reconocimientos += 1
                    else:
                        orientaciones += 1

                esquelas_lista.append({
                    "id_esquela": esq.id_esquela,
                    "fecha": esq.fecha,
                    "estudiante_nombre": est_nombre,
                    "estudiante_ci": estudiante.ci,
                    "profesor_nombre": f"{prof.nombres} {prof.apellido_paterno} {prof.apellido_materno or ''}".strip(),
                    "registrador_nombre": reg_nombre,
                    "codigos": codigos,
                    "observaciones": esq.observaciones
                })

            prof_nombre = f"{prof.nombres} {prof.apellido_paterno} {
                prof.apellido_materno or ''}".strip()

            resultado.append({
                "id_profesor": prof.id_persona,
                "profesor_nombre": prof_nombre,
                "profesor_ci": prof.ci,
                "total_esquelas": len(esquelas_lista),
                "reconocimientos": reconocimientos,
                "orientaciones": orientaciones,
                "esquelas": esquelas_lista
            })

        return resultado

    @staticmethod
    def get_esquelas_por_fecha(
        db: Session,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        tipo: Optional[str] = None
    ):
        """
        Obtiene esquelas por rango de fechas
        """
        query = db.query(Esquela)

        if fecha_desde:
            query = query.filter(Esquela.fecha >= fecha_desde)
        if fecha_hasta:
            query = query.filter(Esquela.fecha <= fecha_hasta)

        esquelas = query.order_by(Esquela.fecha.desc()).all()

        resultado = []
        reconocimientos = 0
        orientaciones = 0

        for esq in esquelas:
            # Obtener estudiante
            estudiante = esq.estudiante
            est_nombre = f"{estudiante.nombres} {estudiante.apellido_paterno} {
                estudiante.apellido_materno or ''}".strip()

            # Obtener profesor
            # Obtener profesor
            profesor = db.query(Persona).filter(
                Persona.id_persona == esq.id_profesor).first()
            if profesor:
                prof_nombre = f"{profesor.nombres} {profesor.apellido_paterno} {
                    profesor.apellido_materno or ''}".strip()
            else:
                prof_nombre = "Sin profesor"            # Obtener registrador
            # Obtener registrador
            registrador = db.query(Persona).filter(
                Persona.id_persona == esq.id_registrador).first()
            if registrador:
                reg_nombre = f"{registrador.nombres} {registrador.apellido_paterno} {
                    registrador.apellido_materno or ''}".strip()
            else:
                reg_nombre = "Sin registrador"
            # Obtener códigos
            codigos_query = db.query(CodigoEsquela).join(
                EsquelaCodigo,
                CodigoEsquela.id_codigo == EsquelaCodigo.id_codigo
            ).filter(EsquelaCodigo.id_esquela == esq.id_esquela)

            # Filtrar por tipo si se especifica
            if tipo:
                codigos_query = codigos_query.filter(
                    CodigoEsquela.tipo == tipo)

            codigos_objs = codigos_query.all()

            # Si se filtró por tipo y no hay códigos de ese tipo, saltar esta esquela
            if tipo and not codigos_objs:
                continue

            codigos = []
            tiene_reconocimiento = False
            tiene_orientacion = False

            for cod in codigos_objs:
                codigos.append(f"{cod.codigo} - {cod.descripcion}")
                if cod.tipo == 'reconocimiento':
                    tiene_reconocimiento = True
                else:
                    tiene_orientacion = True

            if tiene_reconocimiento:
                reconocimientos += 1
            if tiene_orientacion:
                orientaciones += 1

            resultado.append({
                "id_esquela": esq.id_esquela,
                "fecha": esq.fecha,
                "estudiante_nombre": est_nombre,
                "estudiante_ci": estudiante.ci,
                "profesor_nombre": prof_nombre,
                "registrador_nombre": reg_nombre,
                "codigos": codigos,
                "observaciones": esq.observaciones
            })

        return {
            "esquelas": resultado,
            "total": len(resultado),
            "reconocimientos": reconocimientos,
            "orientaciones": orientaciones
        }

    @staticmethod
    def get_codigos_frecuentes(
        db: Session,
        tipo: Optional[str] = None,
        limit: int = 10,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None
    ):
        """
        Obtiene los códigos más frecuentemente aplicados
        """
        query = db.query(
            CodigoEsquela.id_codigo,
            CodigoEsquela.codigo,
            CodigoEsquela.descripcion,
            CodigoEsquela.tipo,
            func.count(EsquelaCodigo.id_esquela).label('total_aplicaciones')
        ).join(
            EsquelaCodigo,
            CodigoEsquela.id_codigo == EsquelaCodigo.id_codigo
        )

        # Aplicar filtros de fecha si se especifican
        if fecha_desde or fecha_hasta:
            query = query.join(
                Esquela,
                Esquela.id_esquela == EsquelaCodigo.id_esquela
            )
            if fecha_desde:
                query = query.filter(Esquela.fecha >= fecha_desde)
            if fecha_hasta:
                query = query.filter(Esquela.fecha <= fecha_hasta)

        # Filtrar por tipo si se especifica
        if tipo:
            query = query.filter(CodigoEsquela.tipo == tipo)

        query = query.group_by(
            CodigoEsquela.id_codigo,
            CodigoEsquela.codigo,
            CodigoEsquela.descripcion,
            CodigoEsquela.tipo
        ).order_by(func.count(EsquelaCodigo.id_esquela).desc()).limit(limit)

        resultados = query.all()

        # Calcular total de aplicaciones para porcentajes
        total_aplicaciones = sum(r[4] for r in resultados)

        codigos = []
        for id_cod, cod, desc, tip, total in resultados:
            porcentaje = (total / total_aplicaciones *
                          100) if total_aplicaciones > 0 else 0
            codigos.append({
                "id_codigo": id_cod,
                "codigo": cod,
                "descripcion": desc,
                "tipo": tip,
                "total_aplicaciones": int(total),
                "porcentaje": round(porcentaje, 2)
            })

        return {
            "codigos": codigos,
            "total_aplicaciones": total_aplicaciones
        }

"""
DTOs base compartidos por todos los módulos
"""
from marshmallow import Schema, fields, validate, post_load
from datetime import datetime

class BaseSchema(Schema):
    """Schema base con campos comunes"""
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_active = fields.Boolean(dump_only=True)

class PersonaBaseSchema(BaseSchema):
    """Schema base para personas"""
    nombres = fields.String(required=True, validate=validate.Length(min=2, max=100))
    apellidos = fields.String(required=True, validate=validate.Length(min=2, max=100))
    cedula = fields.String(required=True, validate=validate.Length(min=7, max=20))
    email = fields.Email(allow_none=True)
    telefono = fields.String(allow_none=True, validate=validate.Length(max=15))
    fecha_nacimiento = fields.Date(allow_none=True)
    direccion = fields.String(allow_none=True)
    
    nombre_completo = fields.String(dump_only=True)

class PaginationSchema(Schema):
    """Schema para paginación"""
    page = fields.Integer(missing=1, validate=validate.Range(min=1))
    per_page = fields.Integer(missing=10, validate=validate.Range(min=1, max=100))
    sort_by = fields.String(missing='id')
    sort_order = fields.String(missing='asc', validate=validate.OneOf(['asc', 'desc']))

class ResponseSchema(Schema):
    """Schema para respuestas estandarizadas"""
    success = fields.Boolean(required=True)
    message = fields.String(required=True)
    data = fields.Raw(allow_none=True)
    errors = fields.List(fields.String(), allow_none=True)
    timestamp = fields.DateTime(required=True)

class PaginatedResponseSchema(ResponseSchema):
    """Schema para respuestas paginadas"""
    pagination = fields.Dict(keys=fields.String(), values=fields.Raw())

class ErrorResponseSchema(Schema):
    """Schema para respuestas de error"""
    success = fields.Boolean(required=True, default=False)
    message = fields.String(required=True)
    errors = fields.List(fields.String())
    error_code = fields.String(allow_none=True)
    timestamp = fields.DateTime(required=True)
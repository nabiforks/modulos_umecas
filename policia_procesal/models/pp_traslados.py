# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Traslados(models.Model):
    _name = 'pp.traslado'

    name = fields.Char(
        string="Número de oficio"
    )
    procedencia_imputado = fields.Char(
        string="Procedencia del imputado"
    )
    descripcion_imputado = fields.Text(
        string="Estado físico y vestimenta del imputado"
    )
    fecha_traslado	 = fields.Date(
        string="Fecha de traslado",
        default=fields.Datetime.now
    )
    hora_arribo = fields.Datetime(
        string="Hora de arribo",
        default=fields.Datetime.now
    )
    hora_ingreso = fields.Datetime(
        string="Hora de ingreso",
        default=fields.Datetime.now
    )
    hora_regreso = fields.Datetime(
        string="Hora al regresar la custodia del imputado",
        default=fields.Datetime.now
    )
    dictamen_medico = fields.Boolean(
        string='¿Cuenta con dictamen médico?'
    )
    autoridad_que_ordena_id = fields.Char(
        string='Autoridad que ordena el traslado',
    )
    autoridad_que_realiza_id = fields.Char(
        string='Autoridad que realiza el traslado',
    )
    cargo_autoridad_ordena =  fields.Char(
        string="Cargo",
    )
    cargo_autoridad_realiza =  fields.Char(
        string="Cargo",
    )
    dependencia = fields.Char(
        string="Dependencia a la que pertenece"
    )
    

    #==========Relationship fields==========
    
    employee_ids = fields.Many2many(
        'hr.employee',
        string='Elementos de apoyo',
    )
    medico_id = fields.Many2one(
        'pp.medico',
        string='Nombre',
    )
    vehiculo_id = fields.Many2one(
        'pp.vehiculos',
        string='Vehículo Oficial',
    )

    #==========RELATED==========
    no_cedula =  fields.Char(
        related='medico_id.cedula', 
        string="Número de cedula",
        readonly=True
    )
    placas = fields.Char(
        related='vehiculo_id.placas',
        string='Placas',
        readonly=True
    )
    no_economico = fields.Char(
        related='vehiculo_id.no_economico',
        string='Número económico',
        readonly=True
    )
    """nombre_completo = fields.Char(
        related='imputado_id.display_name',
        string='Nombre del imputado',
    )"""


class RetiroTraslado(models.Model):
    _name = 'pp.retiro_traslado'

    name = fields.Char(
        string='Número de oficio',
    )
    fecha_traslado = fields.Char(
        string='Fecha de traslado',
    )
    observaciones = fields.Text(
        string='Observaciones',
    )
    dependencia = fields.Char(
        string="Dependencia a la que pertenece"
    )
    procedencia_imputado = fields.Char(
        string="Procedencia del imputado"
    )

    #==========Relationship fields==========
    imputado_id = fields.Char(
        #'res.partner',
        string='Imputado',
    )
    employee_ids = fields.Many2many(
        'hr.employee',
        string='Elementos de apoyo',
    )
    autoridad_que_ordena_id = fields.Many2one(
        'pp.autoridad',
        string='Autoridad que ordena el traslado'
    )
    autoridad_que_realiza_id = fields.Many2one(
        'pp.autoridad',
        string='Autoridad que realiza el traslado'
    )
    vehiculo_id = fields.Many2one(
        'pp.vehiculos',
        string='Vehículo Oficial',
    )

    #==========RELATED==========
    cargo_autoridad_realiza =  fields.Char(
        related='autoridad_que_realiza_id.cargo', 
        string="Cargo",readonly=True
    )
    cargo_autoridad_ordena =  fields.Char(
        related='autoridad_que_ordena_id.cargo', 
        string="Cargo",readonly=True
    )
    placas = fields.Char(
        related='vehiculo_id.placas',
        string='Placas',
        readonly=True
    )
    no_economico = fields.Char(
        related='vehiculo_id.no_economico',
        string='Número económico',
        readonly=True
    )
    """nombre_completo = fields.Char(
        related='imputado_id.display_name',
        string='Nombre del imputado',
    )"""
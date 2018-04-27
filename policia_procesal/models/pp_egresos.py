# -*- coding: utf-8 -*-

from odoo import fields, models

class Egreso(models.Model):
    _name = 'pp.egreso'

    name = fields.Char(
        string='No. Oficio de traslado',
        required=True,
    )
    fecha_hora = fields.Datetime(
        string='Fecha y hora de recepción',
    )
    nic_cdi_nuc = fields.Char(
        string='NIC/CDI/NUC',
    )
    autoridad_que_solicita_id = fields.Char(
        string='Autoridad que solicita/ordena el traslado',
    )
    autoridad_que_realiza_id = fields.Char(
        string='Autoridad que realiza el traslado',
    )
    cargo_autoridad_solicita =  fields.Char(
        string="Cargo",
    )
    cargo_autoridad_realiza =  fields.Char(
        string="Cargo",
    )
    numero_elementos = fields.Integer(
        string='Número de elementos',
    )
    dependencia = fields.Many2one(
        'pp.dependencias',
        string='Dependencia a la que pertenecen',
    )
    tipo_audiencia = fields.Char(
        string='Tipo de audiencia',
    )
    fecha_inicio_audiencia = fields.Date(
        string='Fecha',
    )
    hora_inicio_audiencia = fields.Float(
        string='Hora',
    )
    hora_termino_audiencia = fields.Float(
        string="Hora de termino de Audiencia",
    )
    fecha_hora_entrega_responsable = fields.Datetime(
        string='Fecha y hora de entrega al responsable del traslado',
    )
    observaciones = fields.Text(
        string='Observaciones',
    )
    observaciones_traslado = fields.Text(
        string='Observaciones',
    )
    
    #==========RELATIONSHIP==========
    partner_ids = fields.Many2many(
        'res.partner',
        string='Detenido y/o imputado(s)',
        required=True,
    )
    delito_ids = fields.Many2many(
        'umc_delitos',
        string='Delito(s)',
    )
    vehiculo_ids = fields.Many2many(
        'pp.vehiculos',
        string='Vehículo Oficial',
    )
    lugar_id = fields.Many2one(
        'umc_lugares',
        string='Procedencia',
    )
    
    #==========RELATED==========
    
    placas = fields.Char(
        #related='vehiculo_id.placas',
        string='Placas',
        readonly=True
    )
    no_economico = fields.Char(
        #related='vehiculo_id.no_economico',
        string='Número económico',
        readonly=True
    )
    #==========Datos para reporte==========
    responsable = fields.Char(
        string='Nombre del responsable que recibe la custodia',
    )
    seccion = fields.Char(
        string='Sección',
        default='11S',
    )
    serie = fields.Char(
        string='Serie',
        default='11S.3',
    )
    sub_serie = fields.Char(
        string='Subserie',
    )
# -*- coding: utf-8 -*-

from odoo import fields, models

class Audiencias(models.Model):
    _name = 'pp.audiencia'

    name = fields.Char(
        string='Folio',
    )
    lugar = fields.Char(
        string='Lugar programado para la audiencia',
    )
    tipo_audiencia = fields.Char(
        string='Tipo de audiencia',
    )
    causa_penal = fields.Char(
        string='Causa penal',
    )
    no_sala = fields.Integer(
        string='Número de sala',
    )
    fecha_hora = fields.Datetime(
        string='Fecha y hora',
    )
    hora_inicio = fields.Float(
        string='Hora de inico',
    )
    hora_termino = fields.Float(
        string='Hora de termino',
    )
    juez_nombre = fields.Char(
        string='Juez',
    )
    juez_cargo = fields.Char(
        string='Cargo',
    )
    juez_region = fields.Char(
        string='Región',
    )
    resolucion = fields.Text(
        string='Resolución',
    )
    observaciones = fields.Text(
        string='Observaciones',
    )
    pp_cargo = fields.Char(
        string='Cargo',
    )
    datos_audiencia = fields.Text(
        string='Datos de la audiencia',
    )

    #==========RELATIONSHIP FIELDS==========
    imputado_ids = fields.Many2many(
        'res.partner',
        string='',
    )
    expediente_ids = fields.Many2many(
        'umc_expedientes',
        string='Nombre(s) del (los) imputado(s) ',
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Nombre',
    )
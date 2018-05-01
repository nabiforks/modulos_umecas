# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ControlAudiencia(models.Model):
    _name = 'pp.control_audiencia'

    name = fields.Char(
        string='Folio',
        required=True,
    )
    causa_penal = fields.Char(
        string='Causa penal',
    )
    numero_sala = fields.Integer(
        string='Número de sala',
    )
    tipo_audiencia = fields.Char(
        string='Tipo de audiencia',
    )
    tipo_ingreso = fields.Selection([
        ('traslado', 'En traslado'),
        ('voluntaria', 'Presentación voluntaria')],
        string='Tipo de ingreso del imputado'
    )
    fecha_hora = fields.Datetime(
        string='Fecha y hora',
    )
    hora_inicio = fields.Float(
        string='Hora de inico',
    )
    hora_termino = fields.Float(
        string='Hora de término',
    )
    resolucion = fields.Text(
        string='Resolución de la audiencia',
    )
    observaciones = fields.Text(
        string='Observaciones',
    )
    tipo_egreso = fields.Selection([
        ('libertad', 'Libertad'),
        ('traslado', 'En traslado')],
        string='Tipo de egreso'
    )
    recibe = fields.Char(
        string='Recibe',
    )
    hora_recibe = fields.Float(
        string='Hora',
    )
    juez_concat = fields.Char(#Este campo se concatena por los datos correspondientes a Juez_id
        string='Juez',
        compute='concat_name_juez'
    )

    #==========RELATIONSHIPS=========
    partner_ids = fields.Many2many(
        'res.partner',
        string='Imputado(s)',
        required=True,
        default=lambda self: self.env.context.get('partner_ids'),
        ondelete='set null',
    )
    audiencia_id = fields.Many2one(
        'pp.audiencia',
        string='Audiencia',
        ondelete='set null',
    )
    juez_ids = fields.Many2many(
        'pp.jueces',
        string='Recide Juez(es) (Cargo y región)',
    )
    delito_ids = fields.Many2many(
        'umc_delitos',
        string='Delito(s)',
    )
    lugar = fields.Many2one(
        'umc_lugares',
        string='Lugar programado para la audiencia',
    )
    nombre_jefe_grupo_pp = fields.Many2one(
        'pp.jefe_pp',
        string='Nombre',
    )

    #==========RELATED=========
    edad = fields.Integer(
       # related="partner_id.edad",
        string='Edad',
    )
    pp_cargo = fields.Char(
        related='nombre_jefe_grupo_pp.cargo',
        string='Cargo',
        readonly=True, 
    )
    pp_grupo = fields.Char(
        related='nombre_jefe_grupo_pp.grupo',
        string='Grupo',
        readonly=True, 
    )
    #==========Datos para reporte==========
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

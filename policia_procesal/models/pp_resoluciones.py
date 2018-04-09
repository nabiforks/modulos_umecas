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
        string='Hora de termino',
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
    partner_id = fields.Many2one(
        'res.partner',
        string='Imputado',
        required=True,
        default=lambda self: self.env.context.get('partner_id'),
        ondelete='set null',
    )
    juez_id = fields.Many2one(
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
        related="partner_id.edad",
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
    juez_nombre = fields.Char(
        related='juez_id.name',
        string='Nombre',
    )
    juez_titulo = fields.Char(
        related='juez_id.titulo',
        string='Título',
    )
    juez_cargo = fields.Char(
        related='juez_id.cargo',
        string='Cargo',
    )

    #==========METHODS=========
    @api.multi
    @api.depends('juez_nombre','juez_titulo')
    def concat_name_juez(self):
        for record in self:
            record.juez_concat = record.juez_titulo +', '+record.juez_nombre
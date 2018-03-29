# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class CustodiaProvicional(models.Model):
    _name = 'pp.custodia'

    name = fields.Char(
        'Custodia provicional',
        required=True,
        readonly=True,
        default=lambda self: 'Nuevo'
    )
    fecha_recepcion = fields.Date(
        string='Fecha de recepción'
    )
    fecha_hora_entrega = fields.Datetime(
        string='Fecha y hora de entrega',
    )
    pertenencias = fields.Integer(
        string='Pertenencias',
        compute='compute_pertenencias_count'
    )
    alimentos = fields.Integer(
        string='Alimentos',
        compute='compute_suministro_count',
    )
    no_registrado = fields.Boolean(
        string='No esta registrado'
    )
    temp_imputados = fields.Text(
        string='Imputado(s)',
    )
    temp_delitos = fields.Text(
        string='Delito(s)',
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('terminado', 'Terminado'),
        ], default='borrador', string='Estatus', readonly=True
    )
    desc_reg_imputados = fields.Char(
        string='Nota',
        compute='compute_note',
    )
    observaciones = fields.Text(
        string='Observaciones',
    )
    #==========Relationship fields==========
    expediente_ids = fields.Many2many(
        'umc_expedientes',
        string='Imputado(s)',
    )
    """name = fields.Many2one(
        'res.partner',
        string='Nombre del imputado',
    )"""
    traslado_id = fields.Many2one(
        'pp.traslado',
        string='No. Oficio de traslado',
    )

    #==========RELATED==========
    nombre_imp = fields.Char(
        string='Valor', related='expediente_ids.x_imputado_name', readonly=True,
    )
    
    procedencia = fields.Char(
        related='traslado_id.procedencia_imputado', 
        string='Procedencia',
        readonly=True, 
    )
    autoridad_que_solicita_id = fields.Char(
        related='traslado_id.autoridad_que_ordena_id',
        string='Autoridad que solicita el traslado',
        readonly=True, 
    )
    autoridad_que_realiza_id = fields.Char(
        related='traslado_id.autoridad_que_realiza_id',
        string='Autoridad que realiza el traslado',
        readonly=True, 
    )
    vehiculo = fields.Char(
        related='traslado_id.vehiculo_id.name',
        string='Vehículo',
        readonly=True, 
    )
    no_economico = fields.Char(
        related='traslado_id.vehiculo_id.no_economico',
        string='No. Económico',
        readonly=True, 
    )
    placas = fields.Char(
        related='traslado_id.vehiculo_id.placas',
        string='Placas',
        readonly=True, 
    )
    """nombre_completo = fields.Char(
        related='traslado_id.expediente_ids.x_imputado_name',
        string='Nombre del imputado',
    )"""

    #==========METHODS==========
    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'pp.custodia') or 'Nuevo'
        result = super(CustodiaProvicional, self).create(vals)
        return result

    @api.multi
    def reg_custodia_realizado(self):
        self.state = 'terminado'

    @api.multi
    @api.depends('no_registrado')
    def compute_note(self):
        for record in self:
            if record.no_registrado==True:
                record.desc_reg_imputados="No se encontraron expedientes"
            else:
                record.desc_reg_imputados="Expedientes encontrados"

    #///Botones 
    @api.multi
    def compute_pertenencias_count(self):
        for partner in self:
            partner.pertenencias = self.env['pp.pertenencias'].search_count(
                [('partner_id', '=', partner.name.id)])
    
    @api.multi
    def compute_suministro_count(self):
        for partner in self:
            partner.alimentos = self.env['pp.suministro'].search_count(
                [('partner_id', '=', partner.name.id)])


#======================================================New Class
class TrasladoImputado(models.Model):
    _name = 'pp.traslado_custodia'

    traslado_id = fields.Many2one(
        'pp.traslado',
         string='Traslado'
    )
    expediente_ids = fields.Many2one(
        'umc_expedientes', 
        string='Expedientes'
    )
    imputado = fields.Char(
        related='expediente_ids.x_imputado_name',
        readonly=True,
        string='Imputado'
    )

    custodia_id = fields.Many2one(
        string=u'Custodia',
        comodel_name='pp.custodia',
        ondelete='cascade',
    )
# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class CustodiaProvicional(models.Model):
    _name = 'pp.custodia'

    name = fields.Char(
        'Custodia',
        required=True,
        readonly=True,
        default=lambda self: 'Nuevo'
    )
    partner_id = fields.Many2one(
        'res.partner',
        required=True,
        #default=lambda self: self.env.context.get('partner_id'),
        ondelete='set null',
        string='Nombre del imputado',
    )
    causa_penal = fields.Char(
        string='Causa penal',
    )
    fecha_hora_registro = fields.Datetime(
        string='Fecha y hora de registro',
        default=lambda self: fields.datetime.now()
    )
    conducta = fields.Text(
        string='Conducta del imputado',
    )
    fecha_hora_egreso = fields.Datetime(
        string='Egreso del centro de justicia',
    )
    nombre_completo = fields.Char(
        related='partner_id.display_name',
        string='Nombre del imputado/detenido',
    )
    audiencias = fields.Integer(
        string='Pertenencias',
        compute='compute_audiencia_count'
    )
    delito_ids = fields.Many2many(
        'umc_delitos',
        string='Delito(s)',
        readonly=True, 
    )

    #==========Pertenencias y suministro de alimentos==========
    fecha_hora_devolucion = fields.Datetime(
        string='Fecha y hora de devolución',
    )
    recepcion_id = fields.Many2one(
        'pp.recepcion',
        #default=lambda self: self.env.context.get('active_id'),
        string='Recepción',
    )
    pertenencias_list_ids = fields.One2many(
        'pp.pertenencia_list',
        'custodia_id',
        string='Lista de pertenencias',
    )
    alimentos_list = fields.One2many(
        'pp.suministro_list',
        'custodia_id',
        string='Lista',
    )

    #==========Actuacion de PP con el imputado==========
    city = fields.Char(
        string='Ciudad, Municipio, Delegación',
    )
    numero_estancia = fields.Integer(
        string='Número de estancia',
    )
    sabe_leer_escribir = fields.Selection(
        [('si', 'Si'),('no', 'No')],
        string='Sabe leer y escribir'
    )
    entidad_id = fields.Many2one(
        'res.country.state',
        string='Entidad federativa',
    )
    nacionalidad_id = fields.Many2one(
        'umc_nacionalidad',
        string='Nacionalidad',
    )
    idioma_id = fields.Many2one(
        'umc_lengua',
        string='Idioma o lengua',
    )
    hora_actuacion = fields.Float(
        string='Hora',
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
    #==========METHODS==========
    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'pp.custodia') or 'Nuevo'
        result = super(CustodiaProvicional, self).create(vals)
        return result

    @api.multi
    def compute_audiencia_count(self):
        for partner in self:
            partner.audiencias = self.env['pp.audiencia'].search_count(
                [('custodia_id', '=', partner.id)])
        """

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
"""

#===============MODELO PARA LA LISTA DE PERTENENCIAS===============
class PertenenciasLista(models.Model):
    _name = 'pp.pertenencia_list'
    
    pertenencia = fields.Char(
        string='Pertenencia',
        required=True,
    )
    detalle = fields.Char(
        string='Detalles',
    )
    custodia_id = fields.Many2one(
        'pp.custodia',
        string='Resguardo de pertenencias',
        readonly=True, 
    )

#===============MODELO PARA LA LISTA DE SUMINISTRO DE ALIMENTO===============
class AlimentosList(models.Model):
    _name = 'pp.suministro_list'

    fecha = fields.Date(
        string='Fecha',
        required=True,
    )
    tercio = fields.Selection(
        [('primero', '1er. TERCIO'),
        ('segundo', '2do. TERCIO'),
        ('tercero','3er. TERCIO'),
        ('adicional','ADICIONAL')],
        required=True,
    )
    descripcion = fields.Text(
        string='Descripción',
    )
    custodia_id = fields.Many2one(
        'pp.custodia',
        string='Alimentos',
        readonly=True, 
    )
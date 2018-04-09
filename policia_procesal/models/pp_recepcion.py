# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Recepcion(models.Model):
    _name = 'pp.recepcion'

    consecutivo = fields.Char(
        'Recepción',
        required=True,
        readonly=True,
        default=lambda self: 'Nuevo'
    )
    numero_oficio = fields.Char(
        string='No. de Oficio de traslado',
        required=True,
    )
    fecha_hora = fields.Datetime(
        string='Fecha y hora de recepción',
        default=fields.Datetime.now
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
    custodias = fields.Integer(
        string='Pertenencias',
        compute='compute_custodia_count'
    )

    #==========RELATIONSHIP==========
    partner_id = fields.Many2one(
        'res.partner',
        string='Imputado/detenido',
        required=True,
    )
    delito_ids = fields.Many2many(
        'umc_delitos',
        string='Delito(s)',
    )
    vehiculo_id = fields.Many2one(
        'pp.vehiculos',
        string='Vehículo',
    )
    lugar_id = fields.Many2one(
        'umc_lugares',
        string='Procedencia',
    )
    dependencia = fields.Many2one(
        'pp.dependencias',
        string='Dependencia a la que pertenecen',
    )
    
    #==========RELATED==========
    name = fields.Char(
    	related='partner_id.display_name',
        string='Nombre del imputado/detenido',
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


    #==========Traslado de ingreso ==========
    #==========Traslado de ingreso ==========
    elementos_apoyo = fields.Integer(
        string='Elementos de apoyo',
    )
    vehiculos_apoyo = fields.Integer(
        string='Vehículos de apoyo',
    )
    descripcion_imputado = fields.Text(
        string="Estado físico y vestimenta del imputado"
    )
    fecha_traslado	 = fields.Date(
        string="Fecha de traslado",
    )
    hora_arribo = fields.Float(
        string="Hora de arribo",
    )
    hora_ingreso = fields.Float(
        string="Hora de ingreso",
    )
    hora_regreso = fields.Float(
        string="Hora al regresar la custodia a la coorporación",
    )
    no_cedula =  fields.Char(
        related='medico_id.cedula', 
        string="Número de cedula",
        readonly=True
    )

    #==========RELATIONSHIP==========
    medico_id = fields.Many2one(
        'pp.medico',
        string='Nombre',
    )

    #==========METHODS==========
    @api.model
    def create(self, vals):
        if vals.get('consecutivo', 'Nuevo') == 'Nuevo':
            vals['consecutivo'] = self.env['ir.sequence'].next_by_code(
                'pp.recepcion') or 'Nuevo'
        result = super(Recepcion, self).create(vals)
        return result

    @api.multi
    def compute_custodia_count(self):
        for partner in self:
            partner.custodias = self.env['pp.custodia'].search_count(
                [('partner_id', '=', partner.partner_id.id)])
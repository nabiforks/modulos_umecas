# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Recepcion(models.Model):
    _name = 'pp.recepcion'

    name = fields.Char(
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
    audiencias = fields.Integer(
        string='Audiencias',
        compute='compute_audiencia_count'
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
        string="Número de cédula",
        readonly=True
    )

    #==========RELATIONSHIP==========
    medico_id = fields.Many2one(
        'pp.medico',
        string='Nombre',
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
    x_casa_justicia = fields.Many2one(
        string=u'Casa de Justicia',
        comodel_name='res.company',
        ondelete='set null',
        default=lambda self: self.env.user.company_id,
    )

    #==========METHODS==========
    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'pp.recepcion') or 'Nuevo'
            print "###################### Aqui Create"
        result = super(Recepcion, self).create(vals)
        return result

    @api.multi
    def compute_audiencia_count(self):
        for partner in self:
            partner.audiencias = self.env['pp.audiencia'].search_count(
                [('recepcion_id', '=', partner.id)])
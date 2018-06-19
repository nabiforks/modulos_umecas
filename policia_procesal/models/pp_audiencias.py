# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Audiencias(models.Model):
    _name = 'pp.audiencia'

    name = fields.Char(
        'Acceso',
        required=True,
        readonly=True,
        default=lambda self: 'Nuevo'
    )
    numero_sala = fields.Integer(
        string='Sala de audiencia No.',
    )
    fecha_hora = fields.Datetime(
        string='Fecha y hora',
    )
    hora_ingreso = fields.Float(
        string='Hora de ingreso',
    )
    hora_inicio = fields.Float(
        string='Hora de inico',
    )
    hora_termino = fields.Float(
        string='Hora de término',
    )
    hora_salida = fields.Float(
        string='Hora de salida',
    )
    tipo_audiencia = fields.Char(
        string='Tipo de audiencia',
    )
    
    causa_penal = fields.Char(
        string='Causa penal',
       # related="custodia_id.causa_penal"
    )
    tipo_arribo = fields.Char(
        string='Tipo de arribo',
    )
    resolucion = fields.Text(
        string='Resolución',
    )
    observaciones = fields.Text(
        string='Observaciones (Próxima fecha de audiencia)',
    )

    #Control de audiencias
    tipo_ingreso = fields.Selection([
        ('traslado', 'En traslado'),
        ('voluntaria', 'Presentación voluntaria')],
        string='Tipo de ingreso'
    )
    tipo_egreso = fields.Selection([
        ('libertad', 'Libertad'),
        ('traslado', 'En traslado')],
        string='Tipo de egreso'
    )
    nombre_jefe_grupo_pp = fields.Char(
        string='Nombre',
    )
    pp_cargo = fields.Char(
        string='Cargo',
    )
    pp_grupo = fields.Char(
        string='Grupo',
    )

    #==========RELATIONSHIPS=========
    partner_ids = fields.Many2many(
        'res.partner',
        string='Imputado(s)',
        default=lambda self: self.env.context.get('partner_ids'),
        ondelete='set null',
    )
    juez_ids = fields.Many2many(
        'pp.jueces',
        string='Jueces',
    )
    acceso_ids = fields.One2many(
        'pp.acceso_audiencia',
        'audiencia_id',
        string='Lista de acceso',
    )
    recepcion_id = fields.Many2one(
        'pp.recepcion',
        string=u'Recepción',
        readonly=True,
        ondelete='set null',
    )

    delito_ids = fields.Many2many(
        'umc_delitos',
        string='Delito(s)',
    )
    lugar = fields.Many2one(
        'umc_lugares',
        string='Lugar programado para la audiencia',
    )
    rci = fields.Many2one(
        'pp.responsable',
        string='RCI',
    )
    rsa = fields.Many2one(
         'pp.responsable',
        string='RSA',
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
    x_casa_justicia = fields.Many2one(
        string=u'Casa de Justicia',
        comodel_name='res.company',
        ondelete='set null',
        default=lambda self: self.env.user.company_id,
    )

    #==========METHODS============
    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].sudo().next_by_code(
                'pp.audiencia') or 'Nuevo'
        result = super(Audiencias, self).create(vals)
        return result
    

#=====================================
#| MODELO LISTA DE ACCESO A LA SALA  |
#=====================================
class AccesoAudiencia(models.Model):
    _name = 'pp.acceso_audiencia'

    tipo = fields.Selection([
        ('solicitante', 'Solicitante'),
        ('victima', 'Víctima'),
        ('ofendido', 'Ofendido'),
        ('defensa','Defensa'),
        ('fiscalia','Fiscalia'),
        ('familiar','Familiar imputado'),
        ('familiar_v_o','Familiar víctima(s) u ofendido(s)'),
        ('publico','Público general'),
        ('medios','Medios de comunicación')],
        required=True,
    )
    name = fields.Char(
        string='Nombre',
    )
    audiencia_id = fields.Many2one(
        'pp.audiencia',
        string='Audiencia',
    )
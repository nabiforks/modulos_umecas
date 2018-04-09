# -*- coding: utf-8 -*-

from odoo import fields, models

class Audiencias(models.Model):
    _name = 'pp.audiencia'

    name = fields.Char(
        string='Datos',
        default='Acceso'
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
        string='Hora de termino',
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
        string='Observaciones',
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
    partner_id = fields.Many2one(
        'res.partner',
        string='Imputado',
        required=True,
        default=lambda self: self.env.context.get('partner_id'),
        ondelete='set null',
    )
    juez_id = fields.Many2one(
        'pp.jueces',
        string='Jueces',
    )
    acceso_ids = fields.One2many(
        'pp.acceso_audiencia',
        'audiencia_id',
        string='Lista de acceso',
    )
    custodia_id = fields.Many2one(
        'pp.custodia',
        string=u'Custodia',
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
    

#=====================================
#| MODELO LISTA DE ACCESO A LA SALA  |
#=====================================
class AccesoAudiencia(models.Model):
    _name = 'pp.acceso_audiencia'

    tipo = fields.Selection([
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
    nombre = fields.Char(
        string='Nombre',
    )
    audiencia_id = fields.Many2one(
        'pp.audiencia',
        string='Audiencia',
    )
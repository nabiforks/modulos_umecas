# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models


class Encuestas(models.Model):
    _name = 'umc_evaluacion'
    _inherit = 'mail.thread'

    x_name = fields.Char('Evaluación', required=True, readonly=True,
                         default=lambda self: 'Nuevo')
    x_expediente_id = fields.Many2one(
        'umc_expedientes',
        string=u'Expediente',
        readonly=True,
        ondelete='set null',
    )
    x_evaluador_id = fields.Many2one(
        'hr.employee',
        string=u'Evaluador',
        # readonly=True,
        ondelete='set null',
    )

    partner_id = fields.Many2one(
        'res.partner',
        string=u'Imputado',
        readonly=True,
        default=lambda self: self.env.context.get('partner_id'),
        ondelete='set null',
    )
    x_tipo_entrevista = fields.Selection(
        string=u'Tipo de Entrevista',
        selection=[('ad', 'Adolescente'),
                   ('ret', 'Retenido'), ('int', 'Interno')],
        required=True,
    )
    state = fields.Selection([
        ('solicitud', 'Solicitud'),
        ('entrevista', 'Entrevista'),
        ('analisis', 'Analisis de Riesgo'),
        ('hecho', 'Hecho'),
    ], default='solicitud', readonly=True)
    # Campos de las entrevistas

    x_lugar_entrevista = fields.Char(
        string=u'Lugar',
    )

    x_fecha_entrevista = fields.Datetime(
        string=u'Fecha y hora',
        default=fields.Datetime.now,
    )

    @api.model
    def create(self, vals):
        if vals.get('x_name', 'Nuevo') == 'Nuevo':
            vals['x_name'] = self.env['ir.sequence'].next_by_code(
                'umc_evaluacion') or'Nuevo'
        print vals
        result = super(Encuestas, self).create(vals)
        return result

    @api.multi
    def asignar_borrador(self):
        self.state = 'solicitud'
        print "xxxxxxxxxxxxpartner",self.partner_id.id
        print "xxxxxxxxxxxxpartner--",self.x_domicilio_id.parent_id.id

    @api.multi
    def asignar_evaluador(self):
        if self.x_evaluador_id:
            self.state = 'entrevista'

    @api.multi
    def terminar_entrevista(self):
        self.state = 'analisis'

    @api.multi
    def terminar_analisis(self):
        self.state = 'hecho'

    #///////////////////////////////////////Campos de las entrevistas////////////////
    #///////////////////////////////////////Campos de las entrevistas////////////////
    #///////////////////////////////////////Campos de las entrevistas////////////////

    #/////////////////////Datos personales//////////////
    x_apellido_pat = fields.Char(
        string=u'Apellido Paterno',
        #related='partner_id.lastname',
    )

    x_apellido_mat = fields.Char(
        string=u'Apellido Materno',
        #related='partner_id.x_apellido_mat',
    )
    x_nombre_entrevistado = fields.Char(
        string=u'Nombre(s)',
        #related='partner_id.firstname',
    )
    x_otronombre = fields.Char(
        string=u'Otro nombre',
    )
    x_apodo = fields.Char(
        string=u'Apodo',
    )
    x_lugar_nacimiento = fields.Char(
        string=u'Lugar de Nacimiento',
    )
    x_fecha_nacimiento = fields.Date(
        string=u'Fecha de nacimiento',
    )
    x_edad = fields.Integer(
        string=u'Edad',
    )
    x_sexo = fields.Selection(
        string=u'Sexo',
        selection=[('m', 'Masculino'), ('f', 'Femenino')]
    )

    #///////////////////////// II.-Domicilio/////////////////
    
    x_domicilio_actual = fields.One2many(
        string=u'Domicilio actual',
        comodel_name='umc_domicilio',
        inverse_name='x_evaluacion_id',
    )
    x_domicilio_anterior = fields.One2many(
        string=u'Domicilio anterior',
        comodel_name='umc_domicilio',
        inverse_name='x_evaluacion_id',
    )
    
    
    x_partner_id_id = fields.One2many(
        string=u'test',
        related='partner_id.child_ids'
    )
    
    
    x_domicilio_id = fields.One2many(
        string=u'Domicilio',
        comodel_name='res.partner',
        inverse_name='parent_id',
    )
    
    
    
    

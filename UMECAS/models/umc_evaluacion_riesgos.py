# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models


class Encuestas(models.Model):
    _name = 'umc_evaluacion'
    #_inherit = 'mail.thread'

    x_name = fields.Char('Evaluación', required=True, readonly=True,
                         default=lambda self: 'Nuevo')
    x_expediente_id = fields.Many2one(
        'umc_expedientes',
        string=u'Expediente',
        readonly=True,
        required=True,
        ondelete='set null',
    )
    x_evaluador_id = fields.Many2one(
        'hr.employee',
        string=u'Evaluador',
        required=True,
        ondelete='set null',
    )

    partner_id = fields.Many2one(
        'res.partner',
        string=u'Imputado',
        readonly=True,
        required=True,
        default=lambda self: self.env.context.get('partner_id'),
        ondelete='set null',
    )
    x_imputado_name = fields.Char(
        string=u'Imputado',        
        related='partner_id.display_name',         
        readonly=True,               
    )
    x_tipo_entrevista = fields.Selection(
        string=u'Tipo de Entrevista',
        related='partner_id.x_imputado_tipo'
    )
   
    state = fields.Selection([
        ('solicitud', 'Solicitud'),
        ('entrevista', 'Entrevista'),
        ('analisis', 'Analisis de Riesgo'),
        ('hecho', 'Hecho'),
    ], default='solicitud', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('x_name', 'Nuevo') == 'Nuevo':
            vals['x_name'] = self.env['ir.sequence'].next_by_code(
                'umc_evaluacion') or'Nuevo'
        result = super(Encuestas, self).create(vals)
        return result

    @api.multi
    def asignar_borrador(self):
        self.state = 'solicitud'

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

    x_entrevistas_ids = fields.One2many(
        string=u'Entrevistas',
        comodel_name='umc_entrevistas',
        inverse_name='x_evaluacion_id',
    )

    #///////////////////////////////////////////Evaluación de riesgos///////////////////////////////////////////////
    #///////////////////////////////////////////Evaluación de riesgos///////////////////////////////////////////
    #///////////////////////////////////////////Evaluación de riesgos///////////////////////////////////////////////
    #///////////////////////////////////////////Evaluación de riesgos////////////////////////////////////////////////

    x_fecha_analisis = fields.Date(
        string=u'Fecha Analisis de Riesgos',
        default=fields.Date.context_today,
    )
    x_ponderacion = fields.Integer(
        string=u'Ponderación',
        compute='calcular_ponderacion'
    )
    x_escala_riesgos = fields.Selection(
        string=u'Escala de riesgo',
        selection=[('1', 'Bajo'), ('2', 'Medio'), ('3', 'Alto')],
        compute='calcular_ponderacion'
    )
    x_escalas_ids = fields.One2many(
        string=u'Escala de valores',
        comodel_name='ucm.escalavalores.evaluacion',
        inverse_name='x_evaluacion_id',
        #default=lambda self: self.env['ucm.escalavalores.evaluacion'].search([
        #]).ids,
    )

    @api.multi
    @api.depends('x_escalas_ids')
    def calcular_ponderacion(self):
        for record in self:
            sumador = 0
            for linea_escala in record.x_escalas_ids:
                sumador += linea_escala.num_valor
            record.x_ponderacion = sumador
            if sumador >= 4:
               record.x_escala_riesgos = '1'
            elif sumador <= -7:
                record.x_escala_riesgos = '3'
            else:
                record.x_escala_riesgos = '2'
    #///////////////////////////////////////////Evaluación de riesgos/////////////////////////////////////////////
    
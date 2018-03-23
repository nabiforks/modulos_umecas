# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class umc_evaluacion(models.Model):
    _name = 'umc_evaluacion'
    #_inherit = 'mail.thread'

    x_name = fields.Char('Solicitud de evaluación', required=True, readonly=True,
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
        string=u'Imputado ID',
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
    """x_tipo_entrevista = fields.Selection(
        string=u'Tipo de Entrevista',
        related='partner_id.x_imputado_tipo'
    )"""
    x_tipo_entrevista = fields.Selection(
        [('retenido', 'Retenido'), ('adolescente', 'Adolescente'), ('interno', 'Interno')], default='1', required=True, string=u'Tipo de Entrevista')

    state = fields.Selection([
        ('solicitud', 'Solicitud'),
        ('entrevista', 'Entrevista'),
        ('analisis', 'Escala de Riesgos'),
        ('evaluacion', 'Evaluación'),
    ], default='solicitud', readonly=True, string='Estatus')
    x_casa_justicia = fields.Many2one(
        string=u'Casa de Justicia',
        comodel_name='res.company',
        ondelete='set null',
        readonly=True,
        required=True,
    )

    @api.model
    def create(self, vals):
        if vals.get('x_name', 'Nuevo') == 'Nuevo':
            vals['x_name'] = self.env['ir.sequence'].next_by_code(
                'umc_evaluacion') or'Nuevo'
        result = super(umc_evaluacion, self).create(vals)
        return result

    @api.multi
    def asignar_borrador(self):
        self.state = 'solicitud'

    @api.multi
    def generar_entrevista(self):
        if self.x_evaluador_id:
            self.state = 'entrevista'
            valores_entrevista = {'x_evaluacion_id': self.id,
                                  'x_evaluador_id': self.x_evaluador_id,
                                  'x_imputado_id': self.partner_id,
                                  'x_casa_justicia': self.x_casa_justicia.id}
            res = self.env['umc_entrevistas'].create(valores_entrevista)
            self.x_entrevista_id = res
            return res

    @api.multi
    def terminar_entrevista(self):
        if self.x_entrevista_status == 'terminado':
            self.state = 'analisis'
            secciones = self.env['ucm.escalavalores.secciones'].search([]).ids
            for seccion in secciones:
                self.env['ucm.escalavalores.evaluacion'].create(
                    {'seccion': seccion, 'x_evaluacion_id': self.id})
        else:
            raise ValidationError("La entrevista aun no ha sido terminada")

    @api.multi
    def terminar_analisis(self):
        self.state = 'evaluacion'

    #///////////////////////////////////////Campos de las entrevistas////////////////
    #///////////////////////////////////////Campos de las entrevistas////////////////
    #///////////////////////////////////////Campos de las entrevistas////////////////

    x_entrevista_id = fields.Many2one(
        string=u'Entrevista',
        comodel_name='umc_entrevistas',
        readonly=True,
        ondelete='set null',
    )
    x_entrevista_status = fields.Selection(
        string=u'Estatus de Entrevista',
        readonly=True,
        related='x_entrevista_id.state',
    )

    #///////////////////////////////////////////Escala de riesgos///////////////////////////////////////////////
    #///////////////////////////////////////////Escala de riesgos///////////////////////////////////////////
    #///////////////////////////////////////////Escala de riesgos///////////////////////////////////////////////
    #///////////////////////////////////////////Escala de riesgos////////////////////////////////////////////////

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
        selection=[('bajo', 'Bajo'), ('medio', 'Medio'), ('alto', 'Alto')],
        compute='calcular_ponderacion'
    )
    x_escala_valores_id = fields.Many2one(
        string=u'Escala valores ID',
        comodel_name='umc_escalas',
        store=True,
        default=lambda self: self.env['umc_escalas'].search([]),
        ondelete='set null',
    )

    x_escalas_ids = fields.One2many(
        string=u'Escala de valores',
        comodel_name='ucm.escalavalores.evaluacion',
        inverse_name='x_evaluacion_id',
        #default=lambda self: self.env['ucm.escalavalores.evaluacion'].search([]).ids,
    )

    @api.multi
    @api.depends('x_escalas_ids', 'x_escala_valores_id.x_bajo', 'x_escala_valores_id.x_alto')
    def calcular_ponderacion(self):
        print self.x_escala_valores_id
        for record in self:
            sumador = 0
            for linea_escala in record.x_escalas_ids:
                sumador += linea_escala.num_valor
            record.x_ponderacion = sumador
            if sumador >= self.x_escala_valores_id.x_bajo:
                record.x_escala_riesgos = 'bajo'
            elif sumador <= self.x_escala_valores_id.x_alto:
                record.x_escala_riesgos = 'alto'
            else:
                record.x_escala_riesgos = 'medio'
    #///////////////////////////////////////////Evaluación/////////////////////////////////////////////
    #///////////////////////////////////////////Evaluación/////////////////////////////////////////////
    #///////////////////////////////////////////Evaluación/////////////////////////////////////////////
    #///////////////////////////////////////////Evaluación/////////////////////////////////////////////

    x_conclusion = fields.Text(
        string=u'Conclusión',
    )

# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models


class Encuestas(models.Model):
    _name = 'umc_evaluacion'

    x_name = fields.Char('Evaluación', required=True, readonly=True,
                         default=lambda self: 'Nuevo')
    x_expediente_id = fields.Many2one(
        'umc_expedientes',
        string=u'Expediente',
        readonly=True,
        ondelete='set null',
    )

    partner_id = fields.Many2one(
        'res.partner',
        string=u'Imputado',        
        readonly=True,        
        default= lambda  self: self.env.context.get('partner_id'),
        ondelete='set null',
    )
    x_tipo_entrevista = fields.Selection(
        string=u'Tipo de Entrevista',
        selection=[('ad', 'Adolescente'), ('ret', 'Retenido'), ('int', 'Interno')],
        required=True,
        )
    state = fields.Selection([
        ('entrevista', 'Entrevista'),
        ('analisis', 'Analisis de Riesgo'),
        ('hecho', 'Hecho'),
    ], default='entrevista', readonly=True)
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

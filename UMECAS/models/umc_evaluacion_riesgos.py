# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models


class Encuestas(models.Model):
    _name= 'umc_evaluacion'

    
    partner_id = fields.Many2one(
        'res.partner',        
        string=u'Imputado',
        ondelete='set null',
    )    
    x_tipo_entrevista = fields.Selection(
        string=u'Tipo de Entrevista',
        selection=[('ad', 'Adolescente'), ('ret', 'Retenido'),('int','Interno')])
    state = fields.Selection([
        ('entrevista', 'Entrevista'),
        ('analisis', 'Analisis de Riesgo'),
        ('hecho', 'Hecho'),
    ], default='entrevista', readonly=True)
    #Campos de las entrevistas
    
    x_lugar_entrevista = fields.Char(
        string=u'Lugar',
    )   
    
    x_fecha_entrevista = fields.Datetime(
        string=u'Fecha y hora',
        default=fields.Datetime.now,
    )
    
    
    
# -*- coding: utf-8 -*-
from odoo import api, fields, models


class umc_sustancia(models.Model):
    _name = 'umc_sustancia'

    x_name = fields.Char(
        string=u'Sustancia',
        required=True,
    )
    

class umc_sustancias_consume(models.Model):
    _name = 'umc_sustancias_consume'
    
    x_name= fields.Many2one(
        string=u'Sustancia',
        comodel_name='umc_sustancia',
        required=True,
        ondelete='set null',
    )
    x_frecuencia = fields.Integer(
        string=u'Frecuencia de consumo',
        help='Días a la semana que consume esta sustancia'
    )
    x_cantidad = fields.Char(
        string=u'Cantidad',
    )
    x_ultimo_consumo = fields.Date(
        string=u'Fecha de último',
    )
    x_entrevista_id = fields.Many2one(
        string=u'Entrevista ID',
        comodel_name='umc_entrevistas',
        ondelete='cascade',
    )
    
    
    
    
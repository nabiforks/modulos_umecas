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

    x_intra_extra = fields.Selection(
        string=u'Intramuros/Extramuros',
        selection=[('intramuros', 'Intramuros'), ('extramuros', 'Extramuros')],
        default='extramuros',
    )
    x_name = fields.Many2one(
        string=u'Sustancia',
        comodel_name='umc_sustancia',
        required=True,
        ondelete='set null',
    )
    x_frecuencia = fields.Selection(
        string=u'Frecuencia de consumo',
        help='Días a la semana que consume esta sustancia',
        selection=[('1', 'Cada X hora'), ('2', 'Diario'), ('3', 'Semanal'), ('4', 'Mensual'),
                   ('5', 'Ocacional')]
    )
    x_cantidad = fields.Char(
        string=u'Cantidad',
    )
    x_ultimo_consumo = fields.Date(
        string=u'Fecha de último consumo',
    )
    x_entrevista_id = fields.Many2one(
        string=u'Entrevista ID',
        comodel_name='umc_entrevistas',
        ondelete='cascade',
    )

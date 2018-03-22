# -*- coding: utf-8 -*-
from odoo import api, fields, models


class umc_regiones(models.Model):
    _name = 'umc_regiones'

    x_name = fields.Char(
        string=u'Región',
        required=True,
    )    
    x_codigo = fields.Char(
        string=u'Código',
        required=True,
    )
    
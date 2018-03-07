# -*- coding: utf-8 -*-
from odoo import api, fields, models


class umc_enfermedades(models.Model):
    _name = 'umc_enfermedades'

    x_name = fields.Char(
        string=u'Enfermedad',
        required=True,
    )
    

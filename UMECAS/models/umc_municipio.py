# -*- coding: utf-8 -*-
from odoo import api, fields, models


class umc_municipio(models.Model):
    _name = 'umc_municipio'

    
    name = fields.Char(
        string=u'Municipio',
        required=True,        
    )
    codigo = fields.Char(
        string=u'Código de Municipio',
    )   
    
    estado_id = fields.Many2one(
        string=u'Estado',
        comodel_name='res.country.state',
        ondelete='set null',
    )
    
    
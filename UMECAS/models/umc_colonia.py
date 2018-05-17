# -*- coding: utf-8 -*-
from odoo import api, fields, models


class umc_colonia(models.Model):
    _name = 'umc_colonia'

    name = fields.Char(
        string=u'Colonia',
        required=True,        
    )
    codigo = fields.Char(
        string=u'Código de Colonia',
    )
    x_sector = fields.Selection(
        string=u'Sector',
        selection=[('1', '1'), ('2', '2'),('3', '3'),('4', '4')]
    )
       
    
    municipio_id = fields.Many2one(
        string=u'Municipio',
        comodel_name='umc_municipio',
        ondelete='set null',
    )
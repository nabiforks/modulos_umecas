# -*- coding: utf-8 -*-
from odoo import api, fields, models


class umc_casa_justicia(models.Model):
    _inherit = 'res.company'

    
    x_region = fields.Many2one(
        string=u'Región',
        comodel_name='umc_regiones',
        ondelete='set null',
    )    
    x_abreviatura = fields.Char(
        string=u'Abreviatura',        
        help='Esta abreviatura aparecerá en la nomenclatura del expediente',        
    )
    x_logo_actual = fields.Binary(
        string=u'Logo Administración actual',
    )
    
    
    
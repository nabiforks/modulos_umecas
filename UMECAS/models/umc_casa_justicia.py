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
    #////////////////////////////////////////////////////////
    #//////////////////////////////////////////Renombrar campos para colonia y municipio///////////////////
    """street2 = fields.Many2one(
        string=u'Colonia',
        comodel_name='umc_colonia',
        ondelete='set null',
    )
    city = fields.Many2one(
        string=u'Municipio',
        comodel_name='umc_municipio',
        ondelete='set null',
    )"""
    
    
    
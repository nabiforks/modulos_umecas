# -*- coding: utf-8 -*-
from odoo import api, fields, models


class umc_delitos_proceso(models.Model):
    _name = 'umc_delitos_proceso'

    
    x_name = fields.Many2one(
        string=u'Delito ',
        comodel_name='umc_delitos',        
        required=True,        
        ondelete='set null',
    )
    x_fundamento = fields.Char(
        string=u'Fundamento',
    )
    x_gravedad = fields.Selection(
        string=u'Gravedad',
        selection=[('grave', 'Grave'), ('nograve', 'No grave'),('fed','Fed.')]
    )
        
    x_entrevista_id = fields.Many2one(
        string=u'Entrevista _ID',
        comodel_name='umc_entrevistas',
        ondelete='cascade',
    )
    

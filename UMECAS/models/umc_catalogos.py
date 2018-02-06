# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models

class Delitos(models.Model):
    _name='umc_delitos'

    
    x_name = fields.Char(
        string=u'Delito',
    )
    
    x_expedientes_id = fields.Many2one(
        string=u'Expedientes_ids',
        comodel_name='umc_expedientes',
        ondelete='set null',
    )
    
    


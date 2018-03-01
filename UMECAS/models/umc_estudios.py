# -*- coding: utf-8 -*-
from odoo import api, fields, models


class umc_estudios(models.Model):
    _name = 'umc_estudios'

    x_name = fields.Selection(
        string=u'Escolaridad',
        selection=[('ninguno', 'Ninguno'), ('primaria', 'Primaria')],
        default='ninguno',
        required=True,

    )        
    x_institucion = fields.Char(
        string=u'Nombre de la Institución',
    )    
    x_desercion = fields.Char(
        string=u'Motivo deserción',
    )    
    x_domicilio_ids = fields.One2many(
        string=u'Domicilio',
        comodel_name='umc_domicilio',
        inverse_name='x_estudios_id',
    )
    x_entrevista_id = fields.Many2one(
        string=u'Entrevista ID',
        comodel_name='umc_entrevistas',
        ondelete='set null',
    )
    

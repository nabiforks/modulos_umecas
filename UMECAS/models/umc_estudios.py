# -*- coding: utf-8 -*-
from odoo import api, fields, models


class umc_estudios(models.Model):
    _name = 'umc_estudios'

    
    x_name= fields.Many2one(
        string=u'Escolaridad',
        comodel_name='umc_escolaridad',
        ondelete='set null', 
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
class umc_escolaridad(models.Model):
    _name = 'umc_escolaridad' 
    
    x_name= fields.Char(
        string=u'Nivel escolar',
    )    
    x_codigo = fields.Char(
        string=u'Código',
    )
    
       

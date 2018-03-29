# -*- coding: utf-8 -*-
from odoo import api, fields, models


class umc_enfermedades(models.Model):
    _name = 'umc_enfermedades'

    x_name = fields.Char(
        string=u'Enfermedad',
        required=True,
    )
    
class umc_discapacidad(models.Model):
    _name = 'umc_discapacidad'

    x_name = fields.Char(
        string=u'Discapacidad',
        required=True,
    )
class umc_enfermedades_padece(models.Model):
    _name = 'umc_enfermedades_padece'
    
    x_name= fields.Many2one(
        string=u'Enfermedad que padece',
        comodel_name='umc_enfermedades',
        required=True,
        ondelete='set null',
    )
    x_tiempo_padece = fields.Integer(
        string=u'¿Tiempo de padecimiento?',
    )    
    x_tiempo_unidad = fields.Selection(
        string=u'Días/Semanas/Meses/Años',
        selection=[('dias', 'Días'), ('semanas', 'Semanas'),
                   ('meses', 'Meses'), ('anios', 'Años')]
    )    
    x_tratamiento = fields.Char(
        string=u'¿Recibe tratamiento? (especificar)',
    )
    x_entrevista_id = fields.Many2one(
        string=u'Entrevista ID',
        comodel_name='umc_entrevistas',
        ondelete='cascade',
    )
    
    
    
    
# -*- coding: utf-8 -*-
from odoo import api, fields, models


class umc_amistades(models.Model):
    _name = 'umc_amistades'

    x_name = fields.Char(
        string=u'Nombre Completo',
        required=True,
    )
    x_edad = fields.Integer(
        string=u'Edad',        
        default=18,        
    )    
    x_domicilio_ids = fields.One2many(
        string=u'Domicilio',
        comodel_name='umc_domicilio',
        inverse_name='x_amistades_id',
    )
    x_relacion = fields.Many2one(
        string=u'Tipo de relación',
        comodel_name='umc_parentesco',
        ondelete='set null',
    )
    x_numero = fields.Char(
        string=u'Teléfono (Casa, empleo, cel.)',
    )    
    x_tiempo_cantidad = fields.Integer(
        string=u'Cantidad',
    )
    x_tiempo_unidad = fields.Selection(
        string=u'Días/Semanas/Meses/Años',
        selection=[('dias', 'Días'), ('semanas', 'Semanas'),('meses', 'Meses'),('anios', 'Años')]
    ) 

    x_entrevista_id = fields.Many2one(
        string=u'Entrevista _ID',
        comodel_name='umc_entrevistas',
        ondelete='cascade',
    )
class umc_detenidos_con(models.Model):
    _name = 'umc_detenidos_con'
    _inherit = 'umc_amistades'

    
    test = fields.Boolean(
        string=u'Test',
    )
    x_entrevista_id2 = fields.Many2one(
        string=u'Entrevista _ID',
        comodel_name='umc_entrevistas',
        ondelete='cascade',
    )
    
    

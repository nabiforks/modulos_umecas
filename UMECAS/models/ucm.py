# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class Ucm(models.Model):
    _name = 'ucm.escalavalores.secciones'

    x_seccion_ids = fields.One2many(
        'ucm.escalavalores.valor', 'seccion_id', 'Respuestas')
    name = fields.Char(string='Sección')
    sequence = fields.Integer(
        string=u'Secuencia',      
    )
    """
    x_evaluacion_id = fields.Many2one(
        string=u'Evaluacion ID',
        comodel_name='umc_evaluacion',
        ondelete='set null',
    )
    
    """


class UcmValores(models.Model):
    _name = 'ucm.escalavalores.valor'

    name = fields.Char(string='Respuesta')
    valor = fields.Integer(string='Valor')
    seccion_id = fields.Many2one(
        'ucm.escalavalores.secciones', string='Sección',
        ondelete='cascade',
    )


class UcmEvaluacion(models.Model):
    _name = 'ucm.escalavalores.evaluacion'

    seccion = fields.Many2one('ucm.escalavalores.secciones', string='Sección',required=True)
    valor_ids = fields.Many2one('ucm.escalavalores.valor', string='Respuesta')
    num_valor = fields.Integer(
        'Valor', related='valor_ids.valor', readonly=True,)
    
    sequence = fields.Integer(
        string=u'Secuencia',      
    )
    
    x_evaluacion_id = fields.Many2one(
        string=u'Evaluacion ID',
        comodel_name='umc_evaluacion',
        ondelete='cascade',
    )
    """
    _sql_constraints = [
        ('seccion_unique', 'unique(seccion)', 'la sección ya existe')
    ]"""

class umc_escalas(models.Model):
    _name = 'umc_escalas'
    
    x_name = fields.Char(
        string=u'Descripción',
    )    
    x_bajo = fields.Integer(
        string=u'Bajo: Mayor que: ',
    )
    x_medio = fields.Char(
        string=u'Medio: entre: ',        
        compute='calcular_riesgo_medio'        
    )
    x_alto = fields.Integer(
        string=u'Alto: Menor que: ',
    )    
    @api.depends('x_bajo','x_alto')
    def calcular_riesgo_medio(self):
        if self.x_bajo and self.x_alto:
            self.x_medio= str(self.x_bajo-1)+" y "+str(self.x_alto+1)   

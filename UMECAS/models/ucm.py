# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class Ucm(models.Model):
    _name = 'ucm.escalavalores.secciones'

    x_seccion_ids = fields.One2many(
        'ucm.escalavalores.valor', 'seccion_id', 'Respuestas')
    name = fields.Char(string='Seccion')
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
        'ucm.escalavalores.secciones', string='Seccion',
        ondelete='cascade',
    )


class UcmEvaluacion(models.Model):
    _name = 'ucm.escalavalores.evaluacion'

    seccion = fields.Many2one('ucm.escalavalores.secciones', string='Sección')
    valor_ids = fields.Many2one('ucm.escalavalores.valor', string='Respuesta')
    num_valor = fields.Integer(
        'Valor', related='valor_ids.valor', readonly=True,)

    x_evaluacion_id = fields.Many2one(
        string=u'Evaluacion ID',
        comodel_name='umc_evaluacion',
        ondelete='cascade',
    )
    """
    _sql_constraints = [
        ('seccion_unique', 'unique(seccion)', 'la sección ya existe')
    ]"""

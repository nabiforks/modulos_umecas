# -*- coding: utf-8 -*-
from datetime import timedelta, datetime,date
from odoo import api, fields, models


class umc_domicilio_inherit(models.Model):
    
    _inherit = ['umc_domicilio']

    x_encuadre_id = fields.Many2one(
        string=u'Entrevista encuadre ID',
        comodel_name='sup_entrevista_encuadre',
        ondelete='cascade',
    )

class umc_enfermedades_padece_inherit(models.Model):
    
    _inherit = ['umc_enfermedades_padece']

    x_encuadre_id = fields.Many2one(
        string=u'Entrevista encuadre ID',
        comodel_name='sup_entrevista_encuadre',
        ondelete='cascade',
    )
class umc_empleos_inherit(models.Model):
    
    _inherit = ['umc_empleos']

    x_encuadre_id = fields.Many2one(
        string=u'Entrevista encuadre ID',
        comodel_name='sup_entrevista_encuadre',
        ondelete='cascade',
    )
class res_partner_inherit(models.Model):
    
    _inherit = ['res.partner']

    x_encuadre_id = fields.Many2one(
        string=u'Entrevista encuadre ID',
        comodel_name='sup_entrevista_encuadre',
        ondelete='cascade',
    )
class umc_amistades_inherit(models.Model):
    
    _inherit = ['umc_amistades']

    x_encuadre_id = fields.Many2one(
        string=u'Entrevista encuadre ID',
        comodel_name='sup_entrevista_encuadre',
        ondelete='cascade',
    )
class umc_actividades_inherit(models.Model):
    
    _inherit = ['umc_actividades']

    x_encuadre_id = fields.Many2one(
        string=u'Entrevista encuadre ID',
        comodel_name='sup_entrevista_encuadre',
        ondelete='cascade',
    )
class umc_sustancias_consume_inherit(models.Model):
    
    _inherit = ['umc_sustancias_consume']

    x_encuadre_id = fields.Many2one(
        string=u'Entrevista encuadre ID',
        comodel_name='sup_entrevista_encuadre',
        ondelete='cascade',
    )

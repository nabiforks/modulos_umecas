# -*- coding: utf-8 -*-

from odoo import fields, models

class Imputado(models.Model):
    _inherit = 'res.partner'

    audiencia_id = fields.Many2one(
        'policia_procesal.pp.audiencia',
        string='Audiencia',
        readonly=True, 
    )

    #=====Ver numero de registro de traslados=====
    """traslados_count = fields.Integer(
        compute='compute_traslados_count'
    )

    @api.multi
    def compute_traslados_count(self):
        for imputado in self:
            imputado.traslados_count = self.env['pp.traslado'].search_count(
                [('imputado_id', '=', imputado.id)])"""
# -*- coding: utf-8 -*-
from odoo import fields, models, api

class smart_button_expedientes_inherit(models.Model):
    _inherit = 'umc_expedientes'

    x_registros = fields.Integer(
        string='Registros',
        compute='compute_registros_count'
    )
    

    @api.multi
    def compute_registros_count(self):
        for contador in self:
            contador.x_registros = self.env['sup_mc_scp'].search_count(
                [('x_expediente_id', '=', contador.id)])


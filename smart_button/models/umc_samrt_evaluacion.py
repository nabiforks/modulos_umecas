# -*- coding: utf-8 -*-
from odoo import fields, models, api


class smart_button_umc_expedientes(models.Model):
    _inherit = 'umc_expedientes'

    x_umc_evaluaciones = fields.Integer(
        string='Evaluaciones',
        compute='compute_entrevistas_count'
    )
    #default=lambda self: self.env['helpdesk.ticket'].search_count([('partner_id', '=', self.id)]),

    @api.multi
    def compute_entrevistas_count(self):
        for partner in self:
            partner.x_umc_evaluaciones = self.env['umc_evaluacion'].search_count(
                [('partner_id', '=', partner.id)])
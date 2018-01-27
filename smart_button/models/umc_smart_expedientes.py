# -*- coding: utf-8 -*-
from odoo import fields, models, api


class smart_button_umc_partner(models.Model):
    _inherit = 'res.partner'

    x_expedientes_count = fields.Integer(
        string='Tickets',
        compute='compute_expedientes_count'
    )
    #default=lambda self: self.env['helpdesk.ticket'].search_count([('partner_id', '=', self.id)]),

    @api.multi
    def compute_expedientes_count(self):
        for partner in self:
            partner.x_expedientes_count = self.env['umc_expedientes'].search_count(
                [('partner_id', '=', partner.id)])

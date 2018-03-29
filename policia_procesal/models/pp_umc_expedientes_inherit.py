# -*- coding: utf-8 -*-

from odoo import fields, models

class ExpList(models.Model):
    _inherit = 'umc_expedientes'

    traslado_id = fields.Many2one(
        'pp.traslado',
        string='traslado Id',
    )
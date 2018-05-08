# -*- coding: utf-8 -*-
from odoo import api, fields, models


class sup_eventos(models.Model):

    _inherit = 'calendar.event'
    #_name = 'sup_eventos'

    #_inherits = {'calendar.event': 'id'}

    """x_mc_id = fields.Many2one(
        string=u'Medida Cautelar',
        comodel_name='sup_mc_lines',
        ondelete='set null',
    )"""
    x_supervision_id = fields.Many2one(
        string=u'Supervisión ID',
        comodel_name='sup_mc_scp',
        ondelete='set null',
    )

    x_imputado_name = fields.Char(
        string=u'Imputado',
        readonly=True,
        related='x_supervision_id.x_imputado_id.display_name',
    )

    x_cumplio = fields.Boolean(
        string=u'Cumplió/Realizado',
    )

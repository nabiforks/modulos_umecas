# -*- coding: utf-8 -*-
from odoo import fields, models, api


class umc_evaluacion_inherit(models.Model):
    _inherit = 'umc_evaluacion'

    x_impedimento_id = fields.Many2one(
        string='Oficio de impedimento',
        comodel_name='sup_documentos',
        readonly=True,
        ondelete='restrict',
    )

    @api.multi
    def impedimento(self):
        self.state = 'impedimento'
        if not self.x_impedimento_id:
            res_model = str(self.__class__.__name__)
            valores_documento = {
                'x_orden_name': self.x_name,
                'x_res_model': res_model,
                'x_modelo_id': self.id,
                'x_tipo_documento': 'Oficio de impedimento'
            }
            res = self.env['sup_documentos'].create(valores_documento)
            self.x_impedimento_id = res
            self.x_impedimento_id.impedimento()
            return res
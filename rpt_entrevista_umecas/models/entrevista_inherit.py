# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'umc_entrevistas'

    @api.multi
    def imprimir_reporte_entrevistas(self):
        # self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        if self.state == 'terminado':
            return self.env['report'].get_action(self, 'rpt_entrevista_umecas.detalles_entrevista')
        else:
            return False

    @api.multi
    def imprimir_reporte_entrevistas_escala_riesgos(self):
        if self.state == 'terminado':
            return self.env['report'].get_action(self, 'rpt_entrevista_umecas.detalles_entrevista_escala_riesgos')
        else:
            return False

# -*- coding: utf-8 -*-
from odoo import api, fields, models



class umc_evaluacion_inherit(models.Model):
    _inherit = 'umc_evaluacion'

    @api.multi
    def imprimir_reporte_evaluacion(self):
        #self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        if self.state == 'evaluacion':
            return self.env['report'].get_action(self,'reporte_evaluacion_umecas.detalles_evaluacion')
        else:
            return False
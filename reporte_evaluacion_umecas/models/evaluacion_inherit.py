# -*- coding: utf-8 -*-
from odoo import api, fields, models



class Partner(models.Model):
    _inherit = 'umc_evaluacion'

    #@api.multi
    #def imprimir_reporte_evaluacion(self):
    #    self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
    #    return self.env['report'].get_action('reporte_evaluacion_umecas.evaluacion_umecas_report')
    @api.multi
    def  imprimir_reporte_evaluacion(self):
        print "********************** entrando"
        reporte = self.env.ref('reporte_evaluacion_umecas.evaluacion_umecas_report').report_name
        print reporte
        if reporte:
        #    self.env['mail.template'].browse(template.id).send_mail(self.id)
            self.env['report'].get_action(self,reporte)
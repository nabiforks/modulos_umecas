# -*- coding: utf-8 -*-

from odoo import api, fields, models

ROMAN = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]


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
    def numberToRoman(self, number):
        result = ""
        number = int(number)
        for (arabic, roman) in ROMAN:
            (factor, number) = divmod(number, arabic)
            result += roman * factor
        return result;

class umc_evaluacion_inherit(models.Model):
    _inherit = 'umc_evaluacion'
    
    @api.multi
    def imprimir_reporte_entrevistas_escala_riesgos(self):
        if self.state == 'analisis':
            return self.env['report'].get_action(self, 'rpt_entrevista_umecas.detalles_entrevista_escala_riesgos')
        else:
            return False
    @api.multi
    def numberToRoman(self, number):
        result = ""
        number = int(number)
        for (arabic, roman) in ROMAN:
            (factor, number) = divmod(number, arabic)
            result += roman * factor
        return result;
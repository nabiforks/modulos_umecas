# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Doc_inherit(models.Model):
    _inherit = 'sup_documentos'

    @api.multi
    def imprimir_documento(self):
        return self.env['report'].get_action(self, 'reportes_supervision.report_document')
        print "***************************Documento_inherit"

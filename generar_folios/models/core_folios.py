# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CoreFolios(models.Model):
    _name = 'core_formato_folio'
    formato = fields.Char(required=True)

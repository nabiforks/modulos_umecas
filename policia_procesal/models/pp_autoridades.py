# -*- coding: utf-8 -*-

from odoo import fields, models

class Autoridades(models.Model):
    _name = 'pp.autoridad'

    name = fields.Char(string='Nombre')
    cargo = fields.Char(string='Cargo')
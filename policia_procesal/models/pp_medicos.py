# -*- coding: utf-8 -*-

from odoo import fields, models

class Medicos(models.Model):
    _name = 'pp.medico'

    name = fields.Char(string='Nombre')
    cedula = fields.Char(string='Cédula')
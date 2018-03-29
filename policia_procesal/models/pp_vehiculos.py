# -*- coding: utf-8 -*-

from odoo import fields, models

class Vehiculos(models.Model):
    _name = 'pp.vehiculos'

    name = fields.Char(
        string='Veiculo oficial',
    )
    no_economico = fields.Char(
        string='Número económico',
    )
    placas = fields.Char(
        string='Placas',
    )
    descripcion = fields.Text(
        string='Descripción'
    )
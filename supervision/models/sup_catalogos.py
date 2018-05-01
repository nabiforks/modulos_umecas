# -*- coding: utf-8 -*-

from odoo import fields, models

class CatalogoMC(models.Model):
    _name = 'sup_mc'

    codigo = fields.Char(
        string='Código',
    )
    name = fields.Char(
        string='Nombre',
        required=True,
    )

class CatalogoSCP(models.Model):
    _name = 'sup_scp'

    codigo = fields.Char(
        string='Código',
    )
    name = fields.Char(
        string='Nombre',
        required=True,
    )
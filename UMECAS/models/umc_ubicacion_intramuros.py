# -*- coding: utf-8 -*-

from odoo import api, fields, models


class umc_ubicacion_intramuros(models.Model):
    _name = 'umc_ubicacion_intramuros'

    """x_name = fields.Char(
        string=u'Name',
    )"""
    x_area = fields.Char(
        string=u'Area',
    )
    x_celda = fields.Char(
        string=u'Número celda',
    )
    x_dormitorio = fields.Char(
        string=u'Dormitorio',
    )
    x_estancia = fields.Char(
        string=u'Estancia',
    )
    x_fecha_ingreso = fields.Date(
        string=u'Fecha ingreso',
    )

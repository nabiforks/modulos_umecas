# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models
import json
from geopy.geocoders import Nominatim


class Domicilio(models.Model):
    _name = 'umc_domicilio'

    x_name = fields.Char(
        string=u'Name',
    )

    x_direccion = fields.Char(
        string=u'Domicilio',
    )
    x_vivienda = fields.Selection(
        string=u'Vivienda',
        selection=[('propia', 'Propia'), ('rentada', 'Rentada'), ('prestada', 'Prestada'), ('hipotecada', 'Hipotecada'), ('otro', 'Otro')])
    x_croquis = fields.Char(string="Croquis", default='{"position":{"lat":19.04360786502212,"lng":-98.19820135831833},"zoom":15}',
                            )

    x_evaluacion_id = fields.Many2one(
        string=u'Entrevista',
        comodel_name='umc_evaluacion',
        ondelete='set null',
    )

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
    x_calle = fields.Char(
        string=u'Calle',
    )
    x_colonia = fields.Char(
        string=u'Colonia',
    )
    x_municipio = fields.Char(
        string=u'Municipio',
    )
    x_estado_id = fields.Many2one(
        string=u'Estado',
        comodel_name='res.country.state',
        default=lambda self: 504,
        ondelete='set null',
    )
    """x_pais_id = fields.Many2one(
        string=u'País',
        comodel_name='res.country',
        default=lambda self: 157,
        ondelete='set null',
    )"""
    x_vivienda = fields.Many2one(
        string=u'Tipo Vivienda',
        comodel_name='umc_tipo_vivienda',
        ondelete='set null',
    )
    

    x_croquis = fields.Char(string="Croquis", default='{"position":{"lat":19.04360786502212,"lng":-98.19820135831833},"zoom":15}',
                            )

    x_evaluacion_id = fields.Many2one(
        string=u'Entrevista',
        comodel_name='umc_entrevistas',
        ondelete='set null',
    )

# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models
import json
from geopy.geocoders import Nominatim


class Partner(models.Model):
    #_name = 'umc_imputado'

    _inherit = 'res.partner'

    fecha_nacimiento = fields.Date(string=u'Fecha_Nac')
    fecha_actual = fields.Date(default=fields.Date.today)
    edad = fields.Integer(string="Edad", compute="_calcular_edad")
    x_imputado = fields.Boolean(
        string=u'Imputado',
        default=True,
    )
    x_imputado_tipo = fields.Selection(
        [('1', 'Retenido'), ('2', 'Adolescente'), ('3', 'Interno')], string=u'Tipo')
    
    x_apodo = fields.Char(
        string=u'Apodo / Sobrenombre',
    )    
    x_nacionalidad = fields.Char(
        string=u'Nacionalidad',
    )
    x_originario = fields.Char(
        string=u'Originario',
    )
    x_estado_civil = fields.Selection(
        string=u'Estado Civil',
        selection=[('1', 'Soltero'), ('2', 'Casado'),('3', 'Unión Libre'),('4', 'Divorciado'),('5','Viudo')]
    )
    x_ocupacion = fields.Char(
        string=u'Ocupación',
    )
    x_identificacion = fields.Char(
        string=u'Identificación',
    )
    x_ingreso_economico = fields.Float(
        string=u'Ingreso económico (MXN) diarios',
    )
    
    
    
    
    
    
    
    
    google_map_partner_test = fields.Char(string="Map",
                                          default='{"position":{"lat":19.04360786502212,"lng":-98.19820135831833},"zoom":15}',
                                          )

    @api.depends('fecha_nacimiento', 'fecha_actual')
    def _calcular_edad(self):
        for r in self:
            if not (r.fecha_nacimiento and r.fecha_actual):
                continue
            # diff = (datetime.date.today() - r.fecha_nac).days
            #r.edad =  int(diff / 365)
            #start_date = fields.Date.today
            start_date = fields.Datetime.from_string(r.fecha_nacimiento)
            end_date = fields.Datetime.from_string(r.fecha_actual)
            r.edad = (end_date - start_date).days / 365
            #r.edad = 10 * 10

    @api.onchange('google_map_partner_test')
    def latitud_longitud(self):
        print "xxxxxxxxxxxxxxx", self.google_map_partner_test
        o = json.loads(self.google_map_partner_test)
        print o['position']['lat']
        self.partner_latitude = o['position']['lat']
        self.partner_longitude = o['position']['lng']
        geolocator = Nominatim()
        geol = str(o['position']['lat']) + " , " + str(o['position']['lng'])
        location = geolocator.reverse(geol)
        # print location.address
        print geol

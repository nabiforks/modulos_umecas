# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models
#import json
#from geopy.geocoders import Nominatim


class Partner(models.Model):
    #_name = 'umc_imputado'

    _inherit = 'res.partner'

    @api.multi 
    def name_get(self): 
        result = super(Partner, self).name_get() 
        res = [] 
        for element in self: 
            name = '' 
            name += element.display_name or '' 
            res.append((element.id, name)) 
        return res

    fecha_nacimiento = fields.Date(string=u'Fecha_Nac')
    fecha_actual = fields.Date(default=fields.Date.today)
    # edad = fields.Integer(string="Edad")
    edad = fields.Integer(string="Edad", compute="_calcular_edad")
    x_imputado = fields.Boolean(
        string=u'Imputado',
    )
    x_sexo = fields.Selection(
        string=u'Sexo',
        selection=[('m', 'Masculino'), ('f', 'Femenino'),('o', 'Otro')]
    )    
    
    x_imputado_tipo = fields.Selection(
        [('retenido', 'Retenido'), ('adolescente', 'Adolescente'), ('interno', 'Interno')],  string=u'Tipo de imputado')

    x_apodo = fields.Char(
        string=u'Apodo / Sobrenombre',
    )
    x_nacionalidad = fields.Many2one(
        string=u'Nacionalidad',
        comodel_name='umc_nacionalidad',
        ondelete='cascade',
        default=lambda self: self.env['umc_nacionalidad'].search(
            [('x_name', 'ilike', 'Mexican')]),

    )
    x_originario = fields.Char(
        string=u'Originario de: ',
    )
    x_estado_civil = fields.Selection(
        string=u'Estado civil',
        selection=[('soltero', 'Soltero'), ('casado', 'Casado'),
                   ('cuncubinato', 'Cuncubinato'), ('otro', 'Otro')]
    )
    x_identificacion = fields.Many2one(
        string=u'Identificación',
        comodel_name='umc_identificacion',
        ondelete='cascade',
    )
    x_ingreso_economico = fields.Char(
        string=u'Ingreso económico',
    )

    """
    google_map_partner_test = fields.Char(string="Map",
                                          default='{"position":{"lat":19.04360786502212,"lng":-98.19820135831833},"zoom":15}',
                                          )
    """
    
    @api.depends('fecha_nacimiento', 'fecha_actual')
    def _calcular_edad(self):
        for r in self:
            if not (r.fecha_nacimiento and r.fecha_actual):
                continue
            # diff = (datetime.date.today() - r.fecha_nac).days
            # r.edad =  int(diff / 365)
            # start_date = fields.Date.today
            start_date = fields.Datetime.from_string(r.fecha_nacimiento)
            end_date = fields.Datetime.from_string(r.fecha_actual)
            r.edad = (end_date - start_date).days / 365
            # r.edad = 10 * 10
    
    """
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
    """
    #//////////////////////////////////////////Renombrar campos para colonia y municipio////////////
    #//////////////////////////////////////////Renombrar campos para colonia y municipio////////////
    #//////////////////////////////////////////Renombrar campos para colonia y municipio/////////////////
    #//////////////////////////////////////////Renombrar campos para colonia y municipio///////////////////
    street2 = fields.Many2one(
        string=u'Colonia',
        comodel_name='umc_colonia',
        ondelete='set null',
    )
    city = fields.Many2one(
        string=u'Municipio',
        comodel_name='umc_municipio',
        ondelete='set null',
    )
    #//////////////////////////////////////////Campos usados en entrevista////////////
    #//////////////////////////////////////////Campos usados en entrevista////////////
    #//////////////////////////////////////////Campos usados en entrevista/////////////////
    #//////////////////////////////////////////Campos usados en entrevista///////////////////
    x_parentesco = fields.Many2one(
        string=u'Parentesco',
        comodel_name='umc_parentesco',
        ondelete='set null',
    )
    x_entrevistas_id = fields.Many2one(
        string=u'Entrevista',
        comodel_name='umc_entrevistas',
        ondelete='set null',
    )
    x_ocupacion = fields.Many2one(
        string=u'Ocupación',
        comodel_name='umc_ocupacion',
        ondelete='set null',
    )
    x_habita_domicilio = fields.Boolean(
        string=u'¿Habita el mismo domicilio?',
    )
    x_dependiente_economico = fields.Boolean(
        string=u'Dependiente económico',
    )
    x_domicilio = fields.Char(
        string=u'Domicilio',
    )
    x_nucleo = fields.Selection(
        string=u'Núcleo',
        selection=[('primario', 'Primario'),('secundario','Secundario')]
    )
    #//////////////////////////////////////////one2many Expedientes////////////
    #//////////////////////////////////////////one2many Expedientes////////////
    #//////////////////////////////////////////one2many Expedientes/////////////////
    #//////////////////////////////////////////one2many Expedientes///////////////////
    
    
    x_expedientes_ids = fields.One2many(
        string=u'Expedientes',
        comodel_name='umc_expedientes',
        inverse_name='partner_id',
    )
    

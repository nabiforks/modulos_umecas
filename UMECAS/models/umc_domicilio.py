# -*- coding: utf-8 -*-
import json
import urllib2
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


def geo_find(addr):
    if not addr:
        return None
    url = 'https://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='
    url += urllib2.quote(addr.encode('utf8'))

    try:
        result = json.load(urllib2.urlopen(url))
    except Exception as e:
        raise UserError(
            _('Cannot contact geolocation servers. Please make sure that your Internet connection is up and running (%s).') % e)

    if result['status'] != 'OK':
        return None

    try:
        geo = result['results'][0]['geometry']['location']
        return float(geo['lat']), float(geo['lng'])
    except (KeyError, ValueError):
        return None


def geo_query_address(street=None, zip=None, city=None, state=None, country=None):
    if country and ',' in country and (country.endswith(' of') or country.endswith(' of the')):
        # put country qualifier in front, otherwise GMap gives wrong results,
        # e.g. 'Congo, Democratic Republic of the' => 'Democratic Republic of the Congo'
        country = '{1} {0}'.format(*country.split(',', 1))
    return tools.ustr(', '.join(filter(None, [street,
                                              ("%s %s" %
                                               (zip or '', city or '')).strip(),
                                              state,
                                              country])))


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[('map', _('Map'))])


class IrActionsActWindowView(models.Model):
    _inherit = 'ir.actions.act_window.view'

    view_mode = fields.Selection(selection_add=[('map', _('Map'))])


class IrActionsActWindow(models.Model):
    _inherit = 'ir.actions.act_window'

    view_type = fields.Selection(selection_add=[('map', _('Map'))])


class Domicilio(models.Model):
    _name = 'umc_domicilio'

    x_name = fields.Char(
        string=u'Domicilio', required=True, readonly=True,
        default=lambda self: 'Nuevo'
    )

    @api.model
    def create(self, vals):
        if vals.get('x_name', 'Nuevo') == 'Nuevo':
            vals['x_name'] = self.env['ir.sequence'].next_by_code(
                'umc_domicilio') or'Nuevo'
        result = super(Domicilio, self).create(vals)
        return result
    x_calle = fields.Char(
        string=u'Calle',
    )
    #x_colonia = fields.Char(
    #    string=u'Colonia',
    #)
    
    x_colonia= fields.Many2one(
        string=u'Colonia',
        comodel_name='umc_colonia',
        ondelete='set null',
    )    
    #x_municipio = fields.Char(
    #    string=u'Municipio',
    #)    
    x_municipio= fields.Many2one(
        string=u'Municipio',
        comodel_name='umc_municipio',
        ondelete='set null',
    )
    
    x_estado_id = fields.Many2one(
        string=u'Estado',
        comodel_name='res.country.state',
        default=lambda self: 504,
        ondelete='set null',
    )
    x_cp = fields.Char(
        string=u'C.P.',
    )
    x_pais_id = fields.Many2one(
        string=u'País',
        comodel_name='res.country',
        default=lambda self: 157,
        ondelete='set null',
    )

    x_vivienda = fields.Many2one(
        string=u'Tipo Vivienda',
        comodel_name='umc_tipo_vivienda',
        ondelete='set null',
    )
    x_vivienda_name = fields.Char(
        string=u'Vivienda nombre',
        related='x_vivienda.x_name',
    )
    x_porquien = fields.Char(
        string=u'¿Por quien?',
    )

    x_tipo_domicilio = fields.Selection(
        string=u'Tipo de domicilio ',
        selection=[('actual', 'Actual'), ('secundario',
                                          'Secundario'), ('anterior', 'Anterior')],
        default='actual',
    )
    x_motivo_mudanza = fields.Text(
        string=u'Motivos de mudanza',
    )
    x_caracteristicas_ref = fields.Text(
        string=u'Caracteristicas y referencias',
    )
    x_tiempo_cantidad = fields.Integer(
        string=u'Cantidad',
    )
    x_tiempo_unidad = fields.Selection(
        string=u'Días/Semanas/Meses/Años',
        selection=[('dias', 'Días'), ('semanas', 'Semanas'),
                   ('meses', 'Meses'), ('anios', 'Años')]
    )
    latitud = fields.Float(string='Geo Latitude', digits=(16, 5))
    longitud = fields.Float(string='Geo Longitude', digits=(16, 5))
    #///////////////OBTENER GEOLOCALIZACIÓN

    @api.multi
    def geo_localiza(self):
        # We need country names in English below
        for partner in self.with_context(lang='en_US'):
            result = geo_find(geo_query_address(street=partner.x_calle,
                                                zip=partner.x_cp,
                                                city=partner.x_municipio,
                                                state=partner.x_estado_id.name,
                                                country=partner.x_pais_id.name))
            if result is None:
                result = geo_find(geo_query_address(
                    city=partner.x_municipio,
                    state=partner.x_estado_id.name,
                    country=partner.x_pais_id.name
                ))

            if result:
                partner.write({
                    'latitud': result[0],
                    'longitud': result[1],
                })
        return True
    #////////////////Modelos que hacen referencia a este modelo
    #////////////////Modelos que hacen referencia a este modelo
    #////////////////Modelos que hacen referencia a este modelo
    x_evaluacion_id = fields.Many2one(
        string=u'Entrevista ID',
        comodel_name='umc_entrevistas',
        ondelete='cascade',
    )
    x_empleo_id = fields.Many2one(
        string=u'Empleo ID',
        comodel_name='umc_empleos',
        ondelete='cascade',
    )
    x_amistades_id = fields.Many2one(
        string=u'Amistades ID',
        comodel_name='umc_amistades',
        ondelete='cascade',
    )
    x_estudios_id = fields.Many2one(
        string=u'Estudio ID',
        comodel_name='umc_estudios',
        ondelete='cascade',
    )

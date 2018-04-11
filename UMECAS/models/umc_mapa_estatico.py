# coding:utf-8
from __future__ import print_function
from __future__ import division


import requests
from odoo import api, fields, models


# URLs antiguas
#
url = "https://maps.googleapis.com/maps/api/staticmap?center=-38.25466,-4.971062&zoom=13&size=600x300&maptype=roadmap&markers=color:blue|label:S|40.702147,-74.015794&markers=color:green|label:G|40.711614,-74.012318&markers=color:red|label:C|40.718217,-73.998284"
tmp_url = "https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=17&size=800x400&maptype=roadmap&markers=color:green|label:|{lat},{lon}"


class Entrevistas_inherit_mapa(models.Model):

    _inherit = 'umc_entrevistas'

    def crea_url(self, datos):
        return tmp_url.format(**datos)

    def save_imagen(self, datos):
        url = self.crea_url(datos)
        r = sesion.get(url)
        f = open('/odoo/modulos_umecas/UMECAS/static/img/%s.png' % datos["nombre"], 'wb')
        f.write(r.content)
        f.close()


#proxy = "10.238.8.23:8080"
proxies = {}
sesion = requests.Session()
sesion.proxies = proxies

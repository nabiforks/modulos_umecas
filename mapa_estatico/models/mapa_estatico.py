# coding:utf-8
from __future__ import print_function
from __future__ import division


import requests

# URLs antiguas
#
url ="https://maps.googleapis.com/maps/api/staticmap?center=-38.25466,-4.971062&zoom=13&size=600x300&maptype=roadmap&markers=color:blue|label:S|40.702147,-74.015794&markers=color:green|label:G|40.711614,-74.012318&markers=color:red|label:C|40.718217,-73.998284"
tmp_url="https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=17&size=400x400&maptype=roadmap&markers=color:green|label:|{lat},{lon}"


def crea_url(datos):
    return tmp_url.format(**datos)


def save_imagen(datos):
    url = crea_url(datos)
    r = sesion.get(url)
    f = open('%s.png' % datos["nombre"], 'wb')
    f.write(r.content)
    f.close()


#proxy = "10.238.8.23:8080"
proxies = {}
sesion = requests.Session()
sesion.proxies = proxies

# Aqui se modifican los datos
datos = {"lat": 19.02424, "lon": -98.20194, "nombre": "gm2img"}

save_imagen(datos)

# -*- coding: utf-8 -*-
{
    'name': "Mapa estatico",

    'summary': """
        Genera un png de un mapa
        """,

    'description': """
        Recibe latitud y longitud y regresa una ruta con una imagen .png con 
        el mapa
    """,

    'author': "pcs@soluciones4g.com",
    'website': "soluciones4g.com",

    'category': 'Extra Tools',
    'version': '1.0',

    'depends': ['base'],
    'external_dependencies': {'python': ['requests']},
    'data': [
        # 'security/accesos.csv',

    ],

    'installable': True,
    'auto_install': False,
}

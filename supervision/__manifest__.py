# -*- coding: utf-8 -*-
{
    'name': "Supervisión - UMECAS",

    'summary': """Módulo de Supervisión para UMECAS""",

    'description': """
        Control de medidad cautelares, firmas y SCPP 
    """,

    'author': "pcs@soluciones4g",
    'website': "http://www.soluciones4g.com",
    'category': 'Test',
    'version': '0.1',
    'depends': ['base','mail','UMECAS'],
    'data': [
        'views/sup_menu_items.xml',
        'data/datos_demo.xml',
        'views/sup_catalogos.xml',
    ],
    'intallable': True,
    'auto_install': False,
}

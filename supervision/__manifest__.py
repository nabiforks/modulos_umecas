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
        'data/sequence_names.xml',
        'views/sup_mc_scp.xml',
        'views/sup_expedientes_inherit.xml',
    ],
    'intallable': True,
    'auto_install': False,
}

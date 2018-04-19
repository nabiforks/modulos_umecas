# -*- coding: utf-8 -*-
{
	'name': "Policía Procesal",

    'summary': """
        Administrar procesos de policia procesal""",

    'description': """
        Modulo funcional para policia procesal
    """,

    'author': "S4G",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['UMECAS','base'],

    # always loaded
    'data': [
       'security/security.xml',
       'security/ir.model.access.csv',
       'views/pp_catalogos_view.xml',
       'views/pp_recepcion_view.xml',
       'views/pp_custodia_provicional_view.xml',
       'views/pp_audiencias_view.xml',
       'views/pp_resoluciones_view.xml',
       'views/pp_egresos_view.xml',
       'views/pp_menus_view.xml',
       'data/sequence_names.xml'
    ],
    'installable':True,
    'auto_install':False,
}
# -*- coding: utf-8 -*-
{
	'name': "Policía Procesal",

    'summary': """
        Administrar procesos de policia procesal""",

    'description': """
        Modulo funcional para policia procesal
    """,

    'author': "AHC",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr','UMECAS','base'],

    # always loaded
    'data': [
       'views/pp_traslados_view.xml',
       'views/pp_retiro_traslados_view.xml',
       'views/pp_autoridades_view.xml',
       'views/pp_resguardo_pertenencias_view.xml',
       'views/pp_medicos_view.xml',
       'views/pp_vehiculos_view.xml',
       'views/pp_custodia_provicional_view.xml',
       'views/pp_audiencias_view.xml',
       'views/pp_suministro_alimentos_view.xml',
       'views/pp_menus_view.xml',
       'data/sequence_names.xml'
    ],
    'installable':True,
    'auto_install':False,
}
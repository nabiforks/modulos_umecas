# -*- coding: utf-8 -*-
{
    'name': "UMECAS - smart button",

    'summary': """
    Agregar smart button a los imputados y expedientes
    """,

    'description': """
        smart button a imputados para acceder a los expedientes del imputado,
        smart button a expedientes para acceder a las solicitudes de evaluación de ee expediente
    """,

    'author': "Soluciones4g",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','UMECAS'],

    # always loaded
    'data': [
        'views/add_button_partner.xml',
    ],
    'installable':True,
    'auto_install':False,
}

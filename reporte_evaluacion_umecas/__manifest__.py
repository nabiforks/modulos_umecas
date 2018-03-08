# -*- coding: utf-8 -*-
{
    'name': "Reporte de evaluaciones / UMECAS",

    'summary': """
        Generación de reporte de evaluaciones para UMECAS
        """,

    'description': """
        Generar reporte desde la vista de evaluaciones 
    """,

    'category': 'Extra Tools',
    'version': '1.0',

    'depends': ['base','UMECAS'],

    'data': [
        'report/reporte_evaluacion.xml',
    ],

    'installable':True,
    'auto_install':False,
}
# -*- coding: utf-8 -*-
{
    'name': "Reportes para policia procesal",

    'summary': """
        Generación de reportes para Policia procesal
        """,

    'description': """
        Generar reportes desde las vistas de Policia Procesal 
    """,

    'category': 'Extra Tools',
    'version': '1.0',

    'depends': ['base','policia_procesal'],

    'data': [
        'report/reporte_recepcion.xml',
        'report/reporte_traslado.xml',
        'report/reporte_lectura_derechos.xml',
    ],

    'installable':True,
    'auto_install':False,
}
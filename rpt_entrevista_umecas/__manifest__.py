# -*- coding: utf-8 -*-
{
    'name': "Reporte de entrevistas / UMECAS",

    'summary': """
        Generación de reporte de entrevistas para UMECAS
        """,

    'description': """
        Generar reporte desde la vista de evaluaciones 
    """,

    'author': "soluciones4g",
    'website': "http://www.soluciones4g.com",

    'category': 'Extra Tools',
    'version': '1.0',

    'depends': ['base', 'UMECAS'],

    'data': [
        'report/reportes_entrevista.xml',
        'report/reportes_entrevista_escala_riesgo.xml',
        'views/entrevista_inherit.xml',
        'report/external_layout_inherit.xml',
        'report/reportes_corroboracion.xml'
        # 'security/accesos.csv',
    ],

    'installable': True,
    'auto_install': False,
}

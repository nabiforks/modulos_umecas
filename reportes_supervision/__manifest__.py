# -*- coding: utf-8 -*-
{
    'name': "Reporte de MC y SCP - Supervisón UMECAS",

    'summary': """
        Generación de reporte Medidas cautelares y suspension condicional del proceso
        """,

    'description': """
        Generar reporte desde ordenes de supervision
        
    """,

    'category': 'Extra Tools',
    'version': '1.0',

    'depends': ['base','UMECAS'],

    'data': [
        'report/reporte_mc_scp.xml',
        #'views/evaluacion_inherit.xml',
        #'security/accesos.csv',
    ],

    'installable':True,
    'auto_install':False,
}
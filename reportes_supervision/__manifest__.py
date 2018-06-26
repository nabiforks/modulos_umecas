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

    'depends': ['base','UMECAS','supervision'],

    'data': [
        'data/report_format.xml',
        'report/reporte_evaluacion_inherit.xml',
        'report/reporte_entrevista.xml',
        'report/reporte_actividades.xml',
        'report/reporte_documentos.xml',
        'views/documentos_inherit.xml',
        #'views/evaluacion_inherit.xml',
        #'security/accesos.csv',
    ],

    'installable':True,
    'auto_install':False,
}
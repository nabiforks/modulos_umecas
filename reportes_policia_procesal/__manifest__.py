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
        'report/reporte_pertenencias_alimentos.xml',
        'report/reporte_acceso_audiencia.xml',
        'report/reporte_datos_resolucion.xml',
        'report/reporte_control_audiencia.xml',
        'report/reporte_egreso.xml',
        'report/reporte_retiro_traslado.xml',
    ],

    'installable':True,
    'auto_install':False,
}
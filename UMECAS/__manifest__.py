# -*- coding: utf-8 -*-
{
    'name': "UMECAS",

    'summary': """Módulo para UMECAS""",

    'description': """
        Administración expedientes para incautados, procesados y adolescentes
        control de entrevistas y seguimiento  
    """,

    'author': "soluciones4g",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','mail'],

    # always loaded
    'data': [
        #'views/vista_ssp.xml',
        'security/umc_grupos.xml',
        'security/ir.model.access.csv',        
        'views/vista_umc_imputado.xml',
        'views/vista_umc_expedientes.xml',
        'views/vista_umc_evaluacion.xml',
        'views/umc_entrevistas.xml',
        'views/umc_empleos.xml',
        'views/umc_estudios.xml',
        'views/umc_catalogos.xml',                
        'data/sequence_names.xml',
        'views/vista_umc_domicilio.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo_curso.xml',
    ],
    'intallable': True,
    'auto_install': False,
}

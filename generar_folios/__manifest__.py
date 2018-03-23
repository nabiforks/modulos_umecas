# -*- coding: utf-8 -*-
{
    'name': "Generar Folios",

    'summary': """
        Generación de Folios personalizados
        """,

    'description': """
        Generación de Folios personalizados
    """,

    'author': "mdark1001",
    'website': "https://mdark1001.github.io/",

    'category': 'Extra Tools',
    'version': '1.0',

    'depends': ['base'],

    'data': [
        # 'security/accesos.csv',
        'views/generar_folios_view_tree.xml',
        'views/generar_tipo_folio.xml',
        'views/menu.xml'
    ],

    'installable': True,
    'auto_install': False,
}

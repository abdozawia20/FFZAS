# -*- coding: utf-8 -*-
{
    'name': "FFZAS",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/reservation_view.xml',
        'views/res_users_views.xml',
        'views/res_config_settings_view.xml'
    ],

    'installable': True,
    'application': True,
}


# -*- coding: utf-8 -*-

{
    'name': 'Record deletion history logs',
    'version': '1.0.1.2',
    'author':'Soft-integration',
    'category': 'Security/Access rights',
    'description': "",
    'depends': [
        'mail'
    ],
    'data': [
        'security/record_deletion_history_log_security.xml',
        'security/ir.model.access.csv',
        'views/record_deletion_history_views.xml',
        'views/record_deletion_history_menuitem.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

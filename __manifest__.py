{
    'name': 'Coffre-fort client',
    'version': '2.0.2',
    'summary': 'Un module pour enregistrer des documents',
    'sequence': 30,
    'description': """Un module pour enregistrer des documents""",
    'author': 'pixelblank',
    'website': '',
    'category': 'Document Management',
    'depends': ['base_setup', 'base', 'contacts', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/vault_views.xml',
        'views/res_partner_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            ('prepend','client_vault/static/src/css/style.css'),
            'client_vault/static/src/js/*',
        ],
    },
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

# -*- coding: utf-8 -*-
{
    'name': "apotek",

    'summary': """
        ini summary udah diganti ya""",

    'description': """
        cuma deskrpsi yang udah di upgrade
    """,

    'author': "bj",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','board','mail','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/templates.xml',
        'views/menu.xml',
        'views/dokter_view.xml',
        'views/pasien_view.xml',
        'views/rekmedis_view.xml',
        'views/penjualan_view.xml',
        'views/tempat_obat_view.xml',
        'views/tipemedis_view.xml',
        'views/rawat_inap_view.xml',
        'views/obat_view.xml',
        'views/idp_view.xml',
        'views/rujukan_view.xml',
        'views/kunjungan_view.xml',

        'views/dashboard.xml',
        'views/dpenjualan_view.xml',

        # 'views/tes_view.xml',

        'report/r_rujukan.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

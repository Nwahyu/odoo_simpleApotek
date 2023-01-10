# -*- coding: utf-8 -*-
# from odoo import http


# class Apotek(http.Controller):
#     @http.route('/apotek/apotek', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/apotek/apotek/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('apotek.listing', {
#             'root': '/apotek/apotek',
#             'objects': http.request.env['apotek.apotek'].search([]),
#         })

#     @http.route('/apotek/apotek/objects/<model("apotek.apotek"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('apotek.object', {
#             'object': obj
#         })

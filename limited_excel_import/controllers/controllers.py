# -*- coding: utf-8 -*-
# from odoo import http


# class LimitedExcelImport(http.Controller):
#     @http.route('/limited_excel_import/limited_excel_import', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/limited_excel_import/limited_excel_import/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('limited_excel_import.listing', {
#             'root': '/limited_excel_import/limited_excel_import',
#             'objects': http.request.env['limited_excel_import.limited_excel_import'].search([]),
#         })

#     @http.route('/limited_excel_import/limited_excel_import/objects/<model("limited_excel_import.limited_excel_import"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('limited_excel_import.object', {
#             'object': obj
#         })

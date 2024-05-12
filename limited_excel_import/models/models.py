# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class limited_excel_import(models.Model):
#     _name = 'limited_excel_import.limited_excel_import'
#     _description = 'limited_excel_import.limited_excel_import'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

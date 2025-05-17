from odoo import models, fields

class TodoTag(models.Model):
    _name = 'todo.tag'
    _description = 'Todo Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color Index')
from odoo import models, fields

class TodoTag(models.Model):
    _name = 'todo.tag'
    _description = 'Todo Tag'

    name = fields.Char(string='Tag Name', required=True)
    # color = fields.Integer(string='Color Index') # Optional

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists!"),
    ]
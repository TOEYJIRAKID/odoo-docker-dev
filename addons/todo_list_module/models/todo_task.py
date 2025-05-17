from odoo import models, fields, api

class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Todo Task Item'

    todo_list_id = fields.Many2one('todo.list', string='Todo List', required=True, ondelete='cascade')
    name = fields.Char(string='Task Name', required=True)
    description = fields.Text(string='Description')
    is_complete = fields.Boolean(string='Completed?', default=False)
    sequence = fields.Integer(string='Sequence', default=10) # For ordering

    # To link the visibility of 'is_complete' to the parent's state
    todo_list_state = fields.Selection(related='todo_list_id.state', string="Todo List Status", store=True)
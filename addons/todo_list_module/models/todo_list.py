from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class TodoList(models.Model):
    _name = 'todo.list'
    _description = 'Todo List'
    _order = 'date_start, id'

    name = fields.Char(string='Title', required=True)
    tag_ids = fields.Many2many('todo.tag', string='Tags')
    date_start = fields.Datetime(string='Start Date', required=True)
    date_end = fields.Datetime(string='End Date', required=True)
    state = fields.Selection([
        ('draft', 'DRAFT'),
        ('in_progress', 'IN PROGRESS'),
        ('complete', 'COMPLETE')
    ], string='Status', default='draft')
    
    task_ids = fields.One2many('todo.task', 'todo_list_id', string='Tasks')

    attendee_ids = fields.Many2many(
        'res.users', 
        string='Attendee',
        domain=[('share', '=', False)]
    )
    
    all_tasks_completed = fields.Boolean(compute='_compute_all_tasks_completed', store=True)
    
    @api.depends('task_ids', 'task_ids.is_done')
    def _compute_all_tasks_completed(self):
        for record in self:
            if record.task_ids:
                record.all_tasks_completed = all(task.is_done for task in record.task_ids)
            else:
                record.all_tasks_completed = False
    
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end and record.date_start >= record.date_end:
                raise ValidationError(_("End date must be greater than start date."))
    
    def action_start_progress(self):
        self.write({'state': 'in_progress'})
    
    def action_mark_done(self):
        self.write({'state': 'complete'})

class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Todo Task'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    is_done = fields.Boolean(string='Is Complete', default=False)
    todo_list_id = fields.Many2one('todo.list', string='Todo List', ondelete='cascade', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    
    @api.model
    def create(self, vals):
        task = super().create(vals)
        task.todo_list_id._compute_all_tasks_completed()
        return task
    
    def write(self, vals):
        result = super().write(vals)
        if 'is_done' in vals:
            for task in self:
                task.todo_list_id._compute_all_tasks_completed()
        return result
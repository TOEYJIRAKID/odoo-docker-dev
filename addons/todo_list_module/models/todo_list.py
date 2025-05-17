from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class TodoList(models.Model):
    _name = 'todo.list'
    _description = 'Todo List'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # For chatter and activities

    name = fields.Char(string='Title', required=True, tracking=True)
    tag_ids = fields.Many2many('todo.tag', string='Tags')
    start_date = fields.Datetime(string='Start Date', required=True, default=fields.Datetime.now, tracking=True)
    end_date = fields.Datetime(string='End Date', required=True, tracking=True)
    task_ids = fields.One2many('todo.task', 'todo_list_id', string='Tasks')
    attendee_ids = fields.Many2many('res.users', string='Attendees', domain=[('share', '=', False)], default=lambda self: self.env.user) # Internal users

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('complete', 'Complete'),
    ], string='Status', default='draft', required=True, tracking=True, copy=False)

    # For the "Done" button visibility
    all_tasks_done = fields.Boolean(compute='_compute_all_tasks_done', string="All Tasks Done?")

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(_("End Date cannot be earlier than Start Date."))

    def action_start_progress(self):
        self.ensure_one()
        if self.state == 'draft':
            self.write({'state': 'in_progress'})
        else:
            raise UserError(_("Todo list is not in draft state."))
        return True

    @api.depends('task_ids', 'task_ids.is_complete')
    def _compute_all_tasks_done(self):
        for record in self:
            if not record.task_ids:
                record.all_tasks_done = False # Or True if no tasks means "done" by definition
            else:
                record.all_tasks_done = all(task.is_complete for task in record.task_ids)

    def action_mark_complete(self):
        self.ensure_one()
        if not self.all_tasks_done:
            raise UserError(_("Not all tasks are completed yet!"))
        self.write({'state': 'complete'})
        # To make it read-only, you'd typically control this via view attributes based on state
        return True

    # Optional: Override write method to prevent edits when 'complete'
    # This is a more robust way than just hiding fields in the view.
    def write(self, vals):
        for record in self:
            if record.state == 'complete' and any(field in vals for field in ['name', 'tag_ids', 'start_date', 'end_date', 'task_ids', 'attendee_ids']):
                # Allow state changes or specific fields if needed
                if not (len(vals) == 1 and 'state' in vals): # Example: allow only state change if necessary
                    raise UserError(_("Cannot modify a completed Todo List."))
        return super(TodoList, self).write(vals)

    # Optional: Override unlink method
    def unlink(self):
        for record in self:
            if record.state == 'complete':
                raise UserError(_("Cannot delete a completed Todo List."))
        return super(TodoList, self).unlink()
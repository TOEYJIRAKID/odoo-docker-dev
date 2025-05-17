from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class TodoList(models.Model):
    _name = 'todo.list'
    _description = 'Todo List'

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

    all_tasks_done = fields.Boolean(compute='_compute_all_tasks_done', string="All Tasks Done?", store=True)

    is_draft = fields.Boolean(compute='_compute_state_flags', string="Is Draft?")
    is_in_progress = fields.Boolean(compute='_compute_state_flags', string="Is In Progress?")
    is_complete = fields.Boolean(compute='_compute_state_flags', string="Is Complete?")
    can_mark_done = fields.Boolean(compute='_compute_can_mark_done', string="Can Mark Done?")

    @api.depends('state')
    def _compute_state_flags(self):
        for record in self:
            record.is_draft = record.state == 'draft'
            record.is_in_progress = record.state == 'in_progress'
            record.is_complete = record.state == 'complete'

    @api.depends('state', 'all_tasks_done')
    def _compute_can_mark_done(self):
        for record in self:
            record.can_mark_done = record.state == 'in_progress' and record.all_tasks_done

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
            raise UserError(_("Todo list is not in draft state or already in progress."))
        return True

    @api.depends('task_ids', 'task_ids.is_complete')
    def _compute_all_tasks_done(self):
        for record in self:
            if not record.task_ids:
                record.all_tasks_done = False # ไม่มี task ให้ถือว่ายังไม่พร้อมกด DONE
            else:
                record.all_tasks_done = all(task.is_complete for task in record.task_ids)

    def action_mark_complete(self):
        self.ensure_one()
        if self.state == 'in_progress' and self.all_tasks_done:
            self.write({'state': 'complete'})
        else:
            if self.state != 'in_progress':
                raise UserError(_("Todo list must be 'In Progress' to be marked as 'Complete'."))
            if not self.all_tasks_done:
                raise UserError(_("Not all tasks are completed yet!"))
        return True

    def write(self, vals):
        for record in self:
            # ป้องกันการแก้ไข field หลักๆ เมื่อ state เป็น 'complete'
            # อนุญาตให้แก้ไข state ได้ (เช่น admin อาจจะ revert กลับ) หรือ field อื่นๆ ที่ไม่กระทบข้อมูลหลัก
            if record.state == 'complete' and any(key in vals for key in ['name', 'tag_ids', 'start_date', 'end_date', 'task_ids', 'attendee_ids']):
                 # ถ้ามีการแก้ไข field อื่นนอกจาก state และมี field ต้องห้าม ให้ error
                allowed_to_change_on_complete = {'state'} # เพิ่ม field อื่นที่อนุญาตให้แก้ตอน complete ได้ที่นี่
                forbidden_changes = set(vals.keys()) - allowed_to_change_on_complete
                if any(key in ['name', 'tag_ids', 'start_date', 'end_date', 'task_ids', 'attendee_ids'] for key in forbidden_changes):
                    raise UserError(_("Cannot modify a completed Todo List data."))
        return super(TodoList, self).write(vals)

    # Optional: Override unlink method
    def unlink(self):
        for record in self:
            if record.state == 'complete':
                raise UserError(_("Cannot delete a completed Todo List."))
        return super(TodoList, self).unlink()
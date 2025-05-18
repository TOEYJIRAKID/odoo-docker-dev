# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

# โมเดลสำหรับรายการ Todo List เพื่อจัดการรายการสิ่งที่ต้องทำพร้อมกับสถานะและงานย่อย
class TodoList(models.Model):
    _name = 'todo.list'
    _description = 'Todo List'
    _order = 'date_start, id'

    # ฟิลด์ข้อมูลของโมเดล
    name = fields.Char(string='Title', required=True)
    tag_ids = fields.Many2many('todo.tag', string='Tags')
    date_start = fields.Datetime(string='Start Date', required=True)
    date_end = fields.Datetime(string='End Date', required=True)
    state = fields.Selection([
        ('draft', 'DRAFT'),              # สถานะร่าง
        ('in_progress', 'IN PROGRESS'),  # สถานะกำลังดำเนินการ
        ('complete', 'COMPLETE')         # สถานะเสร็จสิ้น
    ], string='Status', default='draft')
    
    task_ids = fields.One2many('todo.task', 'todo_list_id', string='Tasks')

    attendee_ids = fields.Many2many(
        'res.users', 
        string='Attendee',
        domain=[('share', '=', False)]   # แสดงรายชื่อเฉพาะ Internal Users
    )
    
    all_tasks_completed = fields.Boolean(compute='_compute_all_tasks_completed', store=True)

    # คำนวณว่างานย่อยทั้งหมดเสร็จสิ้นหรือไม่ จะเป็น True เมื่องานย่อยทั้งหมดมีสถานะ is_done เป็น True
    @api.depends('task_ids', 'task_ids.is_done')
    def _compute_all_tasks_completed(self):
        for record in self:
            if record.task_ids:
                record.all_tasks_completed = all(task.is_done for task in record.task_ids)
            else:
                record.all_tasks_completed = False
    
    # ตรวจสอบว่าวันที่สิ้นสุดต้องมากกว่าวันที่เริ่มต้น ถ้าไม่เป็นไปตามเงื่อนไข จะแสดงข้อความแจ้งเตือน ValidationError
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end and record.date_start >= record.date_end:
                raise ValidationError(_("End date must be greater than start date."))
    
    # เปลี่ยนสถานะเป็น 'in_progress' เรียกใช้เมื่อกดปุ่ม PROGRESS
    def action_start_progress(self):
        self.write({'state': 'in_progress'})
    
    # เปลี่ยนสถานะเป็น 'complete' เรียกใช้เมื่อกดปุ่ม DONE
    def action_mark_done(self):
        self.write({'state': 'complete'})

# โมเดลสำหรับงานย่อยใน Todo List เพื่อจัดการรายละเอียดของงานย่อยแต่ละรายการ
class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Todo Task'
    _order = 'sequence, id'

    # ฟิลด์ข้อมูลของโมเดล
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    is_done = fields.Boolean(string='Is Complete', default=False)
    todo_list_id = fields.Many2one('todo.list', string='Todo List', ondelete='cascade', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    
    # สร้างงานย่อยใหม่และคำนวณสถานะ all_tasks_completed ของ Todo List
    @api.model
    def create(self, vals):
        task = super().create(vals)
        task.todo_list_id._compute_all_tasks_completed()
        return task
    
    # อัปเดตงานย่อยและคำนวณสถานะ all_tasks_completed ของ Todo List เมื่อมีการเปลี่ยนแปลงสถานะ is_done
    def write(self, vals):
        result = super().write(vals)
        if 'is_done' in vals:
            for task in self:
                task.todo_list_id._compute_all_tasks_completed()
        return result
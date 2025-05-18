# -*- coding: utf-8 -*-
from odoo import models, fields

# โมเดลสำหรับแท็กของ Todo List ใช้สำหรับจัดหมวดหมู่รายการใน Todo List
class TodoTag(models.Model):
    _name = 'todo.tag'
    _description = 'Todo Tag'

    name = fields.Char(string='Name', required=True)  # ชื่อแท็ก
    color = fields.Integer(string='Color Index')      # ดัชนีสีของแท็ก
# -*- coding: utf-8 -*-
{
    'name': 'Todo List',
    'version': '1.0',
    'summary': 'Manage your todo lists',
    'category': 'To-Do',
    'author': 'TOEYJIRA',
    'website': 'https://github.com/TOEYJIRAKID/odoo-docker-dev',
    'depends': ['base'],
    'data': [
        'security/todo_security.xml',        # Security Rule
        'security/ir.model.access.csv',      # สิทธิ์การเข้าถึงโมเดล
        'data/todo_tags_data.xml',           # ข้อมูลแท็กเริ่มต้น
        'views/todo_list_views.xml',         # รายการ Todo List
        'views/menu_views.xml',              # เมนูของโมดูล
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
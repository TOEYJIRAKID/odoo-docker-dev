{
    'name': 'Todo List',
    'version': '17.0.1.0',
    'summary': 'A simple application to manage Todo Lists.',
    'category': 'To-Do',
    'author': 'TOEYJIRA',
    'website': '',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/todo_tag_data.xml',
        'views/todo_list_views.xml',
        'views/todo_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
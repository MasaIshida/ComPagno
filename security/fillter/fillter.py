import memory_manager.manager

need_cookie_funcs = [
    'user_home_view',
    'build_task_view',
    'task_about_view'
]

def is_valid_cookie(func_name):

    return func_name in need_cookie_funcs

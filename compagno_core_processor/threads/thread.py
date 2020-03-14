import threading
from app.models import U_TRAN
from django.utils import timezone


class PostLogProcess(threading.Thread):

    def __init__(self, user_id, view_func, cookie, erro_st):
        threading.Thread.__init__(self)
        self.user_id = user_id
        self.view_func = view_func
        self.cookie = cookie
        self.erro_st = erro_st

    def run(self):

        o = U_TRAN.objects.create(
            user_id=self.user_id,
            acc_dt=timezone.now(),
            erro_cd=self.erro_st,
            view_func=self.view_func,
            cookie=self.cookie
        )


class PostCookieProcess(threading.Thread):

    def __init__(self, func, user_id, val):
        threading.Thread.__init__(self)
        self.func = func
        self.user_id = user_id
        self.val = val

    def run(self):
        self.func(self.user_id, self.val)

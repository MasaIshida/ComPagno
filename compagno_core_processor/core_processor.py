
from django.template import loader
from memory_manager.manager import Manager
from .threads.thread import PostLogProcess, PostCookieProcess
from security.fillter import fillter
from .cookie import cookie
from memory_manager.memory import Memory



"""
ComPangoのコアとなる処理
前処理→メイン処理→後処理のプロセスをprocess_viewに記載する
"""


class CoreProcessMiddleware:

    def __init__(self, get_response):
        """
        AP起動時に実行する処理
        利用者操作には影響しない

        :param get_response:
        """

        self.get_response = get_response

        # メモリーマネージャーをインスタンス
        manager = Manager()

        # チーム運用管理情報をメモリーで保持する
        manager.get_u_teams_records()

        manager.get_u_nati_records()


    def __call__(self, request):
        """
        レスポンス確定後の後処理を記述する
            基本的に利用者操作には関係ない処理を行う。
        :param request:
        :return:
        """

        response = self.get_response(request)

        # 取引ログへの追加スレッド

        # ログイン時セッションデータからユーザーIDを取り出す
        if 'user_info' in request.session:

            user_id = request.session['user_info']['user_id']
            val = cookie.create_cookie_value()
            cookie_val = user_id + "," + val

            # クッキー保存
            response.set_cookie(
                key='c_key',
                value=cookie_val,
                max_age=600
            )

            # メモリークッキー更新処理
            thread2 = PostCookieProcess(Manager.set_cookie, user_id, val)
            thread2.start()

        else:
            user_id = "un_known"
            val = "not_cookie"


        # マルチスレッドにて取引ログを記録
        thread1 = PostLogProcess(
            user_id,
            request.META["PATH_INFO"],
            val,
            response.status_code
        )
        thread1.start()


        # メモリー管理情報更新処理

        return response


    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        処理フローの前処理を記述する
            前処理では逸脱した遷移の場合、
            ログインページへ遷移させる処理をさせる
        :param request: ユーザーリクエスト
        :param view_func: 表示対象viewメゾット
        :param view_args:
        :param view_kwargs:
        :return: None または HttpResponse
        """
        if fillter.is_valid_cookie(view_func.__name__):

            if Manager.has_cookie(request):

                return None

            t = loader.get_template('login.html')
            return None

        return None


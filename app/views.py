from django.shortcuts import render, redirect
from .forms import *
from .models import S_USERS
from django.utils import timezone
from memory_manager.manager import Manager
from compagno_core_processor.threads.view_thread import TranslationProcessThread
from api.line_service import line_service
from api.weather_service import weather

# Create your views here.


def login_view(request):
    """
    ログインページを表示するメゾット
    :param request:
    :return:
    """
    return render(request, 'login.html')


def login_or_singin_event(request):
    """
    初回ログインか通常のログインかで表示するページを操作する
    :param request:
    :return: 登録ページまたは、マイページ
    """

    # 入力値をFromオブジェクトへ
    form = SigninAndSignupFrom(request.POST)

    # バリデーションチェック
    if not form.is_valid():
        # バリデーションチェックが異常だった場合
        return redirect('login')

    # ユーザーレコードを取得
    db_object = S_USERS.objects.filter(
        user_id=form.data["user_id"],
        pwd=form.data["pwd"],
        team_cd=form.data["team_cd"]
    )

    # 登録されていない
    if len(db_object) == 0:
        return redirect('login')

    # 初回ログインの場合
    if db_object[0].first_login_dt is None:

        # 初回ログインページにセッションを保持して移動
        request.session['user_info'] = request.POST
        return render(request, 'entry.html')

    # マイページへ
    # パスはエントリーページの為リダイレクトで処理
    return redirect('user_home')


def post_user_input(request):
    """
    登録ページから入力値を受け取った場合のメゾット
    データベースに登録しレダイレクトでマイページへ遷移する
    :param request:
    :return:
    """
    form = EntryFrom(request.POST)

    if not form.is_valid():
        return render(request, 'login_or_singin_event')

    # 更新対象のデータを取得
    db_object = S_USERS.objects.filter(
        user_id=request.session['user_info']['user_id'],
        pwd=request.session['user_info']["pwd"],
        team_cd=request.session['user_info']["team_cd"]
    )[0]

    # データベースオブジェクトに値をセット
    db_object.last_name = form.data['last_name']
    db_object.first_name = form.data['first_name']
    db_object.age = form.data['age']
    db_object.email_ad = form.data['email_ad']
    db_object.nati_cd = form.data['nati_cd']
    db_object.first_login_dt = timezone.now()

    # 更新を実行
    db_object.save()

    return redirect('user_home')


def user_home_view(request):
    """
    ユーザートップページを表示するメゾット
    :param request:
    :return:
    """
    task_list = []

    # ユーザーレコード取得
    user = S_USERS.objects.filter(
        user_id=request.session['user_info']['user_id'],
        team_cd=request.session['user_info']["team_cd"]
    )[0]

    # タスクレコード取得
    tasks = S_TASKS.objects.filter(
        team_cd=request.session['user_info']["team_cd"],
    )

    for task in tasks:

        taskdetail = S_TASKS_DETAILS.objects.filter(
            task_uuid=task.task_uuid,
            nati_cd = user.nati_cd
        )
        task_list.append([
            taskdetail[0].cont_title,
            taskdetail[0].cont_text,
            taskdetail[0].task_uuid
        ])

    # 天気情報取得

    # メモリクラスからチーム運用管理情報を取得
    team_cd = request.session['user_info']["team_cd"]
    u_teams = Manager.get_u_teams(team_cd)
    weather_info = []
    for i, nati_flag in enumerate(u_teams):
        cd = i + 1
        if nati_flag == "1":

            # 国識別ID
            id = Manager.get_nati_cd(str(cd))[2]

            # 天気情報取得
            result = weather.main(id)
            weather_info.append([
                result.get('name'),
                "http://openweathermap.org/img/w/" + result.get('weather')[0].get('icon') + ".png"
            ])

    return render(request, 'mypage.html', context={'task_list': task_list, 'weather_info': weather_info})


def build_task_view(request):
    """
    タスクを作成するページを表示するメゾット
    :param request:
    :return:
    """
    return render(request, 'buildtask.html')


def post_build_task_input(request):
    """
    タスクを作成するページ情報受け取った処理
    :param request:
    :return:
    """
    task_form = TaskFrom(request.POST)
    task_detail_form = TaskDetails(request.POST)

    # バリデェーションが異常な場合
    if not(task_form.is_valid()) and not(task_detail_form.is_valid()):
        return redirect('user_home')

    # メモリクラスからチーム運用管理情報を取得
    team_cd = request.session['user_info']["team_cd"]
    team_info = Manager.get_u_teams(team_cd)

    # ユーザー情報取得
    user_record = S_USERS.objects.filter(
        user_id=request.session['user_info']['user_id'],
        pwd=request.session['user_info']["pwd"],
        team_cd=request.session['user_info']["team_cd"]
    )[0]

    # マルチスレッドにて翻訳を実施
    api_thread = TranslationProcessThread(
        task_form,
        task_detail_form,
        team_info,
        user_record
    )
    api_thread.start()

    return redirect('user_home')


def post_line_message(request):

    token = S_LINE_GR.objects.filter(
        team_cd=request.session['user_info']["team_cd"]
    )[0]
    msg = "\n" +"title: " + request.POST.get("line_title") + "\n" + request.POST.get("line_message")
    print(request.POST.get("line_message"))
    line_service.main(msg, token.line_tk)
    return redirect('user_home')



def task_about_view(request):
    """
    タスク詳細ページを表示するメゾット
    :param request:
    :return:
    """
    pass


def task_refer_view(request):
    """
    タスク検索結果を表示
    :param request:
    :return:
    """
    pass


def team_admin_view(request):
    """
    チーム管理画面を表示するメゾット
    :param request:
    :return:
    """





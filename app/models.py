from django.db import models

import datetime

# Create your models here.

"""
データベース設計を示すファイル
詳しくはテーブル定義書を参照してください。
"""

class S_USERS(models.Model):
    """
    ユーザー情報
    """
    user_id = models.CharField(verbose_name='ユーザー名', max_length=50)
    pwd = models.CharField(verbose_name='パスワード', max_length=120)
    last_name = models.CharField(verbose_name='本名', max_length=20, blank=True, null=True)
    first_name = models.CharField(verbose_name='苗字', max_length=20, blank=True, null=True)
    age = models.PositiveSmallIntegerField(verbose_name="年齢", default=0, blank=True, null=True)
    email_ad = models.CharField(verbose_name='メールアドレス', max_length=50, blank=True, null=True)
    nati_cd = models.CharField(verbose_name='国籍コード', max_length=3, blank=True, null=True)
    team_cd = models.CharField(verbose_name='チームコード', max_length=10)
    first_login_dt = models.DateTimeField(verbose_name='初回ログイン日時', blank=True, null=True)

    def __str__(self):
        return self.user_id


class S_TASKS(models.Model):
    """
    タスク一覧情報
    """
    task_uuid = models.CharField(verbose_name='タスクUUID', max_length=225)
    team_cd = models.CharField(verbose_name='チームコード', max_length=10)
    user_id = models.CharField(verbose_name='登録ユーザー名', max_length=20)
    start_dt = models.DateTimeField(verbose_name='タスク開始日')
    end_dt = models.DateTimeField(verbose_name='タスク終了日')
    priority_st = models.CharField(verbose_name='優先ステータス', max_length=2, default="0")
    record_dt = models.DateTimeField(verbose_name='登録日時')
    periods_st = models.CharField(verbose_name='定期的ステータス', max_length=1, default="0")
    cycle_st = models.CharField(verbose_name='周期ステータス', max_length=1, default="0")
    del_fg = models.CharField(verbose_name='削除フラグ', max_length=1, default="0")

    def __str__(self):
        return self.task_uuid


class S_TASKS_DETAILS(models.Model):
    """
    タスク詳細情報
    """
    task_uuid = models.CharField(verbose_name='タスクUUID', max_length=225)
    nati_cd = models.CharField(verbose_name='国籍コード', max_length=3)
    cont_title = models.CharField(verbose_name='タスク名', max_length=30)
    cont_text = models.TextField(verbose_name='タスク内容', max_length=1000)


class S_TEAMS(models.Model):
    """
    チーム情報
    """
    team_cd = models.CharField(verbose_name='チームコード', max_length=10)
    team_name = models.CharField(verbose_name='チーム名', max_length=15)
    sta_fg = models.CharField(verbose_name='運用状況', max_length=1)
    gmail_ad = models.CharField(verbose_name='メールアドレス', max_length=50)
    set_dt = models.DateTimeField(verbose_name='作成日時')
    start_dt = models.DateTimeField(verbose_name='使用開始可能日時')
    end_dt = models.DateTimeField(verbose_name='使用終了日時')

    def __str__(self):
        return self.team_cd


class S_TEAM_ADMINS(models.Model):
    """
    管理者情報
    """
    team_cd = models.CharField(verbose_name='チームコード', max_length=10)
    user_id = models.CharField(verbose_name='ユーザー名', max_length=50)
    admin_st = models.CharField(verbose_name='管理者ステータス', max_length=1)
    admin_dt = models.DateTimeField(verbose_name='管理者付与日時', auto_now_add=True)


class S_LINE_GR(models.Model):
    """
    LINEグループ設定情報
    """
    team_cd = models.CharField(verbose_name='チームコード', max_length=10)
    gr_name = models.CharField(verbose_name='LINEグループ名', max_length=50)
    line_tk = models.CharField(verbose_name='LINEトークン', max_length=200)
    et_dt = models.DateTimeField(verbose_name='作成日時')


class S_MSG(models.Model):
    """
    LINE送信メッセージ情報
    """
    team_cd = models.CharField(verbose_name='チームコード', max_length=10)
    user_id = models.CharField(verbose_name='ユーザー名', max_length=50)
    nati_cd = models.CharField(verbose_name='国籍コード', max_length=3)
    msg_text = models.TextField(verbose_name='メッセージ内容', max_length=1000)
    et_dt = models.DateTimeField(verbose_name='送信日時')


# これより先は運用情報テーブル

class U_TEAMS(models.Model):
    """
    チーム運用管理情報
    """
    team_cd = models.CharField(verbose_name='チームコード', max_length=10)
    nati_cd1 = models.CharField(verbose_name='国籍コード', max_length=3, blank=True, null=True)
    nati_cd2 = models.CharField(verbose_name='国籍コード', max_length=3, blank=True, null=True)
    nati_cd3 = models.CharField(verbose_name='国籍コード', max_length=3, blank=True, null=True)

    def __str__(self):
        return self.team_cd

class U_TRAN(models.Model):
    """
    取引ログ情報
    """
    user_id = models.CharField(verbose_name='ユーザー名', max_length=50)
    acc_dt = models.DateTimeField(verbose_name='アクセス日時')
    erro_cd = models.CharField(verbose_name='エラーコード', max_length=3)
    view_func = models.CharField(verbose_name='view_func', max_length=100)
    cookie = models.CharField(verbose_name='クッキー値', max_length=50)

    def __str__(self):
        return self.erro_cd

class U_NATI(models.Model):
    """
    国マスター情報
    """
    nati_name = models.CharField(verbose_name='国名', max_length=10)
    nati_cd = models.CharField(verbose_name='国コード', max_length=5)
    wheather_id = models.CharField(verbose_name='天気取得クエリ', max_length=15)

    def __str__(self):
        return self.nati_name


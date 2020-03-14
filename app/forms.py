from django import forms
from django.forms import ModelForm

from .models import S_USERS, S_TASKS, S_TASKS_DETAILS, S_LINE_GR, S_MSG, U_NATI

"""
DjangoのModelFormを使用する。
バリデーション機能が備わっている為、
セキュリティレベルを向上する。
"""


class SigninAndSignupFrom(ModelForm):
    """
    サインイン・サインアップページのフォームクラス
    ユーザー名とパスワード、チームコードを取得する
    """
    class Meta:
        model = S_USERS
        fields = {"user_id", "pwd", "team_cd"}


class EntryFrom(ModelForm):

    class Meta:
        model = S_USERS
        fields = {"last_name", "first_name", "age", "email_ad", "nati_cd"}


class TaskFrom(ModelForm):

    class Meta:
        model = S_TASKS
        fields = {"priority_st"}


class TaskDetails(ModelForm):

    class Meta:
        model = S_TASKS_DETAILS
        fields = {"cont_title", "cont_text"}



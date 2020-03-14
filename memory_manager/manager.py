from app.models import U_TEAMS, U_NATI
from .memory import Memory

class Manager:

    @staticmethod
    def clear_memory():

        for key in Memory.__dict__:

            if not key.startswith('__'):

                Memory.__dict__[key].clear()


    @staticmethod
    def has_cookie(request):

        if request.COOKIES.get('c_key') is None:
            return False

        try:
            cookie_list = request.COOKIES.get('c_key').split(",")

            return Memory.cookies[cookie_list[0]] == cookie_list[1]

        except KeyError:

            return False

    @staticmethod
    def get_cookie(key):
        return Memory.cookies.get(key)

    @staticmethod
    def set_cookie(user_id, val):
        Memory.cookies[user_id] = val

    @staticmethod
    def get_u_teams(team_cd):
        return Memory.u_t.get(team_cd)

    @staticmethod
    def get_nati_cd(key):
        print(Memory.m_na, key)
        return Memory.m_na.get(key)


    def get_u_teams_records(self):
        """
        チーム運用管理情報を取得する
        """

        records = list(U_TEAMS.objects.all())

        for record in records:
            Memory.u_t[record.team_cd] = [
                record.nati_cd1,
                record.nati_cd2,
                record.nati_cd3
            ]

    @staticmethod
    def update_u_teams_records(self, team_cd, i, val):
        """
        チーム運用管理情報の値の更新
        :param team_cd: チームコード
        :param i: リストインデックス
        :param val: 設定値(0, 1)
        """
        Memory.u_t[team_cd][i] = val


    def get_u_nati_records(self):
        """
        国マスター情報を取得する
        """
        records = list(U_NATI.objects.all())
        for record in records:
            Memory.m_na[str(record.pk)] = [
                record.nati_name,
                record.nati_cd,
                record.wheather_id
            ]

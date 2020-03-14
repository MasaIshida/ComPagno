import threading
from app.forms import S_TASKS, S_TASKS_DETAILS
from api.translation_service import translation
from memory_manager.manager import Manager
from django.utils import timezone
from ..utility import uni_uni_ide


class TranslationProcessThread(threading.Thread):

    def __init__(self, task_form, task_detail_form, team_info, user_record):
        threading.Thread.__init__(self)
        self.task_form = task_form
        self.task_detail_form = task_detail_form
        self.team_info = team_info
        self.user_record = user_record

    def run(self):

        # uuidを生成する
        uuid = uni_uni_ide.create_uuid()

        # 運用情報の値の数だけループする
        for i, nati_flag in enumerate(self.team_info):
            cd = i + 1
            # 翻訳するかの判定
            if nati_flag == "1" and not (self.user_record.nati_cd == str(cd)):

                # タスク名
                tra_title = translation.main(
                    self.task_detail_form.data['cont_title'],
                    Manager.get_nati_cd(str(self.user_record.nati_cd))[1],
                    Manager.get_nati_cd(str(cd))[1]
                )

                # タスク内容
                tra_text = translation.main(
                    self.task_detail_form.data['cont_text'],
                    Manager.get_nati_cd(str(self.user_record.nati_cd))[1],
                    Manager.get_nati_cd(str(cd))[1]
                )

                if tra_text is not None:
                    insert = S_TASKS_DETAILS(
                        task_uuid=uuid,
                        nati_cd=cd,
                        cont_title=tra_title,
                        cont_text=tra_text
                    )
                else:
                    insert = S_TASKS_DETAILS(
                        task_uuid=uuid,
                        nati_cd=cd,
                        cont_title=self.task_form.data["cont_title"],
                        cont_text=self.task_detail_form.data['cont_text']
                    )
                insert.save()
            else:
                # 登録ユーザーの母国語の情報を挿入
                insert = S_TASKS_DETAILS(
                    task_uuid=uuid,
                    nati_cd=cd,
                    cont_title=self.task_form.data["cont_title"],
                    cont_text=self.task_detail_form.data['cont_text']
                )
                insert.save()
        insert = S_TASKS(
            task_uuid=uuid,
            team_cd=self.user_record.team_cd,
            user_id=self.user_record.user_id,
            start_dt=timezone.now(),
            end_dt=timezone.now(),
            priority_st=self.task_form.data["priority_st"],
            record_dt=timezone.now(),
            periods_st="0",
            cycle_st="0",
            del_fg="0"
        )
        insert.save()
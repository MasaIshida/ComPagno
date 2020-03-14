# 初めかた

## インストールモジュール
- pip
- Django
- requests

## 実装コマンド
ComPagno内のmanage.pyがあるディレクトリまで移動する
manage.pyが存在するディレクトリで下記コマンドを実行する


### 1.migrationの作成
```bat
python manage.py makemigrations app
```
migrationsファイルが作成される
ここにはこれまでのデータベースの設定変更の履歴など
が残りもし設定を戻す事がある場合はここのファイルを参照する事で
戻す事が可能となる

### 2.データベースの作成
```bat
python manage.py migrate
```
sqlite3のデータベースが作成される

### 3.管理者ユーザーの作成
```bat
python manage.py createsuperuser
```
データベースの管理者の作成を行う

### 4.サーバー起動
```bat
python manage.py runserver --noreload
```
全てのコマンド実行後にサーバーを起動する
"--noreload"オプションはサーバーロードを防ぐ為にある
無くても良い。

### 備考
```bat
python manage.py loaddata master_data/post_initial.json
```
始めるにあたりマスターデータがないと一部の業務で操作が行えない為
上記コマンドと同じディレクトーにてコマンドを打つとマスターデータが挿入される。




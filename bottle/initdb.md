# PostgreSQLのインストールと起動
```
# yum install postgresql-server
# postgresql-setup initdb
# systemctl start postgresql
```
# PostgreSQLの設定
/var/lib/pgsql/data/pg_hba.conf
```
host    all             all             127.0.0.1/32            md5
```

# ユーザ作成
```
CREATE ROLE one_night_zinrou WITH LOGIN PASSWORD 'one_night_zinrou';
```

# データベース作成
```
CREATE DATABASE one_night_zinrou OWNER one_night_zinrou;
```

# テーブル作成
```
$ python initdb.py
```

from bottle import route, run, template, get, post, put, delete, request, view, HTTPResponse, static_file, url
import json
import requests
import psycopg2.extras
import random
import hashlib

village = {}

#### views ####

# トップページ
@route('/')
def index():
    return template('index')

# 村参加ページ
@route('/participate/')
def participate():
    return template('participate', url=url)

# 村作成ページ
@route('/create/')
def create():
    return template('create', url=url)

# 村のトップページ
@route('/<village_name:re:[0-9A-Za-z]*>/')
def village_index(village_name):
    flag = is_village(village_name)
    if flag is True:
        return template('village_index', url=url, village_name=village_name)

    r = HTTPResponse(status=404)
    return r

# ログインページ
@route('/<village_name:re:[0-9A-Za-z]*>/login/')
def login(village_name):
    flag = is_village(village_name)
    if flag is True:
        return template('login', url=url, village_name=village_name)

    r = HTTPResponse(status=404)
    return r

# 新規登録ページ
@route('/<village_name:re:[0-9A-Za-z]*>/join/')
def join(village_name):
    flag = is_village(village_name)
    if flag is True:
        return template('join', url=url, village_name=village_name)

    r = HTTPResponse(status=404)
    return r

# 村の部屋ページ
@route('/<village_name:re:[0-9A-Za-z]*>/room/')
def room(village_name):
    flag = is_village(village_name)
    if flag is True:
        session_id = request.get_cookie('session_id')

        result = auth(village_name, session_id)

        player_name = result['player_name']
        new_session_id = result['new_session_id']

        if player_name != '':
            return template('room', url=url, player_name=player_name, village_name=village_name, session_id=new_session_id)
        else:
            return template('session_error')

    r = HTTPResponse(status=404)
    return r

# 村の待機ページ
@route('/<village_name:re:[0-9A-Za-z]*>/waiting/')
def waiting(village_name):
    session_id = request.get_cookie('session_id')
    result = auth(village_name, session_id)
    player_name = result['player_name']
    new_session_id = result['new_session_id']
    if player_name != '':
        return template('waiting', url=url, player_name=player_name, village_name=village_name, session_id=new_session_id)
    else:
        return template('session_error')

# 村の行動ページ
@route('/<village_name:re:[0-9A-Za-z]*>/action/')
def action(village_name):
    session_id = request.get_cookie('session_id')
    result = auth(village_name, session_id)
    player_name = result['player_name']
    new_session_id = result['new_session_id']
    if player_name != '':
        return template('action', url=url, player_name=player_name, village_name=village_name, session_id=new_session_id)
    else:
        return template('session_error')

# 村の通知ページ
@route('/<village_name:re:[0-9A-Za-z]*>/notification/')
def notification(village_name):
    session_id = request.get_cookie('session_id')
    result = auth(village_name, session_id)
    player_name = result['player_name']
    new_session_id = result['new_session_id']
    if player_name != '':
        return template('notification', url=url, player_name=player_name, village_name=village_name, session_id=new_session_id)
    else:
        return template('session_error')

# 村の個人ページ
@route('/<village_name:re:[0-9A-Za-z]*>/player/<player_name:re:[0-9A-Za-z]*>/')
@view('player')
def player(village_name, player_name):
    return dict(url=url, village_name=village_name, player_name=player_name)

#### /views ####

#### API ####
@get('/api/')
def get_api():
    global village
    village_names = []
    for key in village.keys():
        village_names.append(key)
    body = json.dumps(village_names)
    r = HTTPResponse(status=200, body=body)
    r.set_header('Content-Type', 'application/json')
    return r

@post('/api/')
def post_api():
    print('ENTER: post_api')
    global village
    print(request.json)
    village_name = request.json.get("village_name")
    password = request.json.get("password")
    data = {'village_name': village_name}

    flag = is_village(village_name)
    if flag is False:
        conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=one_night_zinrou user=one_night_zinrou password=one_night_zinrou")
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute("insert into village (name, password) values (%s, %s)", (village_name, password))
        conn.commit()
        dict_cur.close()
        conn.close()
        status = 200
    else:
        status = 409

    body = json.dumps(data)
    r = HTTPResponse(status=status, body=body)
    r.set_header('Content-Type', 'application/json')
    return r

@post('/api/participate/')
def post_api_participate():
    print('ENTER: post_api_participate')
    global village
    print(request.json)
    village_name = request.json.get("village_name")
    data = {'village_name': village_name}

    flag = is_village(village_name)
    if flag is True:
        status = 200
    else:
        status = 404

    body = json.dumps(data)
    r = HTTPResponse(status=status, body=body)
    r.set_header('Content-Type', 'application/json')
    return r

@get('/api/<village_name:re:[0-9A-Za-z]*>/')
def get_village(village_name):
    flag = is_village(village_name)
    data = {'village_name': village_name}
    if flag is True:
        status = 200
    else:
        status = 404

    body = json.dumps(data)
    r = HTTPResponse(status=status, body=body)
    r.set_header('Content-Type', 'application/json')
    return r

@post('/api/<village_name:re:[0-9A-Za-z]*>/')
def post_village(village_name):
    print(request.json)
    player_name = str(request.json.get("player_name"))
    password = str(request.json.get("password"))
    village_password = str(request.json.get("village_password"))
    data = {'village_name': village_name, 'player_name': player_name}
    flag = is_village(village_name)
    if flag is True:
        village_password_flag = check_village_password(village_name, village_password)
        if village_password_flag is True:
            player_flag = is_player(village_name, player_name)
            if player_flag is False:
                session_id = str(random.random())
                next_session_id = hashlib.sha256(str(session_id + password).encode('utf-8')).hexdigest()
                conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=one_night_zinrou user=one_night_zinrou password=one_night_zinrou")
                dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                dict_cur.execute("select id from village where (name)=(%s)", (village_name,))
                village_id = ''
                for row in dict_cur:
                    village_id = str(row['id'])
                if village_id != '':
                    dict_cur.execute("insert into player (name, password, village_id, session_id) values (%s, %s, %s, %s)", (player_name, password, village_id, next_session_id))
                    conn.commit()
                dict_cur.close()
                conn.close()
                data['session_id'] = session_id
                status = 200
            else:
                status = 409
        else:
            status = 403
    else:
        status = 404

    body = json.dumps(data)
    r = HTTPResponse(status=status, body=body)
    r.set_header('Content-Type', 'application/json')
    return r

@delete('/api/<village_name:re:[0-9A-Za-z]*>/<player_name:re:[0-9A-Za-z]*>/')
def delete_logout(village_name, player_name):
    flag = is_village(village_name)
    if flag is True:
        player_flag = is_player(village_name, player_name)
        if player_flag is True:
            conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=one_night_zinrou user=one_night_zinrou password=one_night_zinrou")
            dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            dict_cur.execute("delete from player where (name)=(%s)", (player_name,))
            conn.commit()
            dict_cur.execute("select player.name from player, village where player.village_id = village.id and (village.name)=(%s)", (village_name,))
            i = 0
            for row in dict_cur:
                i += 1
            if i == 0:
                # プレイヤーが皆ログアウトしたら村を消す
                dict_cur.execute("delete from village where (name)=(%s)", (village_name,))
                conn.commit()
            dict_cur.close()
            conn.close()
            status = 200
        else:
            status = 404
    else:
        status = 404

    r = HTTPResponse(status=status)
    r.set_header('Content-Type', 'application/json')
    return r

@post('/api/<village_name:re:[0-9A-Za-z]*>/login/')
def post_login(village_name):
    player_name = str(request.json.get("player_name"))
    password = str(request.json.get("password"))
    village_password = str(request.json.get("village_password"))
    data = {'village_name': village_name, 'player_name': player_name}
    flag = is_village(village_name)
    if flag is True:
        village_password_flag = check_village_password(village_name, village_password)
        if village_password_flag is True:
            player_flag = is_player(village_name, player_name)
            if player_flag is True:
                password_flag = check_player_password(village_name, player_name, password)
                if password_flag is True:
                    session_id = str(random.random())
                    next_session_id = hashlib.sha256(str(session_id + password).encode('utf-8')).hexdigest()
                    conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=one_night_zinrou user=one_night_zinrou password=one_night_zinrou")
                    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                    dict_cur.execute("select id from village where (name)=(%s)", (village_name,))
                    village_id = ''
                    for row in dict_cur:
                        village_id = str(row['id'])
                    if village_id != '':
                        dict_cur.execute("update player set (session_id)=(%s) where (name)=(%s) and (village_id)=(%s)", (next_session_id, player_name, village_id))
                        conn.commit()
                    dict_cur.close()
                    conn.close()
                    data['session_id'] = session_id
                    status = 200
                else:
                    status = 403
            else:
                status = 400
        else:
            status = 403
    else:
        status = 404

    body = json.dumps(data)
    r = HTTPResponse(status=status, body=body)
    r.set_header('Content-Type', 'application/json')
    return r

#### /API ####

@route('/static/<filepath:path>', name='static_file')
def static(filepath):
    return static_file(filepath, root="./static")

def is_village(village_name):
    conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=one_night_zinrou user=one_night_zinrou password=one_night_zinrou")
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute("select name from village")
    flag = False
    for row in dict_cur:
        if row['name'] == village_name:
            flag = True
            break
    dict_cur.close()
    conn.close()

    return flag

def check_village_password(village_name, password):
    conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=one_night_zinrou user=one_night_zinrou password=one_night_zinrou")
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute("select password from village where (name)=(%s)", (village_name,))
    flag = False
    for row in dict_cur:
        if row['password'] == password:
            flag = True
            break
    dict_cur.close()
    conn.close()

    return flag

def is_player(village_name, player_name):
    conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=one_night_zinrou user=one_night_zinrou password=one_night_zinrou")
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute("select player.name from player, village where player.village_id = village.id and (village.name)=(%s)", (village_name,))
    flag = False
    for row in dict_cur:
        if row['name'] == player_name:
            flag = True
            break
    dict_cur.close()
    conn.close()

    return flag

def check_player_password(village_name, player_name, password):
    conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=one_night_zinrou user=one_night_zinrou password=one_night_zinrou")
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute("select player.password from player, village where player.village_id = village.id and (village.name)=(%s) and (player.name)=(%s)", (village_name, player_name))
    flag = False
    for row in dict_cur:
        if row['password'] == password:
            flag = True
            break
    dict_cur.close()
    conn.close()

    return flag

def auth(village_name, session_id):
    conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=one_night_zinrou user=one_night_zinrou password=one_night_zinrou")
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute("select player.name, player.password from player, village where player.village_id = village.id and (village.name)=(%s) and (session_id)=(%s)", (village_name, session_id, ))
    player_name = ''
    password = ''
    for row in dict_cur:
        player_name = str(row['name'])
        password = str(row['password'])
    new_session_id = ''
    if player_name != '':
        new_session_id = str(random.random())
        new_next_session_id = hashlib.sha256(str(new_session_id + password).encode('utf-8')).hexdigest()
        dict_cur.execute("select id from village where (name)=(%s)", (village_name,))
        village_id = ''
        for row in dict_cur:
            village_id = str(row['id'])
        if village_id != '':
            dict_cur.execute("update player set (session_id)=(%s) where (name)=(%s) and (village_id)=(%s)", (new_next_session_id, player_name, village_id))
            conn.commit()
    dict_cur.close()
    conn.close()

    return {'player_name': player_name, 'new_session_id': new_session_id}

# ビルトインの開発用サーバーの起動
# ここでは、debugとreloaderを有効にしている
if __name__ == '__main__':
    #run(host='192.168.33.254', port=8080, debug=True, reloader=True)
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)
else:
    application = default_app()

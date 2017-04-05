from bottle import route, run, template, get, post, put, delete, request, view, HTTPResponse, static_file, url
import json
import requests

village = {}

#### views ####

# トップページ
@route('/')
@view('index')
def index():
    return dict()

# 村参加ページ
@route('/participate/')
@view('participate')
def participate():
    return dict(url=url)

# 村作成ページ
@route('/create/')
@view('create')
def create():
    return dict(url=url)

# 村のトップページ
@route('/<village_name:re:[0-9A-Za-z]*>/')
@view('village_index')
def village_index(village_name):
    return dict(url=url, village_name=village_name)

# ログインページ
@route('/<village_name:re:[0-9A-Za-z]*>/login/')
@view('login')
def login(village_name):
    return dict(url=url, village_name=village_name)
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
    body = json.dumps({'village_name': village_name, 'session_id': 1})

    flag = is_village(village_name)
    if flag is False:
        village[village_name] = {'password': password, 'player': {}}
        r = HTTPResponse(status=200, body=body)
    else:
        r = HTTPResponse(status=400, body=body)

    r.set_header('Content-Type', 'application/json')
    return r

@post('/api/participate/')
def post_api_participate():
    print('ENTER: post_api_participate')
    global village
    print(request.json)
    village_name = request.json.get("village_name")
    password = request.json.get("password")
    body = json.dumps({'village_name': village_name, 'session_id': 2})

    flag = is_village(village_name)
    if flag is True:
        password_flag = check_village_password(village_name, password)
        if password_flag is True:
            r = HTTPResponse(status=200, body=body)
        else:
            r = HTTPResponse(status=403, body=body)
    else:
        r = HTTPResponse(status=404, body=body)

    r.set_header('Content-Type', 'application/json')
    return r

@get('/api/<village_name:re:[0-9A-Za-z]*>/')
def get_village(village_name):
    flag = is_village(village_name)
    data = {'village_name': village_name}
    body = json.dumps(data)
    if flag is True:
        r = HTTPResponse(status=200, body=body)
    else:
        r = HTTPResponse(status=404, body=body)

    r.set_header('Content-Type', 'application/json')
    return r

@post('/api/<village_name:re:[0-9A-Za-z]*>/player/')
def post_player(village_name):
    global village
    print(request.json)
    name = request.json.get("name")
    password = request.json.get("password")
    data = {'village_name': village_name, 'name': name}
    body = json.dumps(data)
    flag = is_village(village_name)
    if flag is True:
        player = {}
        player[name] = {'password': password}
        village[village_name]['player'].update(player)
        print(village)
        r = HTTPResponse(status=200, body=body)
    else:
        r = HTTPResponse(status=404, body=body)

    r.set_header('Content-Type', 'application/json')
    return r

#### /API ####

@route('/static/<filepath:path>', name='static_file')
def static(filepath):
    return static_file(filepath, root="./static")

def is_village(village_name):
    global village
    flag = False
    if village_name in village:
        flag = True
    return flag

def check_village_password(village_name, password):
    global village
    flag = is_village(village_name)
    if flag is True:
        if village[village_name]['password'] == password:
            return True
    return False

# ビルトインの開発用サーバーの起動
# ここでは、debugとreloaderを有効にしている
if __name__ == '__main__':
    #run(host='192.168.33.254', port=8080, debug=True, reloader=True)
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)
else:
    application = default_app()

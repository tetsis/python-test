from bottle import route, run, template, get, post, put, delete, request, view, HTTPResponse, static_file, url
import json

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
def village_index():
    global village

    # 有効な村名かチェック
    flag = False
    for key in village.keys():
        if village_name == key:
            flag = True

    if flag == True:
        r = HTTPResponse(status=200)
    else:
        r = HTTPResponse(status=404)
    return r

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
    global village
    village_name = request.json.get("village_name")
    password = request.json.get("password")
    village[village_name] = password
    body = json.dumps({'village_name': village_name})
    r = HTTPResponse(status=200, body=body)
    r.set_header('Content-Type', 'application/json')
    return r

@get('/api/<village_name:re:[0-9A-Za-z]*>/')
def get_village(village_name):
    global village
    if village_name in village:
        data = {'village_name': village_name}
        body = json.dumps(data)
        r = HTTPResponse(status=200, body=body)
        r.set_header('Content-Type', 'application/json')
    else:
        r = HTTPResponse(status=404)
    return r

#### /API ####

@route('/static/<filepath:path>', name='static_file')
def static(filepath):
    return static_file(filepath, root="./static")

#### 以下サンプル ####
# routeデコレーター
# これを使用してURLのPathと関数をマッピングする。
@route('/hello')
def hello():
    return "Hello World!"

# http://localhost:8080/hello/name
@route('/hello/<name>')
def hello_name(name):
    return template('Hello {{name}}', name=name)

# http://localhost:8080/tags/python
@route('/tags/<tag_name:re:[a-z]+>')
def tags(tag_name):
    return template('tag_name={{tag_name}}', tag_name=tag_name)

# @route('/resource')と同じ意味
@get('/resource')
def get_resource():
    # 何か処理をする
    return ""

# @route('/resource', method='POST')と同じ意味
@post('/resource')
def post_resource():
    #username = request.forms.get('username')
    username = request.json.get("username")
    return template('username={{username}}', username=username)

# @route('/resource', method='PUT')と同じ意味
@put('/resource')
def put_resource():
    # 何か処理をする
    return ""

# @route('/resource', method='DELETE')と同じ意味
@delete('/resource')
def delete_resource():
    # 何か処理をする
    return ""

# ビルトインの開発用サーバーの起動
# ここでは、debugとreloaderを有効にしている
run(host='localhost', port=8080, debug=True, reloader=True)

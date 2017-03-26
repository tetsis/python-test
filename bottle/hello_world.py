from bottle import route, run, template, get, post, put, delete, request

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

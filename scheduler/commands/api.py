# https://bottlepy.org/docs/dev/
from bottle import route, run, template

@route('/test/<name>')
def test(name):
    return template('{{name}}', name=name)

def api_command(args):

    print("API WIP...")
    run(host='localhost', port=8080)
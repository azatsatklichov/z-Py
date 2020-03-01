'''
CSRF Protection
Posted by Dan Jacob on 2010-05-03 @ 11:29 and filed in Security

A common technique against CSRF attacks is to add a random string to the session, and check that string against a hidden field in the POST.
'''

from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import CSRFError

#http://flask.pocoo.org/snippets/3/
#http://flask-wtf.readthedocs.io/en/stable/csrf.html
@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = some_random_string()
    return session['_csrf_token']

    app.jinja_env.globals['csrf_token'] = generate_csrf_token  

#And then in your template:

<form method=post action="">
    <input name=_csrf_token type=hidden value="{{ form.srf_token() }}">
</form>
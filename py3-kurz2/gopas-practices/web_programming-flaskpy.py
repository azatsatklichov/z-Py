
#documentation
'''
Flask
• Web microframework
• routing, debugging, and Web Server Gateway Interface (WSGI)
subsystems
• template support is provided by Jinja2
• User authentication, formvalidations are available throught
extensions
	• Instalation: pip install flask
'''

print(" -- Python Web Frameworks ")
#https://wiki.python.org/moin/WebFrameworks
#https://pythonhosted.org/Flask-Security/
#https://damyanon.net/post/flask-series-security/
#http://flask.pocoo.org/snippets/3/
print("Debugger ")
#https://spapas.github.io/2016/06/07/django-werkzeug-debugger/
#https://codeseekah.com/2012/10/28/dubugging-flask-applications-under-uwsgi/
#import flask 
from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
	#a+=1
	return '<h1 style="background-color: orange">Hello World!</h1>'

if __name__ == "__main__":
	app.run(debug=True) #host=‚0.0.0.0‘, port=8080


from flask import Flask,render_template
from flask import request
app = Flask('myapp')

@app.route('/')
def index():
  user_agent = request.headers.get("User-Agent")

  return '<h1>Hello World!</h1><br><p>Your browser is %s</p>' % user_agent
@app.route('/user/<name>')
def user(name):
  return render_template('user.html', name=name)
if __name__ == "__main__":
  app.run(debug=True,host="0.0.0.0", port=8080)

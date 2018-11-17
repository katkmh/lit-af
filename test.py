from flask import render_template
from flask import Flask
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Katrina'}
    return render_template('test.html', title='Home', user=user)
    # stream regular by nct

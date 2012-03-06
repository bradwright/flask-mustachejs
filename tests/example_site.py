from flask import Flask, render_template

from flask.ext.mustache import FlaskMustache

app = Flask(__name__)
app = FlaskMustache.attach(app)

@app.route('/')
def index():
    return render_template('index.jinja')

if __name__ == '__main__':
    app.run(debug=True)

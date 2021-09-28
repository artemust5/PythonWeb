from flask import Flask

app = Flask(__name__)


@app.route('/api/v1/hello-world-28')
def index():
    """Index page route"""

    return '<h1>Hello World, Art Ust, 28 var</h1>'

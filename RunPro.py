from application import app

from waitress import serve

# serve(app)
serve(app, port=9785)

# http://localhost:9785/api/v1/hello-world-28

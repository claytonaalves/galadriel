from app.app import create_app
from config import BaseConfig

app = create_app(BaseConfig)

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=5000)

    from gevent.wsgi import WSGIServer
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()

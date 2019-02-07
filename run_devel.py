from app.app import create_app
from config import BaseConfig

from gevent.pywsgi import WSGIServer
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication

app = create_app(BaseConfig)

@run_with_reloader
def run_server():
    http_server = WSGIServer(('0.0.0.0', 5000), DebuggedApplication(app))
    http_server.serve_forever()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    run_server()

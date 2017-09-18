from app.app import create_app
from config import BaseConfig

app = create_app(BaseConfig)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

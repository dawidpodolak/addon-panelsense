from flask import Flask
from loging.logger import _LOGGER

app = Flask(__name__)


def start_web_app():
    _LOGGER.info("Start web app")
    app.run(debug=True, host="0.0.0.0", port=5000)


@app.route("/")
def dashboard():
    return "Hello, World! fsadfdsd"

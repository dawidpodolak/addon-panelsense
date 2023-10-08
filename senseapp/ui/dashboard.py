from flask import Flask, render_template, request
from loging.logger import _LOGGER
from flask_babel import Babel
from typing import Callable, Set
from server.sense_server import PanelSenseServer
from server.client.sense_client import SenseClient, SenseClienDetails
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)

app.config["LANGUAGES"] = {"en": "English", "pl": "Polski"}
sense_server_callback: Callable[[], PanelSenseServer]


def start_web_app(server_callback: Callable[[], PanelSenseServer]):
    global sense_server_callback
    _LOGGER.info("Start web app")
    sense_server_callback = server_callback
    server_callback().client_connected_callbacks.add(on_client_connected)
    server_callback().client_diconnected_callbacks.add(on_client_disconnected)
    app.run(debug=True, host="0.0.0.0", port=5000)


def on_client_connected(senseClient: SenseClient):
    with app.app_context():
        turbo.push(
            turbo.replace(
                render_template("index.html", clients=get_connected_clients()),
                "devide_list",
            )
        )


def on_client_disconnected(senseClient: SenseClient):
    with app.app_context():
        turbo.push(
            turbo.replace(
                render_template("index.html", clients=get_connected_clients()),
                "devide_list",
            )
        )


@app.route("/")
def dashboard():
    return render_template("index.html", clients=get_connected_clients())


def get_connected_clients():
    global sense_server_callback

    clientSet: Set[SenseClienDetails] = set()

    for client in sense_server_callback().connected_clients:
        clientSet.add(client.details)
    return [client.model_dump() for client in clientSet]

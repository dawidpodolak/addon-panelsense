from typing import Callable, Optional, Set

from flask import Flask, render_template, request
from flask_babel import Babel
from loging.logger import _LOGGER
from server.client.sense_client import SenseClienDetails, SenseClient
from server.client_connection_helper import ClientConectionHelper
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)

app.config["LANGUAGES"] = {"en": "English", "pl": "Polski"}
sense_server_callback: Callable[[], ClientConectionHelper]


def start_web_app(isDebug: bool, server_callback: Callable[[], ClientConectionHelper]):
    global sense_server_callback
    _LOGGER.info(f"Start web app. UI debug is on: {isDebug}")
    sense_server_callback = server_callback
    server_callback().client_connected_callbacks.add(on_client_connected)
    server_callback().client_diconnected_callbacks.add(on_client_disconnected)
    app.run(debug=isDebug, host="0.0.0.0", port=5000)


def on_client_connected(senseClient: SenseClient):
    with app.app_context():
        turbo.push(
            turbo.replace(
                get_index_renderer(),
                "devide_list",
            )
        )


def on_client_disconnected(senseClient: SenseClient):
    with app.app_context():
        turbo.push(
            turbo.replace(
                get_index_renderer(),
                "devide_list",
            )
        )


@app.route("/")
def dashboard():
    return get_index_renderer()


# <!-- <div class="device-item" onclick="location.href= '{{ url_for('device_page', installation_id=client['installation_id']) }}'"> -->
@app.route("/device/<installation_id>")
def device_page(installation_id):
    client = get_sense_client(installation_id)
    if client == None:
        raise

    return render_template(
        "device.html",
        show_top_bar=True,
        title=client.details.name,
        device=client.details,
    )


def get_index_renderer():
    with app.app_context():
        return render_template(
            "index.html", title="PanelSense devices", clients=get_connected_clients()
        )


def get_sense_client(installation_id: str) -> Optional[SenseClient]:
    global sense_server_callback
    for client in sense_server_callback().connected_clients:
        if client.details.installation_id == installation_id:
            return client
    return None


def get_connected_clients():
    global sense_server_callback

    clientSet: Set[SenseClienDetails] = set()

    for client in sense_server_callback().connected_clients:
        clientSet.add(client.details)
    return [client.model_dump() for client in clientSet]

from typing import Callable, List, Optional, Set

from flask import Flask, jsonify, render_template, request
from flask_babel import Babel
from loging.logger import _LOGGER
from pydantic import BaseModel
from server.client.sense_client import SenseClienDetails, SenseClient
from server.client_connection_helper import ClientConectionHelper
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)

app.config["LANGUAGES"] = {"en": "English", "pl": "Polski"}
sense_server_callback: Callable[[], ClientConectionHelper]
update_sense_client_config_callback: Callable[[str], None]
current_user_page: str = "/"


class UiClient(BaseModel):
    is_online: bool
    installation_id: str
    name: str
    version_name: str
    version_code: int


def start_web_app(isDebug: bool):
    _LOGGER.info(f"Start web app. UI debug is on: {isDebug}")

    app.run(debug=isDebug, host="0.0.0.0", port=5000)


def set_client_callback(server_callback: Callable[[], ClientConectionHelper]):
    global sense_server_callback
    sense_server_callback = server_callback
    server_callback().client_connected_callbacks.add(on_client_connected)
    server_callback().client_diconnected_callbacks.add(on_client_disconnected)


def on_client_connected(senseClient: SenseClient):
    if current_user_page == "/":
        update_index()
    elif "device" in current_user_page:
        update_device(senseClient.details.installation_id)


def on_client_disconnected(senseClient: SenseClient):
    if current_user_page == "/":
        update_index()
    elif "device" in current_user_page:
        update_device(senseClient.details.installation_id)


def update_index():
    with app.app_context():
        turbo.push(
            turbo.replace(
                get_index_renderer(),
                "device_list",
            )
        )


def update_device(installation_id: str):
    _LOGGER.info(f"Update device: {installation_id}")
    with app.app_context():
        turbo.push(
            turbo.replace(
                get_device_renderer(installation_id),
                "device_status",
            )
        )


@app.route("/")
def dashboard():
    return get_index_renderer()


@app.route("/device/<installation_id>")
def device_page(installation_id):
    return get_device_renderer(installation_id)


@app.route("/update_configuration", methods=["POST"])
def receive_text():
    data = request.get_json()
    configuration = data.get("configuration", "")
    installation_id = data.get("installation_id", "")

    _LOGGER.debug(f"Text from page: {sense_server_callback()}")
    sense_server_callback().update_sense_client_config(installation_id, configuration)
    return jsonify({"status": "success"}), 200


@app.route("/user_current_page", methods=["POST"])
def user_current_page():
    global current_user_page
    data = request.get_json()
    current_user_page = data.get("current_page")
    _LOGGER.info(f"Current user page: {current_user_page}")
    return jsonify({"status": "success"}), 200


def get_index_renderer():
    with app.app_context():
        return render_template(
            "index.html", title="PanelSense devices", clients=get_connected_clients()
        )


def get_device_renderer(installation_id: str):
    client = get_sense_client(installation_id)
    if client == None:
        raise
    ui_client = UiClient(
        is_online=client.is_online,
        installation_id=client.details.installation_id,
        name=client.details.name,
        version_name=client.details.version_name,
        version_code=client.details.version_code,
    )
    with app.app_context():
        return render_template(
            "device.html",
            show_top_bar=False,
            title=ui_client.name,
            configuration=client.get_configuration().split("\n"),
            device_details=ui_client,
        )


def get_sense_client(installation_id: str) -> Optional[SenseClient]:
    global sense_server_callback
    for client in sense_server_callback().connected_clients:
        if client.details.installation_id == installation_id:
            return client
    return None


def get_connected_clients():
    global sense_server_callback

    clientSet: List[UiClient] = list()

    for client in sense_server_callback().connected_clients:
        clientSet.append(
            UiClient(
                is_online=client.is_online,
                installation_id=client.details.installation_id,
                name=client.details.name,
                version_name=client.details.version_name,
                version_code=client.details.version_code,
            )
        )

    return [client.model_dump() for client in clientSet]

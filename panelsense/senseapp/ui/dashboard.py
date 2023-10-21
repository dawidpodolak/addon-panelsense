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
    configuration: str

    def __hash__(self):
        return hash(self.installation_id)

    def __eq__(self, other):
        if isinstance(other, UiClient):
            return self.installation_id == other.installation_id
        else:
            return False


class UiState(BaseModel):
    selected_client: Optional[UiClient] = None
    clients: Set[UiClient] = set()


dashboard_state = UiState()


def start_web_app(isDebug: bool):
    _LOGGER.info(f"Start web app. UI debug is on: {isDebug}")
    app.run(debug=isDebug, host="0.0.0.0", port=5000)


def set_client_callback(server_callback: Callable[[], ClientConectionHelper]):
    global sense_server_callback
    sense_server_callback = server_callback
    server_callback().client_connected_callbacks.add(on_client_state_changed)
    server_callback().client_diconnected_callbacks.add(on_client_state_changed)


def on_client_state_changed(senseClient: SenseClient):
    _LOGGER.debug(
        f"sense client {senseClient.details.name} online: {senseClient.is_online}"
    )
    update_connected_clients()
    update_selected_client()
    update_page()


def update_page():
    global dashboard_state
    _LOGGER.info(f"Update ui client {dashboard_state.selected_client}")
    with app.app_context():
        render_page = None
        if dashboard_state.selected_client:
            render_page = get_client_details_renderer()
        else:
            render_page = get_client_list_renderer()

        turbo.push(
            turbo.update(
                render_page,
                "main_content",
            )
        )


# START Route region


@app.route("/")
def dashboard():
    return get_dashboard_renderer()


@app.route("/device/<installation_id>")
def show_page(installation_id):
    global dashboard_state
    headers = request.headers
    for header, values in headers.items():
        _LOGGER.info(f"header: {header}: {values}")

    _LOGGER.info(f"show device: {installation_id}")
    selected_client = get_ui_client(installation_id)
    if selected_client:
        dashboard_state = UiState(
            selected_client=selected_client, clients=dashboard_state.clients
        )
        update_page()
        return jsonify({"status": "success"}), 200
    else:
        return (jsonify({"status": "failue", "message": "Client not found"}),)


@app.route("/list")
def show_list():
    global dashboard_state
    _LOGGER.info(f"show list")
    dashboard_state = UiState(clients=dashboard_state.clients)
    update_page()
    return jsonify({"status": "success"}), 200


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


# END Route region


# START Renderer region
def get_dashboard_renderer():
    global dashboard_state
    update_connected_clients()
    _LOGGER.info(f"Client list {len(dashboard_state.clients)}")
    with app.app_context():
        return render_template("index.html", clients=dashboard_state.clients)


def get_client_list_renderer():
    global dashboard_state
    update_connected_clients()
    with app.app_context():
        return render_template("client_list.html", clients=dashboard_state.clients)


def get_client_details_renderer():
    global dashboard_state
    update_connected_clients()
    _LOGGER.info(
        f"Selected client {dashboard_state.selected_client.name}, is online: {dashboard_state.selected_client.is_online}"
    )
    with app.app_context():
        return render_template(
            "client_details.html", client=dashboard_state.selected_client
        )


# END Renderer region


def get_sense_client(installation_id: str) -> Optional[SenseClient]:
    global sense_server_callback
    for client in sense_server_callback().connected_clients:
        if client.details.installation_id == installation_id:
            return client
    return None


# START Client util region
def update_connected_clients():
    global sense_server_callback
    global dashboard_state

    client_set: Set[UiClient] = set()

    for client in sense_server_callback().connected_clients:
        client_set.add(sense_client_to_ui_client(client))

    dashboard_state = UiState(
        selected_client=dashboard_state.selected_client, clients=client_set
    )
    return [client.model_dump() for client in client_set]


def sense_client_to_ui_client(client: SenseClient) -> UiClient:
    return UiClient(
        is_online=client.is_online,
        installation_id=client.details.installation_id,
        name=client.details.name,
        version_name=client.details.version_name,
        version_code=client.details.version_code,
        configuration=client.configuration_str,
    )


def get_ui_client(installation_id: str) -> Optional[UiClient]:
    global dashboard_state
    selected_client = None
    for ui_client in dashboard_state.clients:
        if ui_client.installation_id == installation_id:
            selected_client = ui_client
    return selected_client


def update_selected_client():
    global dashboard_state
    if dashboard_state.selected_client:
        dashboard_state = UiState(
            clients=dashboard_state.clients,
            selected_client=get_ui_client(
                dashboard_state.selected_client.installation_id
            ),
        )

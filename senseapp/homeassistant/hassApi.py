import websocket
import json


def on_message(ws, message):
    print(f"Error: {message}")


def on_error(ws, error):
    print(f"Error: {error}")


def on_close(ws, close_status_code, close_message):
    print(f"Error: {error}")

def on_open(ws):
    print(f"Open socket")

def start_websocket(url, token):
    ws = websocket.WebSocketApp(
        url=url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )

# Sense Server documentation

## Table of contents
1. [Introduction](#introduction)
2. [Authorization](#authorized)
3. [Models](#models)

## Introduction
This documentation provides an information about architecture, models used in sense app related to websocket server application which communicates with PanelSense Android app. It does not touch the part of the application implemented in other moduls

## Models
Each model used to communication with websockets should inherit from ServerOutgoingMessage or ClientIncomingMessage and should contains MessageType. All of this classes are defined at `model/byse.py`

| MessageType   | Description |
| ------------- | ----------- |
| auth          | Message type used for authentication websocket client |
| error         | If received message containt corrupted or not complete data, then message with this type should be returned |
| ha_action     | Message that contains action from or to Home Assistant |

#### Message structure
Below message structure relates incoming message as well as outcoming message.
| Field     | Type          | Description   |
| --------- | ---------     | ------------- |
| type      | MessageType   | type of message |
| data      | Object        | Depends on message type |

## Authorization and credentials
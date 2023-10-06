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
| ha_action_light     | Message that contains light action from or to Home Assistant |
| ha_action_cover     | Message that contains cover action from or to Home Assistant |
| ha_action_switch     | Message that contains cover action from or to Home Assistant |

#### Message structure
Below message structure relates incoming message as well as outcoming message.
| Field     | Type          | Description   |
| --------- | ---------     | ------------- |
| type      | MessageType   | type of message |
| data      | Object        | Depends on message type |

#### Authentication Message

 `type: auth`

##### Incoming message data
| Field     | Type      | Description       |
| --------- | --------- | ----------------- |
| access_token      | str       | generated the combination of username:password at Base64 |
| name              | str       | name of the device |
| version_name      | str       | Name of the app version |
| version_code      | int       | Build number of the app |
| installation_id   | str       | Unique UUID that represents given app on given device |

### Home Assistant Action Light

`type: ha_action_light`

| Field     | Type      | Description       |
| --------- | --------- | ----------------- |
| entity_id | str       | Id of Home Assistant entity   |
| on        | bool      | true if light is on   |
| brightness    | int   | Value from 0 to 255. 0 dark, 255 ligth    |
| color_mode    | str   | hs: hue mode <br>  color_temp: temperature mode <br> white|
| rgb_color | IntArray  | Array of integers represents RGB values from 0 to 255
| supported_color_modes | List<str> | Available mode: hs color_temp |
| max_color_temp_kelvin | int   | max value for color_temp_kelvin |
| min_color_temp_kelvin | int   | min value for color_temp_kelvin|
| max_color_temp_kelvin | int   | current light temperature, set if color_mode is color_temp|

### Home Assistant Action Cover

`type: ha_action_cover`

| Field     | Type      | Description       |
| --------- | --------- | ----------------- |
| entity_id | str       | Id of Home Assistant entity   |
| on        | bool      | true if light is on   |
| brightness    | int   | Value from 0 to 255. 0 dark, 255 ligth    |
| color_mode    | str   | hs: hue mode <br>  color_temp: temperature mode <br> white|
| rgb_color | IntArray  | Array of integers represents RGB values from 0 to 255
| supported_color_modes | List<str> | Available mode: hs color_temp |
| max_color_temp_kelvin | int   | max value for color_temp_kelvin |
| min_color_temp_kelvin | int   | min value for color_temp_kelvin|
| max_color_temp_kelvin | int   | current light temperature, set if color_mode is color_temp|

## Authorization and credentials
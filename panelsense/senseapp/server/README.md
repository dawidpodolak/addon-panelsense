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
| configuration | Configuration for android client |
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

##### Authentication message data
| Field     | Type      | Description       |
| --------- | --------- | ----------------- |
| token      | str       | generated the combination of username:password at Base64 |
| name              | str       | name of the device |
| version_name      | str       | Name of the app version |
| version_code      | int       | Build number of the app |
| installation_id   | str       | Unique UUID that represents given app on given device |

##### Authentication response data
| Field          | Type         | Description       |
| -------------- | ------------ | ----------------- |
| auth_result    | enum         | SUCCESS or FAILURE|

#### Configuration response data
This is a configuration for PanelSense client
| Field         | Type              | Description       |
| ------------- | ----------------- | ----------------- |
| system        | System            | Configuration of how client behaves |
| panel_list    | List<Panel>       | List of panels |

##### System configuration
| Field             | Type              | Description       |
| ----------------- | ----------------- | ----------------- |
| main_panel_id     | str: optional     | Id of PanelItem which will be always visible. If swipe to other pane, app will come back on this. If not defined, than first panel is main

##### Panel
| Field             | Type                  | Description       |
| ----------------- | --------------------- | ----------------- |
| id                | str: optional         | Id of panel, can be set at main_panel_id |
| type              | PanelType: mandatory  | Type of Panel |
| coloumn_coutn     | int: optional         | specify for PanelType grid. Default is 2|
| name              | str: optional         | Name for panel |
| item_list         | List<PanelItem>       | List of panel items |

##### PanelType
|                  | Description       |
| ---------------- | ----------------- |
| grid             | Items are compout at grid |
| home             | Panel with weather (if there is an entity provide), time and two buttons

##### PanelItem
| Field             | Type                  | Description       |
| ----------------- | --------------------- | ----------------- |
| id                | str: optional         | Id of panel item  |
| entity            | str: mandatory        | Home Assistant entity |
| title             | str: optional         | By default is taken from entity   |
| icon              | str: optional         | The name of mdi icon. By default is taken from entity |


### Home Assistant Action Light

`type: ha_action_light`

| Field                 | Type      | Direction     | Description       |
| ---------             | --------- | ---------     | ----------------- |
| brightness            | int       | both          | Value from 0 to 255. 0 dark, 255 ligth    |
| color_mode            | str       | both          | hs: hue mode <br>  color_temp: temperature mode <br> white|
| color_temp_kelvin     | int       | both          | current light temperature, set if color_mode is color_temp|
| entity_id             | str       | both          | Id of Home Assistant entity   |
| friendly_name         | str       | outcoming     | default entuty name
| icon                  | int       | outcoming     | default entity icon
| max_color_temp_kelvin | int       | outcoming     | max value for color_temp_kelvin |
| min_color_temp_kelvin | int       | outcoming     | min value for color_temp_kelvin|
| on                    | bool      | both          | true if light is on   |
| rgb_color             | IntArray  | both          | Array of integers represents RGB values from 0 to 255
| supported_color_modes | List<str> | outcoming     | Available mode: hs color_temp |

### Home Assistant Action Cover

`type: ha_action_cover`

| Field                 | Type      | Direction     | Description       |
| ---------             | --------- | ------------- | ----------------- |
| entity_id             | str       | both          | Id of Home Assistant entity   |
| friendly_name         | str       | outcoming     | default entity name |
| icon                  | str       | outcoming     | default entity icon |
| position              | int       | both          | Value in percenage from 0 to 100 |
| tilt_position         | str       | both          | Value in percenage from 0 to 100 |
| state                 | str       | both          | closing, closed, opened, opening   |
| supported_features    | int       | outcoming     | Available mode: hs color_temp |

### Home Assistant Action Switch

`type: ha_action_switch`

| Field                 | Type      | Direction     | Description       |
| ---------             | --------- | ------------- | ----------------- |
| entity_id             | str       | both          | Id of Home Assistant entity   |
| friendly_name         | str       | outcoming     | default entity name |
| icon                  | str       | outcoming     | default entity icon |
| on                    | bool      | both          | true or false   |

## Authorization and credentials
# PanelSense Configuration



This document provides information how to create yaml configuration for PanelSens Android client.



## Get started

After connecting Android PanelSense app to your PanelSenseAddon, open yaml editor in HomeAssistant (available from addon webUI). Provide your yaml configuration and click button "Send configuration". Be sure that your device is online. Online status is available at the top panel. If device is offline, then configuration won't be send, instead it will be saved and when client become online, this configuration will be send to them.

## YAML Configuration
| Key | Description |
|--|--|
| system | Overall configuration how all app behaves |
| panel_list | List of panel that takes all of screens |

### System
| Key | Required | Description |
|--|--|--|
| main_panel_id | false | Id of panel that is treated as default. If you enable navigation bar, this will be a home button. If not set, then first panel from `panel_list` will be treated as main
| show_nav_bar | false | Navigation bar at the bottom of the screen that help you to navigate you between panels |
| background | false | URL or hex of the background. E.g. of hex "#FFFFFFFF" |

### Panel List
Panels that can be put in `panel_list` list. To use given panel, set `type` key as following:
| type |  |
|--|--|
| home | Panel with weather, time, date and one or two buttons |
| grid | Panel with grid |

#### Panel Home
| Key | Required | Description |
|--|--|--|
| type | true | Should be set to `home` |
| id | false | If set, can be used in `main_panel_id` |
| background | false | URL or hex of the background. E.g. of hex "#FFFFFFFF". |
| time24h | false | If true time will be display with 24 hour format. Otherwise 12hours format will be used |
| weather_entity | false | HomeAssistant weather entity. If not set, weather won't be displayed |
| item_left | false | Left item |
| item_right | false | Right item |

#### Panel Grid
| Key | Required | Description |
|--|--|--|
| type | true | Should be set to `home` |
| id | false | If set, can be used in `main_panel_id` |
| background | false | URL or hex of the background. E.g. of hex "#FFFFFFFF". |
| column_count | false | HomeAssistant weather entity. If not set, weather won't be displayed |
| item_list | false | List of items that will be put into grid

### Items
Item is a part of panels that allows you to controll your entities like light, cover etc. If some entity provides more controll options (like light has brightness or color steering) than shuch item can be long pressed. You don't have to specify the type of item. The type is determined on `entity` key.
| Key | Required | Description |
|--|--|--|
| entity | true | HomeAssistant entity. Base on this, proper item will be used |
| title | false | Displayed title of panel. If empty, it will be taken from entity |
| icon | false | Displayed icon from MDI system e.g. "account" or "lightbulb". If empty, it will be taken from entity |

Icons are taken from https://pictogrammers.com/
### Sample configuration

```yaml
system:
    main_panel_id: "Home"
    show_nav_bar: true
    background: "https://asset.gecdesigns.com/img/background-templates/modern-crystal-abstract-background-template-1612247149783-cover.webp"
panel_list:
    - type: "home"
      id: "Home"
      time24h: true
      weather_entity: "weather.main_weather"
      background: "#66000000"
      item_left:
        entity: "light.kitchen_leds"
        title: "Leds"
        icon: "led-strip-variant"
      item_right:
        entity: "light.kitchen_main"
        title: "Main light"
        icon: "lightbulb"
    - type: "grid"
      id: "covers_and_lights"
      column_count: 3
      background: "#66000000"
      item_list:
        - entity: "cover.kitchen_fron"
          title: "Cover front"
        - entity: "cover.room"
          title: "Room cover"

```

# PanelSense Configuration



This document provides information how to create yaml configuration for PanelSense Android client.



## Get started

After connecting the Android PanelSense app to your PanelSenseAddon, open yaml editor in HomeAssistant (available from the addon webUI). Provide your yaml configuration and click the button "Send configuration". Be sure that your device is online. Online status is available at the top panel. If the device is offline, then the configuration won't be sent, instead, it will be saved and when the client becomes online, this configuration will be sent to them.

## YAML Configuration
| Key | Description |
|--|--|
| system | Overall configuration how app behaves |
| panel_list | List of panels |

### System
| Key | Required | Description |
|--|--|--|
| main_panel_id | false | Id of the panel that is treated as default. If you enable a navigation bar, this will be a home button. If not set, then the first panel from `panel_list` will be treated as the main
| show_nav_bar | false | Navigation bar at the bottom of the screen that help you to navigate between panels |
| background | false | URL or hex of the background. E.g. of hex "#FFFFFFFF" |

### Panel List
Panels that can be put in `panel_list` list. To use given panel, set `type` key as following:
| type |  |
|--|--|
| home | Panel with weather, time, date and one or two buttons |
| grid | Panel with grid |
| flex | Flex panel with columns and rows |

#### Panel Home
<img  src="screenshots/screenshot_panel_home.png?raw=true"  width="350"  />

| Key | Required | Description |
|--|--|--|
| type | true | Should be set to `home` |
| id | false | If set, can be used in `main_panel_id` |
| background | false | URL or hex of the background. E.g. of hex "#FFFFFFFF". |
| time24h | false | If true time will be displayed in 24 hour format. Otherwise, 12hours format will be used |
| weather_entity | false | HomeAssistant weather entity. If not set, the weather won't be displayed |
| item_left | false | Left item |
| item_right | false | Right item |
| item_list | false | List of items that will be put into a bottom panel. The amount of items is not limited. The maximum amount should be determined by you. For NSpanel the max two items look ok. For a 10" tablet it could be 5.

#### Panel Grid
<img  src="screenshots/screenshot_panel_grid.png?raw=true"  width="350" />

| Key | Required | Description |
|--|--|--|
| type | true | Should be set to `grid` |
| id | false | If set, can be used in `main_panel_id` |
| background | false | URL or hex of the background. E.g. of hex "#FFFFFFFF". |
| column_count | false | HomeAssistant weather entity. If not set, the weather won't be displayed |
| item_list | false | List of items that will be put into the grid

#### Panel Flex
<img  src="screenshots/screenshot_panel_flex.png?raw=true"  width="350" />

This panel contains colums and rows that working separately. Rows are displayed from bottom to the top and max amount is 3. Columns (up to 10) contains a lists of items. Columns as same as list can be scrolled if their content exceeds beyond the screen.

| Key | Required | Description |
|--|--|--|
| type | true | Should be set to `flex` |
| id | false | If set, can be used in `main_panel_id` |
| background | false | URL or hex of the background. E.g. of hex "#FFFFFFFF". |
| columns | false | List of columns that contains list of items. Up to 10 |
| rows | false | List of rows that contains list of items. Up to 3

### Items
Item is a part of a panel that allows you to control your entities like light, cover, etc. If some entity provides more control options (like the light has brightness or color steering) then such an item can be long-pressed. You don't have to specify the type of the item. The type is determined by `entity` key.

| Key | Required | Description |
|--|--|--|
| entity | false | HomeAssistant entity. Based on this, the proper item will be used |
| type | false | If specified, then enitity is ignored. Supported values: `clock` |
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
    - type: "flex"
      id: "flex_panel"
	  background: "#66000000"
      columns:
       - - entity: "weather.home"
         - entity: "light.office"
       - - type: "clock"
           time24h: true
         - entity: "cover.kitchen"
       - - entity: "switch.tv"
         - entity: "light.lamp"
      rows:
       - - entity: "cover.kitchen_fron"
           title: "Cover front"
         - entity: "cover.room"
           title: "Room cover"
       - - entity: "cover.kitchen_fron"
           title: "Cover front"
         - entity: "cover.room"
           title: "Room cover"

    - type: "home"
      id: "Home"
      time24h: true
      weather_entity: "weather.main_weather"
      background: "#66000000"
      item_list:
        - entity: "light.kitchen_leds"
          title: "Leds"
          icon: "led-strip-variant"
        - entity: "light.kitchen_main"
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

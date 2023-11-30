

![Logo](https://github.com/dawidpodolak/addon-panelsense/blob/develop/panelsense/logo.png?raw=true)

# Panel Sense

[![MIT License](https://img.shields.io/badge/License-APACHE_2.0-green.svg)](https://github.com/dawidpodolak/addon-panelsense/blob/develop/LICENSE)
[![Version](https://img.shields.io/github/v/release/dawidpodolak/addon-panelsense)](https://github.com/dawidpodolak/addon-panelsense/releases)

PanelSense is a project that helps to manage Home Assistant with Android app that can be installed localy on any Android device like tablet or devices such Sonoff NSPanel. Is fully customizable with this addon installed in HomeAssistant. Android application provides you ability to setup many screens with various options like home panel or grid panel, where you can put buttons to controll light, cover and others HomeAssistant entities.

## Screnshots
<img  src="https://github.com/dawidpodolak/addon-panelsense/blob/feature/documentation/screenshots/screenshot_panel_home.png?raw=true"  width="250" />
<img  src="https://github.com/dawidpodolak/addon-panelsense/blob/feature/documentation/screenshots/screenshot_panel_grid.png?raw=true"  width="250" />
<img  src="https://github.com/dawidpodolak/addon-panelsense/blob/feature/documentation/screenshots/screenshot_details_light.png?raw=true"  width="250" />
<img  src="https://github.com/dawidpodolak/addon-panelsense/blob/feature/documentation/screenshots/screenshot_details_cover.png?raw=true"  width="250" />

## Features
* System
    * navigation bar - bottom bar helps to quick navigate between panel
    * background - set your favourite background by using url or just put simple hex color e.g. "#5B5B5B". It can be set globally for all panels or each panel can has own different background

* HomePanel
    * time - Set time with format 24 hours or 12 hours am pm
    * weather
    * items - quick access for one or two item
* GridPanel - scrollable grid with many items
    * column count

* Items
    * light - provide light entity to controll things like on/off. After long press there is an option to set brightness, hue or color temperature (if supported)
    * cover - provide cover entity to quick ability to close or open. After long press there is an option to set cover position (if supported). Setting tilt position coming soon.
    * support for other features will be added soon.

## Installation

Installation is the same as other addons for HomeAssistant.

1. Copy the url of that repository https://github.com/dawidpodolak/addon-panelsense
2. Open your HomeAssistant instance and navigate to Settings -> Add-on -> Add-on Store
3. At top, right corner click menu button and next Repositories
4. Paste copied url and click Add
5. Now you should see PanelSense addon in section "Home Assistant addon repository"
6. Open it and click Install.
7. After installation, open Configuration and change server_user and serwer_password. This credentials you will need to use in Android app.

## Connect android client

In order to connect an android client, first you need to install android app on your device. To install app please refer to Android project site, [installation section](https://github.com/dawidpodolak/android-panelsense). After installation, you will see a login page where you have to provide:
- IP address to your HA instance where PanelSense is installed
- PanelSense addon port (by default is 8652)
- server_user and server_password
- The name of that device simple to remember for you e.g. `Office table` or `Daily Room NSPanel`. It will help you to identify this device in configuration page

##  Android client configuration

After connecting android client to PanelSense Addon, open web ui in the addon configuration. You can also enable "Show in sidebar" option. If you connect your device properly, you should see the device on the list. Click on that and you will see the top panel with details of the PanelSense device client. Below this, there is a yaml editor to put your configuration. How to configure, please visit [configuration doc](https://github.com/dawidpodolak/addon-panelsense/tree/feature/documentation/configuration.md).

## License

[APACHE 2.0](https://github.com/dawidpodolak/addon-panelsense/blob/develop/LICENSE)


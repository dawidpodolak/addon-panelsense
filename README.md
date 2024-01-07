# Panel Sense

[![MIT License](https://img.shields.io/badge/License-APACHE_2.0-green.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/release/dawidpodolak/addon-panelsense)](releases)

<img  src="panelsense/logo.png?raw=true"  width="500" />


PanelSense is a project that helps to manage Home Assistant with an Android app that can be installed locally on any Android device like a tablet or devices such as Sonoff NSPanel. It's fully customizable with this addon installed in HomeAssistant. Android application provides you the ability to set up many screens with various options like home panel or grid panel, where you can put buttons to control light, cover, and other HomeAssistant entities.

## Screnshots
<img  src="screenshots/screenshot_panel_home.png?raw=true"  width="350" /><img  src="screenshots/screenshot_panel_grid.png?raw=true"  width="350" /><img  src="screenshots/screenshot_details_light.png?raw=true"  width="350" /><img  src="screenshots/screenshot_details_cover.png?raw=true"  width="350" />

## Features
* System
    * navigation bar - bottom bar helps to quickly navigate between panel
    * background - set your favorite background by using URL or just put a simple hex color e.g. "#5B5B5B". It can be set globally for all panels or each panel can have its own different background

* HomePanel
    * time - Set time with format 24 hours or 12 hours am pm
    * weather
    * items - quick access for one or two item
* GridPanel - scrollable grid with many items
    * column count

* Items
    * light - provide light entity to control things like on/off. After a long press, there is an option to set brightness, hue, or color temperature (if supported)
    * cover - provide a cover entity with a quick ability to close or open. After a long press, there is an option to set the cover position (if supported). Setting tilt position coming soon.
    * support for other features will be added soon.

## Installation

Installation is the same as other add-ons for HomeAssistant.

1. Copy the URL of that repository https://github.com/dawidpodolak/addon-panelsense
2. Open your HomeAssistant instance and navigate to Settings -> Add-on -> Add-on Store
3. At the top, right corner click the menu button and next to Repositories
4. Paste the copied URL and click Add
5. Now you should see the PanelSense addon in the section "Home Assistant addon repository"
6. Open it and click Install.
7. After installation, open Configuration and change server_user and serwer_password. This credentials you will need to use in the Android app.

## Connect android client

To connect to an Android client, first, you need to install it on your device. To install the app please refer to the Android project site, [installation section](https://github.com/dawidpodolak/android-panelsense). After installation, you will see a login page where you have to provide:
- IP address to your HA instance where PanelSense is installed
- PanelSense addon port (by default is 8652)
- server_user and server_password
- The name of that device which will be simple to remember for you e.g. `Office table` or `Daily Room NSPanel`. It will help you to identify this device on configuration page

##  Android client configuration

After connecting an Android client to PanelSense Addon, open web UI in the addon configuration. You can also enable "Show in sidebar" option. If you connect your device properly, you should see the device on the list. Click on that and you will see the top panel with details of the PanelSense device client. Below this, there is a yaml editor to put your configuration. How to configure, please visit [configuration doc](configuration.md).

## License

[APACHE 2.0](LICENSE)




![Logo](https://github.com/dawidpodolak/addon-panelsense/blob/develop/panelsense/logo.png?raw=true)

# Panel Sense

[![MIT License](https://img.shields.io/badge/License-APACHE_2.0-green.svg)](https://github.com/dawidpodolak/addon-panelsense/blob/develop/LICENSE)
[![Version](https://img.shields.io/github/v/release/dawidpodolak/addon-panelsense)](https://github.com/dawidpodolak/addon-panelsense/releases)

PanelSense is a project that helps to manage Home Assistant with Android app that can be installed localy on any Android device like tablet or devices such Sonoff NSPanel. Is fully customizable with this addon installed in HomeAssistant

## Installation

Installation is the same as other addons for HomeAssistant.
In order to do that:
1. Copy the url of that repository https://github.com/dawidpodolak/addon-panelsense
2. Open your HomeAssistant instance and navigate to Settings -> Add-on -> Add-on Store
3. At top, right corner click menu button and next Repositories
4. Paste copied url and click Add
5. Now you should see PanelSense addon in section "Home Assistant addon repository"
6. Open it and click Install.
7. After installation, open Configuration and change server_user and serwer_password. This credentials you will need to use in Android app.


## Connect Android Client

In order to connect an android client, first you need to install android app on your device. In order to install app please refer to Android project site, [installation section](https://github.com/dawidpodolak/android-panelsense). After installation, you will see a login page where you have to provide:
- IP address to your HA instance where PanelSense is installed
- PanelSense addon port (by default is 8652)
- server_user and server_password
- The name of that device simple to remember for you e.g. `Office table` or `Daily Room NSPanel`. It will help you to identify this device in configuration page
## Configuration
## License

[APACHE 2.0](https://github.com/dawidpodolak/addon-panelsense/blob/develop/LICENSE)


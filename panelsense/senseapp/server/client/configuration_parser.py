from typing import Any, Dict, List, Union

import yaml
from loguru import logger
from server.model.base import *
from server.model.configuration import *


def parse_configuration(configuration_str: str) -> ConfigurationOutcomingMessage:
    return ConfigurationOutcomingMessage(
        type=MessageType.CONFIGURATION, data=get_configuration(configuration_str)
    )


def get_configuration(configuration_str: str) -> Configuration:
    yaml_config = yaml.safe_load(configuration_str)

    return Configuration(
        system=parse_system(yaml_config.get("system")),
        panel_list=parse_panel_list(yaml_config.get("panel_list")),
    )


def parse_system(system_yaml: Dict[str, Any]) -> ConfigurationSystem:
    return ConfigurationSystem(**system_yaml)


def parse_panel_list(
    panel_list_yaml: List[Dict[str, Any]]
) -> List[ConfigurationPanelUnion]:
    configuration_panel_list = list()
    for panel_yaml in panel_list_yaml:
        try:
            configuration_panel_list.append(parse_panel(panel_yaml))
        except Exception as e:
            logger.error(f"Error: {e} -> {panel_yaml}")

    return configuration_panel_list


def parse_panel(panel_yaml: Dict[str, Any]) -> ConfigurationPanel:
    type = panel_yaml["type"]
    if type == ConfigurationPanelType.GRID.value:
        logger.info(f"Grid panel: {panel_yaml}")
        return ConfigurationGridPanel(**panel_yaml)
    elif type == ConfigurationPanelType.HOME.value:
        logger.info(f"Home panel: {panel_yaml}")
        return ConfigurationHomePanel(**panel_yaml)
    elif type == ConfigurationPanelType.FLEX.value:
        return ConfigurationFlexPanel(**panel_yaml)
    else:
        raise ConfigurationError(f"Unsupported type: {type}")

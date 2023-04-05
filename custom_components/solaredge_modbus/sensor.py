"""Solaredge sensors"""
import logging

from homeassistant.const import CONF_NAME

from .const import (
    BATTERY_1,
    BATTERY_2,
    INVERTER_SENSORS,
    DOMAIN,
    METER_1,
    METER_2,
    METER_3,
    METERS,
    BATTERIES,
)
from . import SolarEdgeEntity, SolaredgeModbusHub
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)


from homeassistant.core import HomeAssistant, callback

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """setup sensors"""
    hub_name = entry.data[CONF_NAME]
    hub = hass.data[DOMAIN][hub_name]["hub"]

    entities = []

    for sensor_info in INVERTER_SENSORS:
        entities.append(SolarEdgeSensorNew(hub, sensor_info))

    if hub.read_meter1:
        for meter_sensor_info in METERS.get(METER_1):
            entities.append(SolarEdgeSensorNew(hub, meter_sensor_info))

    if hub.read_meter2:
        for meter_sensor_info in METERS.get(METER_2):
            entities.append(SolarEdgeSensorNew(hub, meter_sensor_info))

    if hub.read_meter3:
        for meter_sensor_info in METERS.get(METER_3):
            entities.append(SolarEdgeSensorNew(hub, meter_sensor_info))

    if hub.read_battery1:
        for battery_sensor_info in BATTERIES.get(BATTERY_1):
            entities.append(SolarEdgeSensorNew(hub, battery_sensor_info))

    if hub.read_battery2:
        for battery_sensor_info in BATTERIES.get(BATTERY_2):
            entities.append(SolarEdgeSensorNew(hub, battery_sensor_info))

    async_add_entities(entities)
    return True


class SolarEdgeSensorNew(SolarEdgeEntity, SensorEntity):
    """Representation of a solaredge sensor"""

    def __init__(
        self, hub: SolaredgeModbusHub, description: SensorEntityDescription
    ) -> None:
        super().__init__(hub)
        self.entity_description = description
        self._attr_name = f"{self.hub.name} {description.name}"
        self._attr_unique_id = f"{self.hub.name}_{description.key}"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.hub.data.get(self.entity_description.key)
        super()._handle_coordinator_update()

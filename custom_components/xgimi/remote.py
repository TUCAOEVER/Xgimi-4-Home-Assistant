"""Support for the Xgimi Projector."""

from collections.abc import Iterable
import logging

from homeassistant.components.remote import RemoteEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_TOKEN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import XGIMIEntity
from .xgimi import XGIMIBaseEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Xgimi Projector from a config entry."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    host = config[CONF_HOST]
    name = config[CONF_NAME]
    token = config[CONF_TOKEN]
    command_port = config.get("command_port")
    pinging_port = config.get("pinging_port")
    advance_port = config.get("advance_port")

    unique_id = config_entry.unique_id
    assert unique_id is not None

    base_entity = XGIMIBaseEntity(
        ip=host,
        command_port=command_port,
        pinging_port=pinging_port,
        advance_port=advance_port,
        manufacturer_data=token,
        is_on=False,
    )
    async_add_entities([XGIMIRemote(name, unique_id, base_entity)])


class XGIMIRemote(XGIMIEntity, RemoteEntity):
    """XGIMI 远程控制.

    Args:
        XGIMIEntity (_type_): XGIMI 设备对象
        RemoteEntity (_type_): 远程对象

    Returns:
        _type_: XGIMI 远程对象

    """

    @property
    def is_on(self):
        """设备开启时返回 True."""
        return self.base_entity.is_on

    async def async_update(self):
        """更新设备状态."""
        self.base_entity.is_on = await self.async_check_alive()

    async def async_turn_on(self, **kwargs):
        """异步开启设备."""
        await self.async_send_command("poweron")

    async def async_turn_off(self, **kwargs):
        """异步关闭设备."""
        await self.async_send_command("poweroff")

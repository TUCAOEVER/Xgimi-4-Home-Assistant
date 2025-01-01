import asyncio
import logging
import subprocess

import asyncudp
from bluez_peripheral.advert import Advertisement
from bluez_peripheral.util import get_message_bus

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import ADVANCE_COMMAND_DICT, COMMAND_DICT, DOMAIN
from .xgimi import XGIMIBaseEntity

_LOGGER = logging.getLogger(__name__)


class XGIMIEntity(Entity):
    """XGIMI 对象."""

    def __init__(self, name, unique_id, base_entity: XGIMIBaseEntity) -> None:
        """初始化 XGIMI 对象.

        Args:
            name (_type_): 设备名称
            unique_id (_type_): 识别码
            base_entity (XGIMIBaseEntity): 基础 XGIMI 设备对象、

        """
        self.base_entity = base_entity
        self._attr_name = name
        self._attr_unique_id = unique_id

    @property
    def device_info(self) -> DeviceInfo:
        """返回设备信息."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            manufacturer="XGIMI",
            name=self.name,
        )

    async def async_check_alive(self) -> bool:
        """检查设备是否在线."""
        try:
            process = await asyncio.create_subprocess_shell(
                f"ping -c 1 {self.base_entity.ip}",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                await asyncio.wait_for(process.communicate(), timeout=1)
            except TimeoutError:
                process.kill()  # 进程终止
                await process.wait()  # 等待进程结束
                return False
            return bool(process.returncode == 0)
        except Exception as e:
            _LOGGER.debug(
                "Error when checking device's status: %s. Details: %s", self.ip, e
            )
            return False

    async def _async_ble_power_on(
        self,
        manufacturer_data: str,
        company_id: int = 0x0046,
        service_uuid: str = "1812",
    ) -> None:
        """发送开机信号."""
        bus = await get_message_bus()
        advertisment = Advertisement(
            localName="Bluetooth 4.0 RC",
            serviceUUIDs=[service_uuid],
            manufacturerData={company_id: bytes.fromhex(manufacturer_data)},
            timeout=10,
            appearance=961,
        )
        await advertisment.register(bus)

    async def _send_udp_message(self, message, port) -> None:
        """发送 UDP 消息到指定端口."""
        try:
            remote_addr = (self.base_entity.ip, port)
            sock = await asyncudp.create_socket(remote_addr=remote_addr)
            sock.sendto(message.encode("utf-8"))
            sock.close()
        except Exception as e:
            _LOGGER.debug("Failed to send UDP message: %s", e)

    async def async_send_command(self, command) -> None:
        """发送指令."""
        if command in COMMAND_DICT:
            msg = COMMAND_DICT[command]
            await self._send_udp_message(msg, self.base_entity.command_port)
        elif command == "poweroff":
            self.base_entity.is_on = False
            await self._send_udp_message("KEYPRESSES:30", self.base_entity.command_port)
        elif command == "poweron":
            self.base_entity.is_on = True
            await self._async_ble_power_on(self.base_entity.manufacturer_data)
        else:
            msg = ADVANCE_COMMAND_DICT.replace("command_holder", command)
            await self._send_udp_message(msg, self.base_entity.advance_port)

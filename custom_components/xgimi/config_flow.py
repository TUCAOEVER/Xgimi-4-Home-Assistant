"""XGIMIConfig flow."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_TOKEN
from homeassistant.data_entry_flow import FlowResult
from homeassistant.util.network import is_host_valid

from .const import DOMAIN
from .entity import XGIMIEntity
from .xgimi import XGIMIBaseEntity


class XGIMIConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """ConfigFlow 实现类."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """初始化信息以及用户界面."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            name = user_input[CONF_NAME]
            token = user_input[CONF_TOKEN]
            pinging_port = user_input.get("pinging_port")
            command_port = user_input.get("command_port")
            advance_port = user_input.get("advance_port")
            xgimi_entity = XGIMIEntity(
                name=name,
                unique_id=f"{name}-{token}",
                base_entity=XGIMIBaseEntity(
                    ip=host,
                    command_port=command_port,
                    advance_port=advance_port,
                    pinging_port=pinging_port,
                    manufacturer_data=token,
                    is_on=False,
                ),
            )
            if not is_host_valid(host):
                errors[CONF_HOST] = "invalid_host"
            elif not await xgimi_entity.async_check_alive():
                errors[CONF_HOST] = "cannot_connect"
            else:
                await self.async_set_unique_id(f"{name}-{token}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )
        else:
            user_input = {}

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME, default=user_input.get(CONF_NAME, vol.UNDEFINED)
                    ): str,
                    vol.Required(
                        CONF_HOST, default=user_input.get(CONF_HOST, vol.UNDEFINED)
                    ): str,
                    vol.Required(
                        CONF_TOKEN, default=user_input.get(CONF_TOKEN, vol.UNDEFINED)
                    ): str,
                    vol.Required(
                        "pinging_port", default=user_input.get("pinging_port", 554)
                    ): int,
                    vol.Optional(
                        "command_port", default=user_input.get("command_port", 16735)
                    ): int,
                    vol.Optional(
                        "advance_port", default=user_input.get("advance_port", 16750)
                    ): int,
                }
            ),
            errors=errors,
        )

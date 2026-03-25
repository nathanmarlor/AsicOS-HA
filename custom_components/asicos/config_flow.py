"""Config flow for AsicOS Bitcoin Miner."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig

from .const import API_SYSTEM_INFO, CONF_HOST, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): TextSelector(
            TextSelectorConfig(type="text", autocomplete="off")
        ),
    }
)


async def _validate_connection(host: str) -> dict[str, Any]:
    """Validate the user input by connecting to the miner."""
    url = f"http://{host}{API_SYSTEM_INFO}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status != 200:
                raise ConnectionError(f"HTTP {resp.status}")
            data: dict[str, Any] = await resp.json()
            return data


class AsicOSConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AsicOS Bitcoin Miner."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            await self.async_set_unique_id(host)
            self._abort_if_unique_id_configured()

            try:
                info = await _validate_connection(host)
            except (aiohttp.ClientError, TimeoutError, ConnectionError):
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception during config flow")
                errors["base"] = "unknown"
            else:
                title = info.get("board_name", f"AsicOS Miner ({host})")
                return self.async_create_entry(
                    title=title,
                    data={CONF_HOST: host},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle reconfiguration."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip()

            try:
                await _validate_connection(host)
            except (aiohttp.ClientError, TimeoutError, ConnectionError):
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception during reconfigure")
                errors["base"] = "unknown"
            else:
                return self.async_update_reload_and_abort(
                    self._get_reconfigure_entry(),
                    data_updates={CONF_HOST: host},
                )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST,
                        default=self._get_reconfigure_entry().data.get(CONF_HOST, ""),
                    ): TextSelector(
                        TextSelectorConfig(type="text", autocomplete="off")
                    ),
                }
            ),
            errors=errors,
        )

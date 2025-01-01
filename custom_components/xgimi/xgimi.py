class XGIMIBaseEntity:
    def __init__(
        self,
        ip: str,
        command_port: int,
        advance_port: int,
        pinging_port: int,
        manufacturer_data: str,
        is_on: bool,
    ) -> None:
        self._ip = ip
        self._command_port = command_port
        self._advance_port = advance_port
        self._pinging_port = pinging_port
        self._manufacturer_data = manufacturer_data
        self._is_on = is_on

    @property
    def ip(self) -> str:
        """设备IP地址."""
        return self._ip

    @ip.setter
    def ip(self, value: str) -> None:
        self._ip = value

    @property
    def command_port(self) -> int:
        """设备命令端口."""
        return self._command_port

    @command_port.setter
    def command_port(self, value: int) -> None:
        self._command_port = value

    @property
    def advance_port(self) -> int:
        """设备进阶端口."""
        return self._advance_port

    @advance_port.setter
    def advance_port(self, value: int) -> None:
        self._advance_port = value

    @property
    def pinging_port(self) -> int:
        """设备通讯端口."""
        return self._pinging_port

    @pinging_port.setter
    def pinging_port(self, value: int) -> None:
        self._pinging_port = value

    @property
    def manufacturer_data(self) -> str:
        """设备制造商数据，用于设备启动通讯."""
        return self._manufacturer_data

    @manufacturer_data.setter
    def manufacturer_data(self, value: str) -> None:
        self._manufacturer_data = value

    @property
    def is_on(self) -> bool:
        """设备开启时返回 True."""
        return self._is_on

    @is_on.setter
    def is_on(self, value: bool) -> None:
        self._is_on = value

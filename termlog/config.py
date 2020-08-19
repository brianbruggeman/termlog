from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class TerminalConfig:
    """Data class to hold some simple configuration data

    Attributes:
        color: when True, display output with color
        json: when True, display output as json
        timestamp: when True, include timestamp in output
        time_format: control how the timestamp appears in the output

    """

    color: bool = True
    json: bool = False
    time_format: str = "%Y%m%d%H%M%S"
    timestamp: Optional[bool] = None

    def __getitem__(self, item):
        data = asdict(self)
        return data[item]

    def keys(self):
        data = asdict(self)
        return data.keys()


_terminal_config = TerminalConfig()


def set_config(
    color: Optional[bool] = None, json: Optional[bool] = None, time_format: Optional[str] = None, timestamp: Optional[bool] = None,
) -> TerminalConfig:
    """Sets configuration for subsequent termlog API calls.

    Note:  Generally, True should only be set for color or json

    Args:
        color: True will enable color
        json: True will enable json output
        time_format: Sets the timestamp format
        timestamp: True will enable timestamps on each log line

    Returns:
        Updated configuration

    """
    global _terminal_config
    if color is not None:
        _terminal_config.color = color
    if json is not None:
        _terminal_config.json = json
    if time_format is not None:
        _terminal_config.time_format = time_format
    if timestamp is not None:
        _terminal_config.timestamp = timestamp
    return _terminal_config

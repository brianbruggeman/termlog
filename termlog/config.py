from dataclasses import dataclass
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
    timestamp: Optional[bool] = None
    time_format: str = '%Y%m%d%H%M%S'


_terminal_config = TerminalConfig()


def set_config(
        color: Optional[bool] = None,
        json: Optional[bool] = None,
        time_format: Optional[str] = None,
        timestamp: Optional[bool] = None,
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
    _terminal_config.color = color if color is not None else _terminal_config.color
    _terminal_config.json = json if json is not None else _terminal_config.json
    _terminal_config.timestamp = timestamp if timestamp is not None else _terminal_config.timestamp
    _terminal_config.time_format = time_format if time_format is not None else _terminal_config.time_format
    return _terminal_config

import ast
import datetime
import inspect
import json
import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional


def fix_json(obj):
    try:
        return json._default_decoder(obj)
    except Exception:
        return str(obj)


@dataclass
class Message:
    data: Any
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    json: bool = False
    color: bool = False
    type: Any = str
    lexer: str = ''
    time_format: Optional[str] = '%Y%m%d%H%M%S'
    string_format: Optional[str] = ''
    fields: Dict = field(default_factory=dict)

    def __post_init__(self):
        self.time_format = '%Y%m%d%H%M%S' if self.time_format is None else self.time_format
        self.string_format = '' if self.string_format is None else self.string_format
        self._update_fields()

    @property
    def calling_frame(self):
        found = False
        frame = None
        for frame in inspect.getouterframes(inspect.currentframe()):
            if found:
                break
            found = True if frame.function == 'echo' else False
        return None if not (frame and found) else frame

    @property
    def calling_frame_code(self):
        frame = self.calling_frame
        code = ''
        if frame and frame.code_context:
            code = ''.join(frame.code_context).strip()
        return code

    @property
    def calling_frame_data(self):
        frame_data = {}
        frame = self.calling_frame
        if frame:
            members = {k: v for k, v in inspect.getmembers(frame)}
            key_frame = members['frame']
            frame_data.update(key_frame.f_globals)
            frame_data.update(key_frame.f_locals)
        return frame_data

    def _update_fields(self):
        frame_data = self.calling_frame_data
        code = self.calling_frame_code
        parsed = ast.parse(code)
        queue = parsed.body
        data = []
        fields = []
        # Grab field names to get data needed for message
        count = 0
        while queue:
            count += 1
            node = queue.pop(0)
            if isinstance(node, (ast.Expr, ast.FormattedValue, )):
                queue.append(node.value)
            elif isinstance(node, (ast.Call,)):
                # TODO: Find a way to capture the colors here
                for arg in node.args:
                    queue.append(arg)
            elif isinstance(node, (ast.JoinedStr,)):
                for value in node.values:
                    queue.append(value)
            elif isinstance(node, (ast.Str,)):
                data.append(node.s)
            elif isinstance(node, (ast.Name,)):
                fields.append(node.id)
            if count > 1000:  # to prevent a runaway
                break
        for name in fields:
            if name in frame_data:
                self.fields[name] = frame_data[name]

    def __eq__(self, other):
        try:
            equal = (self.data == other.data)
        except AttributeError:
            equal = (self.data == other)
        return equal

    def __radd__(self, other):
        try:
            new_fields = {k: v for k, v in self.fields.items()}
            if isinstance(other, Message):
                new_fields.update(other.fields)
                text = other.data + self.data
            else:
                text = other + str(self.data)
            message = Message(
                text,
                timestamp=self.timestamp,
                json=self.json,
                color=self.color,
                lexer=self.lexer,
                time_format=self.time_format,
                string_format=self.string_format,
                fields=new_fields,
                )
        except (AttributeError, TypeError):
            text = other + str(self.data)
            message = Message(
                text,
                timestamp=self.timestamp,
                json=self.json,
                color=self.color,
                lexer=self.lexer,
                time_format=self.time_format,
                string_format=self.string_format,
                fields=self.fields,
                )
        except Exception:
            breakpoint()
        finally:
            return message

    def __add__(self, other):
        try:
            new_fields = {k: v for k, v in self.fields.items()}
            new_fields.update(other.fields)
            return Message(
                self.data + other.data,
                timestamp=self.timestamp,
                json=self.json,
                color=self.color,
                lexer=self.lexer,
                time_format=self.time_format,
                string_format=self.string_format,
                fields=new_fields,
                )
        except AttributeError:
            return Message(
                self.data + other,
                timestamp=self.timestamp,
                json=self.json,
                color=self.color,
                lexer=self.lexer,
                time_format=self.time_format,
                string_format=self.string_format,
                fields=self.fields,
                )

    def __str__(self):
        from .formatting import beautify
        data = asdict(self)
        if json or not self.color:
            data['data'] = strip_escape(data['data'])
        if not self.json:
            if self.lexer and self.color:
                string = beautify(self.data, lexer=self.lexer)
            else:
                string = self.string_format.format(**data) if self.string_format else f'{self.data}'
        else:
            msg_fields = ['json', 'color', 'lexer', 'type', 'time_format', 'string_format']
            for field_name in msg_fields:
                data.pop(field_name)
            for field_name, field_value in data.pop('fields', {}).items():
                data[field_name] = field_value
            data['timestamp'] = data['timestamp'].strftime(self.time_format)
            string = json.dumps(data, default=fix_json)
        return str(string)


def strip_escape(text):
    """Remove terminal ascii escape sequences from *text*.

    Args:
        text (str): text to strip escape sequences from

    Returns:
        str: text stripped of escape sequences

    """
    # These are all valid escape sequences... they're probably not
    #  inclusive
    sequences = [
        r'\033',
        r'\x1b',
        r'\u001b',
        ]
    value_sequence = r'\[[0-9;]+m'
    for escape_sequence in sequences:
        pattern = f'{escape_sequence}{value_sequence}'
        replacement = ''
        text = re.sub(pattern, replacement, text)
    return text

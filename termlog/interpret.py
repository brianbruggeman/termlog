"""Interprets each AST node"""
import ast
import sys
import textwrap
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ExtractableFields:
    queue_append: List[str] = field(default_factory=list)
    queue_extend: List[str] = field(default_factory=list)
    field_update: List[str] = field(default_factory=list)


def extract_fields(code: str) -> Dict[str, Any]:
    """Extracts data from code block searching for variables

    Args:
        code: the code block to parse
    """
    # Parsing expects that the code have no indentation
    code = textwrap.dedent(code)
    parsed = ast.parse(code)
    queue: List[Any] = parsed.body
    fields: Dict[str, Any] = {}
    # Grab field names to get data needed for message
    count = -1
    while queue:
        count += 1
        node = queue.pop(0)
        ignored = tuple([ast.Constant, ast.FormattedValue])
        node_data = (
            ", ".join(f"{key}={getattr(node, key)}" for key in node._fields)
            if hasattr(node, "_fields")
            else ", ".join(d for d in dir(node) if not d.startswith("_"))
        )
        ast_mapping = {
            ast.alias: "asname",
            ast.arg: "arg",
            ast.ExceptHandler: "name",
            ast.Name: "id",
        }
        if not (hasattr(node, "__module__") and node.__module__ == "_ast"):
            continue
        if isinstance(node, (ast.Name,)) and not isinstance(node.ctx, ast.Store):
            continue
        if isinstance(node, ignored):
            pass
        elif isinstance(node, tuple(ast_mapping.keys())):
            field_name = ast_mapping[type(node)]
            field_value = getattr(node, field_name)
            if field_value:
                fields.update({field_value: None})
        elif hasattr(node, "_fields"):
            for field_name in node._fields:
                field_value = getattr(node, field_name)
                if hasattr(field_value, "__module__") and field_value.__module__ == "_ast":
                    queue.append(field_value)
                elif isinstance(field_value, (list, tuple)):
                    queue.extend(field_value)
                elif field_value is None:
                    continue
                elif sys.argv[0].endswith("pytest") and "--pdb" in sys.argv:
                    node_lineno = node.lineno if hasattr(node, "lineno") else -1
                    lined_code = "\n".join(
                        f"{'--> ' if lineno + 1 == node_lineno else '    '}{line}" for lineno, line in enumerate(code.split("\n"))
                    )
                    print(f"   * ignoring field: {field_name} = {repr(field_value)} from {repr(node)} in\n\n{lined_code}\n\n")
                    breakpoint()
        else:
            node_lineno = node.lineno if hasattr(node, "lineno") else -1
            lined_code = "\n".join(
                f"{'--> ' if lineno + 1 == node_lineno else '    '}{line}" for lineno, line in enumerate(code.split("\n"))
            )
            print(f"Termlog Warning [Unhandled ast.Node]: {repr(node)} => {node_data} in \n\n{lined_code}\n\n")
            pass

        if count > 4096:  # to prevent a runaway queue
            break
    return fields

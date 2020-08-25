"""Interprets each AST node"""
import ast
import textwrap
from typing import Any, Dict, List


def extract_fields(code: str) -> Dict[str, Any]:
    """Extracts data from code block searching for variables

    Args:
        code: the code block to parse
    """
    # Parsing expects that the code have no indentation
    code = textwrap.dedent(code)
    parsed = ast.parse(code)
    queue: List[Any] = parsed.body
    data = []
    fields: Dict[str, Any] = {}
    # Grab field names to get data needed for message
    count = -1
    while queue:
        count += 1
        node = queue.pop(0)
        ignored = tuple([ast.ImportFrom, ast.Import, ast.Assert, ast.Raise])
        unhandled = tuple(
            [
                ast.Constant,
                ast.Dict,
                ast.DictComp,
                ast.Expr,
                ast.GeneratorExp,
                ast.For,
                ast.List,
                ast.ListComp,
                ast.Return,
                ast.Subscript,
                ast.Try,
                ast.With,
            ]
        )
        if isinstance(node, (list, tuple)):
            queue.extend(node)
        elif isinstance(node, (ast.Expr, ast.FormattedValue, ast.Assign, ast.Starred, ast.Attribute, ast.Subscript, ast.AnnAssign)):
            queue.append(node.value)
        elif isinstance(node, (ast.Call,)):
            queue.extend(node.args)
        elif isinstance(node, (ast.JoinedStr, ast.BoolOp)):
            queue.extend(node.values)
        elif isinstance(node, (ast.Str,)):
            data.append(node.s)
        elif isinstance(node, (ast.Name,)):
            fields.update({node.id: None})
        elif isinstance(node, (ast.BinOp,)):
            queue.append(node.left)
            queue.append(node.right)
        elif isinstance(node, (ast.FunctionDef,)):
            queue.extend(node.body)
        elif isinstance(node, (ast.If, ast.IfExp)):
            queue.append(node.body)
            queue.append(node.orelse)
        # elif isinstance(node, (ast.DictComp,)):
        #     queue.extend(node.generators)
        #     queue.append(node.key)
        #     queue.append(node.value)
        # elif isinstance(node, (ast.Try,)):
        #     queue.extend(node.body)
        #     queue.extend(node.orelse)
        #     queue.extend(node.finalbody)
        elif isinstance(node, ignored):
            pass
        elif isinstance(node, unhandled):
            # print("Termlog Warning [Debug ast.Node]:", node, ", ".join([d for d in dir(node) if not d.startswith("_")]))
            pass
        else:
            print("Termlog Warning [Unhandled ast.Node]:", node, ", ".join([d for d in dir(node) if not d.startswith("_")]))

        if count > 4096:  # to prevent a runaway queue
            break
    return fields

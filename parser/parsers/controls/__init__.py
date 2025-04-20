from parser.parsers.controls.forexpr import parse_for_expr
from parser.parsers.controls.ifexpr import parse_if_expr
from parser.parsers.controls.whileexpr import parse_while_expr

CONTROL_EXPRESSIONS = {
    "for": parse_for_expr,
    "if": parse_if_expr,
    "while": parse_while_expr,
}

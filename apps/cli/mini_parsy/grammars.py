"""The grammars the jobs run, written against parsy as a user of the library
writes them: parsy's own tests, the examples that ship with it, and the
parsers a service or a tool needs (a config file, an access log, CSV, an
HTTP request head, version ranges, a search query language).

Each builder returns a fresh parser; GRAMMARS maps a job's grammar name to
its builder."""
import enum
import re
from collections import namedtuple
from dataclasses import dataclass
from datetime import date

from parsy import (
    alt,
    any_char,
    char_from,
    decimal_digit,
    digit,
    eof,
    forward_declaration,
    from_enum,
    generate,
    index,
    letter,
    line_info,
    match_item,
    peek,
    regex,
    seq,
    string,
    string_from,
    success,
    test_char,
    test_item,
    whitespace,
)

GRAMMARS = {}


def grammar(name):
    def register(fn):
        GRAMMARS[name] = fn
        return fn

    return register


def lower(s):
    return s.lower()


# ------------------------------------------------------------ the tests


@grammar("string")
def _():
    return string("x")


@grammar("string_lower")
def _():
    return string("x", transform=lower)


@grammar("string_cat")
def _():
    return string("Cat", transform=lower)


@grammar("regex_digit")
def _():
    return regex(r"[0-9]")


@grammar("regex_group")
def _():
    return regex(r"a([0-9])b", group=1)


@grammar("regex_name")
def _():
    return regex(r"a(?P<name>[0-9])b", group="name")


@grammar("regex_tuple")
def _():
    return regex(r"a([0-9])b([0-9])c", group=(1, 2))


@grammar("regex_optional_group")
def _():
    return regex(r"(\d+)(?:\.(\d+))?", group=(1, 2))


@grammar("regex_flags")
def _():
    return regex(r"select\s+(\w+)", flags=re.IGNORECASE, group=1)


@grammar("then")
def _():
    return string("x") >> string("y")


@grammar("bind")
def _():
    return string("x").bind(lambda x: string("y"))


@grammar("bind_double")
def _():
    # a letter, then the same letter again
    return regex(r"[a-z]").bind(lambda c: string(c).result(c + c))


@grammar("map")
def _():
    return digit.map(int)


@grammar("combine")
def _():
    return seq(digit, letter).combine(lambda d, l: (d, l))


@grammar("combine_dict_date")
def _():
    return (
        seq(
            regex(r"[0-9]{2}").map(int).tag("day"),
            regex(r"[0-9]{2}").map(int).tag("month"),
            regex(r"[0-9]{4}").map(int).tag("year"),
        )
        .map(dict)
        .combine_dict(date)
    )


Pair = namedtuple("Pair", ["word", "number"])


@grammar("combine_dict_pair")
def _():
    return seq(
        regex(r"[A-Z]+").tag("word"),
        regex(r"[0-9]+").map(int).tag("number"),
    ).combine_dict(Pair)


@grammar("combine_dict_none")
def _():
    return seq(
        regex(r"[A-Z]+").tag("word"),
        whitespace.tag(None),
        regex(r"[0-9]+").map(int).tag("number"),
    ).combine_dict(Pair)


@grammar("combine_dict_underscore")
def _():
    return seq(
        regex(r"[A-Z]+").tag("word"),
        whitespace.tag("_whitespace"),
        regex(r"[0-9]+").map(int).tag("number"),
    ).combine_dict(Pair)


@grammar("concat")
def _():
    return letter.many().concat()


@grammar("generate")
def _():
    @generate
    def xy():
        yield string("x")
        yield string("y")
        return 3

    return xy


@grammar("generate_parser")
def _():
    @generate
    def example():
        yield string("x")
        return string("y")

    return example


@grammar("mark")
def _():
    return (letter.many().mark() << string("\n")).many()


@grammar("tag")
def _():
    return letter.many().concat().tag("word").sep_by(string(","))


@grammar("tag_dict")
def _():
    return seq(letter.tag("first_letter"), letter.many().concat().tag("remainder")).map(dict)


@grammar("generate_desc")
def _():
    @generate("a thing")
    def thing():
        yield string("t")

    return thing


@grammar("generate_no_desc")
def _():
    @generate
    def thing():
        yield string("a")
        yield string("b")

    return thing


@grammar("abc")
def _():
    return string("a") | string("b") | string("c")


@grammar("backtrack")
def _():
    @generate
    def xy():
        yield string("x")
        yield string("y")
        return "never"

    return xy | string("z") | string("xq")


@grammar("or")
def _():
    return string("x") | string("y")


@grammar("or_then")
def _():
    return (string("\\") >> string("y")) | string("z")


@grammar("many")
def _():
    return letter.many()


@grammar("many_then")
def _():
    return string("x").many() >> string("y")


@grammar("times0")
def _():
    return letter.times(0)


@grammar("times3")
def _():
    return letter.times(3)


@grammar("times3_then")
def _():
    return letter.times(3) >> digit


@grammar("times2_4")
def _():
    return letter.times(2, 4)


@grammar("times2_4_then")
def _():
    return letter.times(2, 4) >> digit


@grammar("at_most")
def _():
    return string("ab").at_most(2)


@grammar("at_least")
def _():
    return string("ab").at_least(2)


@grammar("until")
def _():
    return string("s").until(string("x"))


@grammar("until_seq")
def _():
    return seq(string("s").until(string("x")), string("x"))


@grammar("until_then")
def _():
    return string("s").until(string("x")).then(string("x"))


@grammar("until_any")
def _():
    return regex(".").until(string("x"))


@grammar("until_consume")
def _():
    return string("s").until(string("x"), consume_other=True)


@grammar("until_min")
def _():
    return string("s").until(string("x"), min=3)


@grammar("until_max")
def _():
    return string("s").until(string("x"), max=3)


@grammar("until_min_max")
def _():
    return string("s").until(string("x"), min=3, max=5)


@grammar("optional")
def _():
    return string("a").optional()


@grammar("optional_b")
def _():
    return string("a").optional("b")


@grammar("sep_by")
def _():
    return digit.map(int).sep_by(string(","))


@grammar("sep_by_2_4")
def _():
    return digit.map(int).sep_by(string(","), min=2, max=4)


@grammar("sep_by_max0")
def _():
    return digit.sep_by(string(","), max=0)


@grammar("add")
def _():
    return letter + digit


@grammar("add_lists")
def _():
    return letter.times(2) + digit.times(1, 3)


@grammar("multiply")
def _():
    return letter * 3


@grammar("multiply_range")
def _():
    return letter * range(1, 3)


@grammar("alt_empty")
def _():
    return alt()


@grammar("alt")
def _():
    return alt(letter, digit)


@grammar("seq_empty")
def _():
    return seq()


@grammar("seq1")
def _():
    return seq(letter)


@grammar("seq2")
def _():
    return seq(letter, digit)


@grammar("seq_kw")
def _():
    return seq(first_name=regex(r"\S+") << whitespace, last_name=regex(r"\S+"))


@grammar("seq_kw_a")
def _():
    return seq(a=string("a"))


@grammar("ascii")
def _():
    return test_char(lambda c: ord(c) < 128, "ascii character")


@grammar("char_from")
def _():
    return char_from("ab")


@grammar("titles")
def _():
    return string_from("Mr", "Mr.", "Mrs", "Mrs.")


@grammar("titles_hyde")
def _():
    return string_from("Mr", "Mr.", "Mrs", "Mrs.") + string(" Hyde")


@grammar("titles_lower")
def _():
    return string_from("Mr", "Mr.", "Mrs", "Mrs.", transform=lower)


@grammar("peek_any")
def _():
    return peek(any_char)


@grammar("peek_digit")
def _():
    return peek(digit)


@grammar("any_char")
def _():
    return any_char


@grammar("whitespace")
def _():
    return whitespace


@grammar("letter")
def _():
    return letter


@grammar("digit")
def _():
    return digit


@grammar("decimal")
def _():
    return decimal_digit.at_least(1).concat()


@grammar("line_info")
def _():
    @generate
    def foo():
        i = yield line_info
        l = yield any_char
        return (l, i)

    return foo.many()


@grammar("index")
def _():
    @generate
    def foo():
        i = yield index
        l = yield letter
        return (l, i)

    return foo.many()


@grammar("should_fail")
def _():
    return digit.should_fail("not a digit") >> regex(r".*")


@grammar("should_fail_value")
def _():
    return digit.should_fail("not a digit")


class Pet(enum.Enum):
    CAT = "cat"
    DOG = "dog"
    CATERPILLAR = "caterpillar"


class Position(enum.Enum):
    FIRST = 1
    SECOND = 2
    TWELFTH = 12


@grammar("enum_pet")
def _():
    return from_enum(Pet)


@grammar("enum_position")
def _():
    return from_enum(Position)


@grammar("enum_pet_lower")
def _():
    return from_enum(Pet, transform=lower)


@grammar("eof")
def _():
    return string("a") << eof


# token streams: START and STOP are opaque markers


class Marker:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


START = Marker("START")
STOP = Marker("STOP")


@grammar("start_stop")
def _():
    return test_item(lambda i: i in [START, STOP], "START/STOP").many()


@grammar("match_start")
def _():
    return match_item(START, "START")


@grammar("match_start_default")
def _():
    return match_item("x")


@grammar("bracketed")
def _():
    other = test_item(lambda i: i not in [START, STOP], "not START/STOP")
    return match_item(START) >> other.many() << match_item(STOP)


@grammar("forward")
def _():
    expr = forward_declaration()
    simple = regex("[0-9]+").map(int)
    group = string("(") >> expr.sep_by(string(" ")) << string(")")
    expr.become(simple | group)
    return expr


@grammar("forward_az")
def _():
    expr = forward_declaration()
    expr.become(string("A") + expr | string("Z"))
    return expr


@grammar("forward_unset")
def _():
    return forward_declaration()


# ------------------------------------------------------------ parsy's examples

# examples/json.py


@grammar("json")
def _():
    ws = regex(r"\s*")

    def lexeme(p):
        return p << ws

    lbrace = lexeme(string("{"))
    rbrace = lexeme(string("}"))
    lbrack = lexeme(string("["))
    rbrack = lexeme(string("]"))
    colon = lexeme(string(":"))
    comma = lexeme(string(","))
    true = lexeme(string("true")).result(True)
    false = lexeme(string("false")).result(False)
    null = lexeme(string("null")).result(None)
    number = lexeme(regex(r"-?(0|[1-9][0-9]*)([.][0-9]+)?([eE][+-]?[0-9]+)?")).map(float)
    string_part = regex(r'[^"\\]+')
    string_esc = string("\\") >> (
        string("\\")
        | string("/")
        | string('"')
        | string("b").result("\b")
        | string("f").result("\f")
        | string("n").result("\n")
        | string("r").result("\r")
        | string("t").result("\t")
        | regex(r"u[0-9a-fA-F]{4}").map(lambda s: chr(int(s[1:], 16)))
    )
    quoted = lexeme(string('"') >> (string_part | string_esc).many().concat() << string('"'))
    json_value = forward_declaration()
    object_pair = seq(quoted << colon, json_value).map(tuple)
    json_object = lbrace >> object_pair.sep_by(comma).map(dict) << rbrace
    array = lbrack >> json_value.sep_by(comma) << rbrack
    json_value.become(quoted | number | json_object | array | true | false | null)
    return ws >> json_value


# tests/test_sexpr.py; `expr` is a forward declaration here, since a
# generator body can name a parser defined after it and a closure cannot.


@grammar("sexpr")
def _():
    ws = regex(r"\s+", re.MULTILINE)
    comment = regex(r";.*")
    ignore = (ws | comment).many()

    def lexeme(p):
        return p << ignore

    lparen = lexeme(string("("))
    rparen = lexeme(string(")"))
    number = lexeme(regex(r"\d+")).map(int)
    symbol = lexeme(regex(r"[\d\w_-]+"))
    true = lexeme(string("#t")).result(True)
    false = lexeme(string("#f")).result(False)
    atom = true | false | number | symbol
    expr = forward_declaration()

    @generate("a form")
    def form():
        yield lparen
        els = yield expr.many()
        yield rparen
        return els

    @generate
    def quote():
        yield string("'")
        e = yield expr
        return ["quote", e]

    expr.become(form | quote | atom)
    return ignore >> expr.many()


# examples/sql_select.py


class Operator(enum.Enum):
    EQ = "="
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="


@dataclass
class Number:
    value: int


@dataclass
class String:
    value: str


@dataclass
class Field:
    name: str


@dataclass
class Table:
    name: str


@dataclass
class Comparison:
    left: object
    operator: Operator
    right: object


@dataclass
class Select:
    columns: list
    table: Table
    where: object


@grammar("select")
def _():
    number_literal = regex(r"-?[0-9]+").map(int).map(Number)
    string_literal = regex(r"'[^']*'").map(lambda s: String(s[1:-1]))
    identifier = regex("[a-zA-Z][a-zA-Z0-9_]*")
    field = identifier.map(Field)
    table = identifier.map(Table)
    space = regex(r"\s+")
    padding = regex(r"\s*")
    column_expr = field | string_literal | number_literal
    operator = from_enum(Operator)
    comparison = seq(
        left=column_expr << padding,
        operator=operator,
        right=padding >> column_expr,
    ).combine_dict(Comparison)
    SELECT = string("SELECT")
    FROM = string("FROM")
    WHERE = string("WHERE")
    return seq(
        _select=SELECT + space,
        columns=column_expr.sep_by(padding + string(",") + padding, min=1),
        _from=space + FROM + space,
        table=table,
        where=(space >> WHERE >> space >> comparison).optional(),
        _end=padding + string(";"),
    ).combine_dict(Select)


# examples/simple_logo_lexer.py and simple_logo_parser.py


@grammar("logo_lexer")
def _():
    command = string_from("fd", "bk", "rt", "lt")
    number = regex(r"[0-9]+").map(int)
    optional_whitespace = regex(r"\s*")
    eol = string("\n")
    line = seq(
        optional_whitespace >> command,
        whitespace >> number,
        (eof | eol | (whitespace >> eol)).result("\n"),
    )
    return line.many().map(lambda ls: sum(ls, []))


class Command:
    def __init__(self, parameter):
        self.parameter = parameter

    def __repr__(self):
        return f"{self.__class__.__name__}({self.parameter})"


class Forward(Command):
    pass


class Backward(Command):
    pass


class Right(Command):
    pass


class Left(Command):
    pass


COMMANDS = {"fd": Forward, "bk": Backward, "rt": Right, "lt": Left}


@grammar("logo_program")
def _():
    @generate
    def statement():
        cmd_name = yield test_item(lambda i: i in COMMANDS.keys(), "command")
        parameter = yield test_item(lambda i: isinstance(i, int), "number")
        yield match_item("\n")
        return COMMANDS[cmd_name](int(parameter))

    return statement.many()


# examples/simple_eval.py


@grammar("eval_lexer")
def _():
    ws = regex(r"\s*")
    integer = digit.at_least(1).concat().map(int)
    float_ = (digit.many() + string(".").result(["."]) + digit.many()).concat().map(float)
    return ws >> ((float_ | integer | regex(r"[()*/+-]")) << ws).many()


@grammar("eval_tokens")
def _():
    lparen = match_item("(")
    rparen = match_item(")")
    expr = forward_declaration()

    @generate
    def number():
        sign = yield match_item("+") | match_item("-") | success("+")
        value = yield test_item(lambda x: isinstance(x, (int, float)), "number")
        return value if sign == "+" else -value

    simple = (lparen >> expr << rparen) | number

    @generate
    def multiplicative():
        res = yield simple
        op = match_item("*") | match_item("/")
        while True:
            operation = yield op | success("")
            if not operation:
                break
            operand = yield simple
            if operation == "*":
                res *= operand
            elif operation == "/":
                res /= operand
        return res

    @generate
    def additive():
        res = yield multiplicative
        sign = match_item("+") | match_item("-")
        while True:
            operation = yield sign | success("")
            if not operation:
                break
            operand = yield multiplicative
            if operation == "+":
                res += operand
            elif operation == "-":
                res -= operand
        return res

    expr.become(additive)
    return expr


# ------------------------------------------------------------ real-world parsers

# An INI-style settings file: sections, `key = value` and `key: value`,
# comments, blank lines, quoted values and continuation-free lines. Each
# setting is marked with where it starts, for messages that name the line.


@grammar("ini")
def _():
    hspace = regex(r"[ \t]*")
    eol = regex(r"[ \t]*(\r?\n|$)")
    comment = regex(r"[ \t]*[#;][^\n]*") << eol
    blank = regex(r"[ \t]*\r?\n")
    skip = (comment | blank).many()
    name = regex(r"[A-Za-z0-9_.-]+")
    section = string("[") >> hspace >> name << hspace << string("]") << eol
    quoted = string('"') >> regex(r'[^"\r\n]*') << string('"')
    bare = regex(r"[^\r\n#;]*").map(lambda s: s.rstrip())
    tail = regex(r"[ \t]*([#;][^\n]*)?") << eol
    setting = (
        seq(hspace >> name << hspace << char_from("=:") << hspace, (quoted | bare) << tail)
        .mark()
        .map(lambda m: (m[0][0] + 1, m[1][0], m[1][1]))
    )
    body = (setting << skip).many()
    sect = seq(section << skip, body)
    return seq(skip >> body, sect.many()).combine(lambda top, sects: {"": top, **dict(sects)}) << eof


# One line of nginx's combined log format.


@grammar("access_log")
def _():
    sp = string(" ")
    field = regex(r"[^ ]+")
    quoted = string('"') >> regex(r'([^"\\]|\\.)*') << string('"')
    month = from_enum(Month)
    when = seq(
        string("[") >> regex(r"[0-9]{2}").map(int),
        string("/") >> month,
        string("/") >> regex(r"[0-9]{4}").map(int),
        string(":") >> regex(r"[0-9]{2}:[0-9]{2}:[0-9]{2}"),
        sp >> regex(r"[+-][0-9]{4}") << string("]"),
    ).map(tuple)
    request = seq(
        method=regex(r"[A-Z]+") << sp,
        target=regex(r"[^ ]+") << sp,
        version=string("HTTP/") >> regex(r"[0-9]\.[0-9]"),
    ) | regex(r"[^\"]*").map(lambda s: {"raw": s})
    size = string("-").result(0) | regex(r"[0-9]+").map(int)
    return seq(
        addr=field << sp,
        ident=field << sp,
        user=(string("-").result(None) | field) << sp,
        time=when << sp,
        request=string('"') >> request << string('"') << sp,
        status=regex(r"[1-5][0-9]{2}").map(int) << sp,
        bytes=size << sp,
        referer=quoted.map(lambda s: None if s == "-" else s) << sp,
        agent=quoted,
    )


class Month(enum.Enum):
    JAN = "Jan"
    FEB = "Feb"
    MAR = "Mar"
    APR = "Apr"
    MAY = "May"
    JUN = "Jun"
    JUL = "Jul"
    AUG = "Aug"
    SEP = "Sep"
    OCT = "Oct"
    NOV = "Nov"
    DEC = "Dec"


# RFC 4180 CSV: quoted fields with doubled quotes and line breaks inside,
# CRLF or LF records, an optional final line break.


@grammar("csv")
def _():
    dquote = string('"')
    escaped = dquote >> (regex(r'[^"]+') | string('""').result('"')).many().concat() << dquote
    plain = regex(r'[^,"\r\n]*')
    fld = escaped | plain
    record = fld.sep_by(string(","), min=1)
    newline = regex(r"\r?\n")
    # a final line break would read as one more record holding one empty field
    return (record.sep_by(newline) << eof).map(lambda rows: rows[:-1] if len(rows) > 1 and rows[-1] == [""] else rows)


# An HTTP/1.1 request head (RFC 9112): request line, header fields with
# optional whitespace, obsolete line folding refused, and the blank line.


@grammar("http_request")
def _():
    crlf = string("\r\n")
    token = regex(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+")
    method = token.desc("a method")
    target = regex(r"[^ \r\n]+").desc("a request target")
    version = string("HTTP/") >> seq(regex(r"[0-9]").map(int) << string("."), regex(r"[0-9]").map(int)).map(tuple)
    ows = regex(r"[ \t]*")
    value = regex(r"[^\r\n]*").map(lambda s: s.rstrip(" \t"))
    header = seq(token.map(lambda s: s.lower()) << string(":") << ows, value << crlf).map(tuple)
    return seq(
        method=method << string(" "),
        target=target << string(" "),
        version=version << crlf,
        headers=header.many(),
        _end=crlf,
    ).combine_dict(Request)


Request = namedtuple("Request", ["method", "target", "version", "headers"])


# npm-style version ranges: comparators joined by spaces, sets joined by
# `||`, carets and tildes, x-ranges and hyphen ranges.


class Op(enum.Enum):
    GE = ">="
    LE = "<="
    GT = ">"
    LT = "<"
    EQ = "="
    CARET = "^"
    TILDE = "~"


@grammar("semver_range")
def _():
    num = regex(r"0|[1-9][0-9]*").map(int)
    part = num | char_from("xX*").result("x")
    pre = (string("-") >> regex(r"[0-9A-Za-z.-]+")).optional()
    version = seq(
        part,
        (string(".") >> part).optional("x"),
        (string(".") >> part).optional("x"),
    ).map(tuple)
    full = seq(version, pre).combine(lambda v, p: v + ((p,) if p else ()))
    op = from_enum(Op)
    comparator = seq(op.optional(Op.EQ) << regex(r"\s*"), full).map(tuple)
    hyphen = seq(full << regex(r"\s+-\s+"), full).combine(lambda a, b: ("range", a, b))
    clause = hyphen | comparator.sep_by(regex(r"\s+"), min=1)
    return regex(r"\s*") >> clause.sep_by(regex(r"\s*\|\|\s*"), min=1) << regex(r"\s*")


# A search query language: a lexer that makes tokens, then a parser over
# the token list with precedence (NOT, then AND, then OR), parentheses,
# field:value terms, quoted phrases and comparisons.


@grammar("query_lexer")
def _():
    ws = regex(r"\s*")
    word = regex(r"[A-Za-z_][A-Za-z0-9_.-]*").map(
        lambda w: (w.upper(),) if w.upper() in ("AND", "OR", "NOT") else ("WORD", w)
    )
    numb = regex(r"-?[0-9]+").map(lambda s: ("NUM", int(s)))
    phrase = (string('"') >> regex(r'[^"]*') << string('"')).map(lambda s: ("PHRASE", s))
    punct = string_from("(", ")", ":", ">=", "<=", ">", "<", "-").map(lambda s: (s,))
    token = (word | numb | phrase | punct).desc("a token")
    return ws >> (token << ws).many() << eof


@grammar("query_parser")
def _():
    def tok(kind):
        return test_item(lambda t: t[0] == kind, kind)

    expr = forward_declaration()
    value = (tok("WORD") | tok("PHRASE") | tok("NUM")).map(lambda t: t[1])
    compare = seq(
        tok("WORD").map(lambda t: t[1]),
        (tok(":") | tok(">=") | tok("<=") | tok(">") | tok("<")).map(lambda t: t[0]),
        value,
    ).combine(lambda f, o, v: ("field", f, o, v))
    term = compare | value.map(lambda v: ("term", v))
    group = tok("(") >> expr << tok(")")

    @generate
    def unary():
        negs = yield (tok("NOT") | tok("-")).many()
        node = yield group | term
        for _ in negs:
            node = ("not", node)
        return node

    @generate
    def conj():
        first = yield unary
        rest = yield (tok("AND").optional() >> unary).many()
        return first if not rest else ("and", [first] + rest)

    @generate
    def disj():
        first = yield conj
        rest = yield (tok("OR") >> conj).many()
        return first if not rest else ("or", [first] + rest)

    expr.become(disj)
    return expr

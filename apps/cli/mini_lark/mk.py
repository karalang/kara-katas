"""Writes data/: grammars, the inputs they parse, broken grammars, a
copy of lark's bundled grammars for %import, and the job list."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def put(path, body):
    full = os.path.join(DATA, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="") as f:
        f.write(body)


GRAMMARS = {
    "calc.lark": r"""// a calculator with variables, after lark's calc example
?start: sum
      | NAME "=" sum    -> assign_var

?sum: product
    | sum "+" product   -> add
    | sum "-" product   -> sub

?product: power
    | product "*" power  -> mul
    | product "/" power  -> div
    | product "%" power  -> mod

?power: atom
    | atom "**" power    -> pow

?atom: INT              -> number
     | "-" atom         -> neg
     | NAME             -> var
     | NAME "(" [sum ("," sum)*] ")" -> call
     | "(" sum ")"

%import common.CNAME -> NAME
%import common.INT
%import common.WS_INLINE
%ignore WS_INLINE
""",
    "json.lark": r"""// JSON, after lark's json example
?start: value

?value: object
      | array
      | string
      | SIGNED_NUMBER      -> number
      | "true"             -> true
      | "false"            -> false
      | "null"             -> null

array  : "[" [value ("," value)*] "]"
object : "{" [pair ("," pair)*] "}"
pair   : string ":" value

string : ESCAPED_STRING

%import common.ESCAPED_STRING
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS
""",
    "conf.lark": r"""// a service configuration language: blocks, settings, lists, durations
start: _NL* (item _NL*)*

?item: block
     | setting

block: NAME [STRING] "{" _NL* (item _NL*)* "}" _NL
setting: key "=" value _NL
         | key "+=" value _NL -> append
key: NAME ("." NAME)*

?value: STRING          -> string
      | INT             -> int
      | DURATION        -> duration
      | SIZE            -> size
      | "true"          -> true
      | "false"         -> false
      | "[" [value ("," value)* [","]] "]" -> list
      | "env" "(" STRING ")" -> env

DURATION.2: INT ("ms" | "s" | "m" | "h" | "d")
SIZE.2: INT ("KB" | "MB" | "GB")
NAME: /[a-z_][a-z0-9_-]*/
STRING: "\"" /[^"\n]*/ "\""
COMMENT: /#[^\n]*/
_NL: /\r?\n/

%import common.INT
%import common.WS_INLINE
%ignore WS_INLINE
%ignore COMMENT
""",
    "sql.lark": r"""// a SELECT statement with case-insensitive keywords
start: select (";" select)* [";"]

select: "SELECT"i [DISTINCT] columns "FROM"i source join* [where] [group] [order] [limit]

DISTINCT: "DISTINCT"i
columns: "*"                -> all_columns
       | column ("," column)*
column: expr ["AS"i NAME]

source: NAME [NAME]
join: [JOIN_KIND] "JOIN"i source "ON"i expr
JOIN_KIND: "LEFT"i | "INNER"i

where: "WHERE"i expr
group: "GROUP"i "BY"i expr ("," expr)*
order: "ORDER"i "BY"i ordering ("," ordering)*
ordering: expr [DIRECTION]
DIRECTION: "ASC"i | "DESC"i
limit: "LIMIT"i INT

?expr: or_expr
?or_expr: and_expr | or_expr "OR"i and_expr -> or_
?and_expr: not_expr | and_expr "AND"i not_expr -> and_
?not_expr: comparison | "NOT"i not_expr -> not_
?comparison: sum | sum COMP_OP sum -> compare
           | sum "IS"i "NULL"i -> is_null
           | sum "IN"i "(" expr ("," expr)* ")" -> in_list
?sum: term | sum ADD_OP term -> binop
?term: atom | term MUL_OP atom -> binop
?atom: NAME                  -> ref
     | NAME "." NAME         -> qualified
     | INT                   -> int
     | STRING                -> string
     | NAME "(" [expr ("," expr)* | "*"] ")" -> func
     | "(" expr ")"

COMP_OP: "=" | "<>" | "!=" | "<=" | ">=" | "<" | ">"
ADD_OP: "+" | "-"
MUL_OP: "*" | "/"
NAME: /[A-Za-z_][A-Za-z0-9_]*/
STRING: /'[^']*'/
COMMENT: /--[^\n]*/

%import common.INT
%import common.WS
%ignore WS
%ignore COMMENT
""",
    "outline.lark": r"""// an indented outline, after lark's indented_tree example
?start: _NL* item*

item: entry _NL [_INDENT item+ _DEDENT]
entry: (WORD | TAG | NUMBER | DONE)+

DONE.2: "[x]"
TAG: /@[a-z]+/
WORD: /[A-Za-z][A-Za-z'-]*[.,:]?/
NUMBER: /\d+(\.\d+)?/

%import common.WS_INLINE
%declare _INDENT _DEDENT
%ignore WS_INLINE

_NL: /(\r?\n[\t ]*)+/
""",
    "features.lark": r"""// templates, overrides, extends, imports, priorities and repeats
%import .shared (ID, sep_list, _semi)
%import .shared.QUOTED -> TEXT
%import common.WS
%ignore WS

start: stmt*
?stmt: decl _semi
     | call _semi
     | tagged _semi
     | code _semi

decl: "let" ID "=" value
call: ID "(" [sep_list{value, ","}] ")"
!tagged: "#" ID ("." ID)~0..2
code: HEX~2..4 -> hex_code
    | "%" DIGITS

?value: TEXT | NUMBER | ID | list
list: "[" sep_list{value, ";"}? "]"

NUMBER: /-?\d+/
HEX: /[0-9a-f]/
DIGITS: /[0-9]{3}/
""",
    "shared.lark": r"""// definitions other grammars import
ID: /[a-z][a-z0-9_]*/
QUOTED: /'[^']*'/
_semi: ";"
sep_list{item, sep}: item (sep item)*
UNUSED: "never"
""",
    "override.lark": r"""// %override, %extend and %declare on an imported base grammar
%import .base (start, expr, atom, NUMBER, WS)
%ignore WS

%override atom: NUMBER | NAME | "(" expr ")"
%extend expr: expr "^" atom -> power
NAME: /[a-z]+/
""",
    "base.lark": r"""start: expr
?expr: atom
     | expr "+" atom -> plus
atom: NUMBER
NUMBER: /\d+/
WS: " "
""",
    "keywords.lark": r"""// the same terminals with the basic and the contextual lexer
start: (assign | label)*
assign: NAME "=" VALUE ";"
label: NAME ":"
NAME: /[a-z]+/
VALUE: /[a-z0-9]+/
%ignore " "
""",
    "placeholders.lark": r"""start: item+
item: "<" [NAME] ["=" NAME] ">"
    | "(" NAME? ")"           -> paren
    | "{" _opt_names "}"      -> brace
_opt_names: [NAME ("," NAME)*]
NAME: /\w+/
%ignore " "
""",
}

INPUTS = {
    "calc.txt": """1 + 2 * 3
(1 + 2) * 3
2 ** 3 ** 2
-4 - -6
x = 10
y = x * 2 + 1
y % 7
max(x, y, 3) - min(4, 2)
total = abs(-12) + x / 3
total / 0
z + 1
3 +
2 * (4 + 5
7 $ 2
""",
    "package.json": """{
  "name": "mini-lark-demo",
  "version": "1.2.0",
  "private": true,
  "scripts": {"build": "tsc -p .", "test": "jest --ci"},
  "dependencies": {"lodash": "^4.17.21", "express": "4.19.2"},
  "files": [],
  "keywords": ["parser", "grammar", "lalr"],
  "engines": {"node": ">=18"},
  "rating": -2.5e3,
  "nested": [[1, 2], [3, [4, null]], {}]
}
""",
    "broken.json": """{
  "name": "broken",
  "list": [1, 2,, 3],
  "ok": true
}
""",
    "service.conf": """# payments service
name = "payments"
port = 8443
debug = false
timeouts.read = 30s
timeouts.write = 1500ms

upstream "ledger" {
  hosts = ["10.0.0.4:7000", "10.0.0.5:7000",]
  retries = 3
  backoff = 250ms
}

cache {
  size = 512MB
  ttl = 1h
  tags = []
  tags += "hot"
  limits {
    per_user = 64KB
  }
}

secret = env("PAYMENTS_TOKEN")
""",
    "bad.conf": """name = "api"
upstream "a" {
  hosts = ["x"
}
""",
    "queries.sql": """SELECT * FROM users;
select id, name AS who FROM users u WHERE u.age >= 18 AND NOT banned ORDER BY name DESC LIMIT 10;
SELECT DISTINCT country, count(*) AS n FROM users GROUP BY country ORDER BY n DESC, country;
Select o.id, u.name FROM orders o LEFT JOIN users u ON o.user_id = u.id WHERE o.total * 2 > 100 OR o.status IN ('open', 'held');
SELECT name FROM users WHERE email IS NULL -- missing emails
""",
    "bad.sql": """SELECT id FROM users WHERE ORDER BY id
""",
    "todo.outline": """
release 1.4 @work
    backend
        migrate users table @db
        [x] add retry to webhooks
    frontend
        dark mode @ui
            check contrast
        [x] fix login form
groceries @home
    milk 2
    bread
""",
    "bad.outline": """root
    child
  stray
""",
    "statements.feat": """let a = 'hello';
let b = [1; 2; 'three'];
log(a, b, 42);
reset();
#build.release;
#x;
07;
4c2;
%123;
""",
    "bad.feat": """let a = 'x';
#a.b.c.d;
""",
    "math.ovr": "1 + (2 ^ 3) + x",
    "kw.txt": "a = b; c: d = e1;",
    "ph.txt": "<a> <=b> <c=d> <> (x) () {} {p, q}",
}

BAD_GRAMMARS = r"""%%% missing colon
a
%%% incorrect value type
a: 1
%%% unclosed parenthesis
a: ("x"
%%% unmatched paren
a: "x")
%%% bad rule name
Aa: "x"
%%% alias needs lowercase
a: "x" -> "y"
%%% unexpected colon
a: b:
%%% misplaced operator
a: b??
%%% option or new rule
a: "a"
()
%%% dotted terminal
A.B
%%% literal first
"a"
%%% import a string
%import "a"
%%% ignore an import
%ignore %import
%%% undefined rule
start: a b
a: "x"
%%% undefined terminal
start: X
%%% defined twice
start: "a"
start: "b"
%%% empty terminal
start: A
A: ""
%%% recursive terminal
start: A
A: "a" A
%%% rule in terminal
start: A
A: "a" b
b: "b"
%%% alias in terminal
start: A
A: "a" -> x
%%% inlined alias
start: _a
_a: "x" -> y
%%% unknown ignore
start: "a"
%ignore WS
%%% double underscore
start: __x
__x: "a"
%%% bad range
start: "a"~3..1
%%% override missing
%override start: "a"
%%% extend missing
%extend start: "a"
%%% template arity
start: t{"a"}
t{x, y}: x y
%%% template undefined
start: u{"a"}
%%% reduce reduce
start: a | b
a: "x"
b: "x"
%%% newline in string
start: "a
b"
%%% zero width
start: A
A: /a*/
%%% bad escape
start: "\"
%%% inline expand1
start: _x
?_x: "a"
%%% nothing imported
%import common
start: "a"
%%% ok after all
start: "a"+ B?
B: "b"
"""

JOBS = """# mini_lark jobs
grammar calc.lark
calc calc.txt
grammar json.lark
json package.json
json broken.json
recover broken.json
grammar conf.lark
conf service.conf
conf bad.conf
grammar sql.lark
sql queries.sql
sql bad.sql
grammar outline.lark
outline todo.outline
outline bad.outline
grammar features.lark
parse features.lark statements.feat
parse features.lark bad.feat
grammar override.lark
parse override.lark math.ovr
parse keywords.lark kw.txt lexer=basic
parse keywords.lark kw.txt lexer=contextual
parse placeholders.lark ph.txt
parse placeholders.lark ph.txt maybe_placeholders=false
lex calc.lark calc.txt
complete json.lark {"a": [1, true, {"b": 
complete sql.lark SELECT a FROM t WHERE
badgrammars
meta
summary
"""


def main():
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    for name, body in GRAMMARS.items():
        put("grammars/" + name, body)
    for name, body in INPUTS.items():
        put("inputs/" + name, body)
    put("bad_grammars.txt", BAD_GRAMMARS)
    for name in ("common.lark", "lark.lark", "python.lark", "unicode.lark"):
        with open(os.path.join(HERE, "lark", "grammars", name), encoding="utf-8") as f:
            put("lark_grammars/" + name, f.read())
    put("jobs.txt", JOBS)


main()

"""Write data/: grammars for rply in a small line format, inputs to lex and
parse with them, and data/jobs.txt, the jobs that run them.

A grammar file holds one directive a line:
    tokens A B C          the token names given to ParserGenerator
    lex NAME pattern      LexerGenerator.add(NAME, pattern)
    ignore pattern        LexerGenerator.ignore(pattern)
    prec left A B         one entry of the precedence list
    rule <text>           ParserGenerator.production(<text>), whose action
                          builds a node; "<text> %prec NAME" passes
                          precedence=NAME
    onerror               install an error handler

Run: python3 -s -P -B mk.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
FILES = []
JOBS = []


def put(rel, text):
    path = os.path.join(D, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(text.encode("utf-8"))
    FILES.append(rel)
    return rel


def grammar(name, text):
    return put("grammars/%s.grammar" % name, text)


def inp(name, text):
    return put("inputs/%s" % name, text)


def job(line):
    JOBS.append(line)


def section(title):
    JOBS.append("# " + title)


# ------------------------------------------------------------ grammars

CALC = r"""# The calculator from rply's README, grown: variables, calls, comparisons.
tokens NUMBER IDENT PLUS MINUS TIMES DIV MOD POW LPAREN RPAREN COMMA ASSIGN EQ LT GT
lex NUMBER \d+
lex IDENT [A-Za-z_][A-Za-z0-9_]*
lex POW \*\*
lex PLUS \+
lex MINUS -
lex TIMES \*
lex DIV /
lex MOD %
lex LPAREN \(
lex RPAREN \)
lex COMMA ,
lex EQ ==
lex ASSIGN =
lex LT <
lex GT >
ignore [ \t]+
ignore \#[^\n]*
prec nonassoc EQ LT GT
prec left PLUS MINUS
prec left TIMES DIV MOD
prec right UMINUS
prec right POW
rule stmt : IDENT ASSIGN expr | expr
rule expr : expr PLUS expr | expr MINUS expr | expr TIMES expr | expr DIV expr | expr MOD expr
rule expr : expr POW expr
rule expr : expr EQ expr | expr LT expr | expr GT expr
rule expr : MINUS expr %prec UMINUS
rule expr : LPAREN expr RPAREN
rule expr : IDENT LPAREN args RPAREN
rule expr : NUMBER | IDENT
rule args : expr | args COMMA expr
"""

JSON = r"""# JSON, the way rply's users write it.
tokens STRING NUMBER TRUE FALSE NULL LBRACE RBRACE LBRACKET RBRACKET COLON COMMA
lex STRING "(?:[^"\\]|\\.)*"
lex NUMBER -?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?
lex TRUE true\b
lex FALSE false\b
lex NULL null\b
lex LBRACE \{
lex RBRACE \}
lex LBRACKET \[
lex RBRACKET \]
lex COLON :
lex COMMA ,
ignore \s+
rule value : object | array | STRING | NUMBER | TRUE | FALSE | NULL
rule object : LBRACE RBRACE | LBRACE members RBRACE
rule members : pair | members COMMA pair
rule pair : STRING COLON value
rule array : LBRACKET RBRACKET | LBRACKET elements RBRACKET
rule elements : value | elements COMMA value
"""

QUERY = r"""# A SELECT statement over CSV tables.
tokens SELECT FROM WHERE AND OR NOT ORDER BY ASC DESC LIMIT STAR COMMA LPAREN RPAREN CMP NUMBER STRING IDENT
lex SELECT SELECT\b
lex FROM FROM\b
lex WHERE WHERE\b
lex AND AND\b
lex OR OR\b
lex NOT NOT\b
lex ORDER ORDER\b
lex BY BY\b
lex ASC ASC\b
lex DESC DESC\b
lex LIMIT LIMIT\b
lex STAR \*
lex COMMA ,
lex LPAREN \(
lex RPAREN \)
lex CMP <=|>=|<>|<|>|=
lex NUMBER -?\d+
lex STRING '[^']*'
lex IDENT [a-z_][a-z0-9_]*
ignore \s+
prec left OR
prec left AND
prec right NOT
rule query : SELECT cols FROM IDENT where order limit
rule cols : STAR | collist
rule collist : IDENT | collist COMMA IDENT
rule where : | WHERE cond
rule cond : cond OR cond | cond AND cond | NOT cond | LPAREN cond RPAREN | operand CMP operand
rule operand : IDENT | NUMBER | STRING
rule order : | ORDER BY IDENT dir
rule dir : | ASC | DESC
rule limit : | LIMIT NUMBER
"""

calc = grammar("calc", CALC)
json_g = grammar("json", JSON)
query = grammar("query", QUERY)

# The classic conflicts and mistakes, each in its own small grammar.
dangling = grammar("dangling_else", r"""tokens IF THEN ELSE ID
lex IF if\b
lex THEN then\b
lex ELSE else\b
lex ID [a-z]+
ignore \s+
rule stmt : IF ID THEN stmt | IF ID THEN stmt ELSE stmt | ID
""")
dangling_prec = grammar("dangling_else_prec", r"""tokens IF THEN ELSE ID
lex IF if\b
lex THEN then\b
lex ELSE else\b
lex ID [a-z]+
ignore \s+
prec nonassoc THEN
prec nonassoc ELSE
rule stmt : IF ID THEN stmt | IF ID THEN stmt ELSE stmt | ID
""")
ambiguous = grammar("ambiguous", r"""tokens NUMBER PLUS TIMES
lex NUMBER \d+
lex PLUS \+
lex TIMES \*
ignore \s+
rule expr : expr PLUS expr | expr TIMES expr | NUMBER
""")
rr = grammar("reduce_reduce", r"""tokens ID COMMA COLON
lex ID [a-z]+
lex COMMA ,
lex COLON :
ignore \s+
rule decl : names COLON ID | labels COLON
rule names : ID | names COMMA ID
rule labels : ID | labels COMMA ID
""")
unused = grammar("unused", r"""tokens NUMBER PLUS MINUS SEMI
lex NUMBER \d+
lex PLUS \+
lex MINUS -
ignore \s+
rule sum : sum PLUS NUMBER | NUMBER
rule difference : sum MINUS NUMBER
""")
bad_name = grammar("bad_name", r"""tokens NUMBER PLUS
lex NUMBER \d+
rule NUMBER : NUMBER PLUS NUMBER
""")
bad_prec = grammar("bad_prec", r"""tokens NUMBER MINUS
lex NUMBER \d+
prec left MINUS
rule expr : MINUS expr %prec NEG
rule expr : NUMBER
""")
dup_prec = grammar("dup_prec", r"""tokens NUMBER PLUS
prec left PLUS
prec right PLUS
rule expr : expr PLUS expr | NUMBER
""")
bad_assoc = grammar("bad_assoc", r"""tokens NUMBER PLUS
prec middle PLUS
rule expr : expr PLUS expr | NUMBER
""")
no_colon = grammar("no_colon", r"""tokens NUMBER
rule expr -> NUMBER
""")
bare_rule = grammar("bare_rule", r"""tokens NUMBER
rule expr
""")
undefined = grammar("undefined", r"""tokens NUMBER PLUS
rule expr : expr PLUS term | term
""")
epsilon = grammar("epsilon", r"""tokens WORD SEMI
lex WORD [a-z]+
lex SEMI ;
ignore \s+
rule doc : stmts
rule stmts : | stmts stmt
rule stmt : words SEMI
rule words : | words WORD
""")
keyword_prefix = grammar("keyword_prefix", r"""# SELECT is added before IDENT and has no \b, so it matches the start
# of SELECTED.
tokens SELECT IDENT
lex SELECT SELECT
lex IDENT [A-Z]+
ignore \s+
rule query : SELECT IDENT
""")
eq_order = grammar("eq_order", r"""# ASSIGN is added before EQ, so == lexes as two ASSIGN tokens.
tokens ID ASSIGN EQ
lex ID [a-z]+
lex ASSIGN =
lex EQ ==
ignore \s+
rule test : ID EQ ID | ID ASSIGN ID
""")
unlexed = grammar("unlexed", r"""# COMMENT is lexed but is not one of the parser's tokens.
tokens NUMBER PLUS
lex NUMBER \d+
lex PLUS \+
lex COMMENT \#[^\n]*
ignore [ \t\n]+
rule expr : expr PLUS NUMBER | NUMBER
""")
handler = grammar("handler", r"""tokens NUMBER PLUS LPAREN RPAREN
lex NUMBER \d+
lex PLUS \+
lex LPAREN \(
lex RPAREN \)
ignore \s+
onerror
rule expr : expr PLUS term | term
rule term : NUMBER | LPAREN expr RPAREN
""")
lines = grammar("lines", r"""# Newlines are tokens; only spaces are ignored.
tokens WORD NEWLINE
lex WORD [a-z]+
lex NEWLINE \n
ignore [ \t]+
rule doc : line | doc line
rule line : words NEWLINE | NEWLINE
rule words : WORD | words WORD
""")
right_list = grammar("right_list", r"""tokens ITEM COMMA
lex ITEM [a-z0-9]+
lex COMMA ,
ignore \s+
rule list : ITEM | ITEM COMMA list
""")

# ------------------------------------------------------------ inputs

def calc_in(name, text):
    return inp("calc/" + name, text)


arith = calc_in("arith.txt", "1 + 2 * 3")
paren = calc_in("paren.txt", "(1 + 2) * 3")
neg = calc_in("neg.txt", "-2 ** 2")
powr = calc_in("pow.txt", "2 ** 3 ** 2")
mixed = calc_in("mixed.txt", "10 - 4 - 3 % 2 / 1")
call = calc_in("call.txt", "max(1, 2 + 3, -4)")
assign = calc_in("assign.txt", "total = price * qty")
cmp_chain = calc_in("cmp_chain.txt", "1 < 2 < 3")
cmp_ok = calc_in("cmp.txt", "1 + 1 == 2")
trailing = calc_in("trailing.txt", "1 +")
two_ops = calc_in("two_ops.txt", "1 + * 2")
unclosed = calc_in("unclosed.txt", "(1 + 2")
extra = calc_in("extra.txt", "(1 + 2))")
badchar = calc_in("badchar.txt", "1 + 2 @ 3")
badchar2 = calc_in("badchar2.txt", "1 +\n   @")
comment = calc_in("comment.txt", "1 + 2 # three")
empty = calc_in("empty.txt", "")
spaces = calc_in("spaces.txt", "   ")
newline = calc_in("newline.txt", "1 +\n2")
assign_bad = calc_in("assign_bad.txt", "1 = 2")

json_doc = inp("json/config.json", """{
  "name": "orders-service",
  "port": 8080,
  "debug": false,
  "ratio": 0.75,
  "tags": ["api", "internal", "v2"],
  "db": {"host": "db.internal", "pool": {"min": 2, "max": 16}, "replica": null},
  "limits": [],
  "empty": {},
  "escapes": "tab\\there \\"quoted\\" \\u00e9",
  "big": -1.5e-3
}
""")
json_trailing = inp("json/trailing_comma.json", '{"a": 1, "b": [1, 2,], }\n')
json_single = inp("json/single_quotes.json", "{'a': 1}\n")
json_keyword = inp("json/truely.json", '[true, trueish]\n')
json_nested = inp("json/nested.json", '[[[[[["deep"]]]]], {"k": [{"x": {}}]}]\n')
json_unterminated = inp("json/unterminated.json", '{"a": [1, 2\n')
json_scalar = inp("json/scalar.json", '42\n')
json_leading_zero = inp("json/leading_zero.json", '[0, 01]\n')

query_in = inp("queries/report.sql", """SELECT * FROM people
SELECT name, city FROM people WHERE age >= 30
SELECT name, age FROM people WHERE city = 'Oslo' OR city = 'Lima' ORDER BY age DESC
SELECT name FROM people WHERE NOT city = 'Oslo' AND age < 40 ORDER BY name
SELECT name FROM people WHERE NOT (city = 'Oslo' AND age < 40) ORDER BY name LIMIT 3
SELECT id, total FROM orders WHERE total > 100 ORDER BY total LIMIT 2
SELECT id, customer FROM orders WHERE status <> 'paid' ORDER BY customer ASC
SELECT name FROM people WHERE age > 30 AND city = 'Oslo' OR name = 'Ann'
SELECT name FROM people WHERE age > 30 AND (city = 'Oslo' OR name = 'Ann')
SELECT nickname FROM people
SELECT name FROM pets
SELECT name, FROM people
SELECT name FROM people WHERE age > 30 AND
SELECT name FROM people LIMIT 2 ORDER BY name
SELECT name FROM people WHERE city = "Oslo"
select name from people
SELECT name FROM people WHERE age > 25 ORDER BY city DESC LIMIT 0
SELECT selected FROM people
""")
put("tables/people.csv", """name,age,city
Ann,34,Oslo
Bo,28,Lima
Cai,41,Oslo
Dee,25,Pune
Eli,30,Lima
Fay,52,Kyiv
Gus,30,Oslo
""")
put("tables/orders.csv", """id,customer,total,status
1001,Ann,250,paid
1002,Bo,75,pending
1003,Cai,120,paid
1004,Ann,99,refunded
1005,Eli,310,pending
1006,Fay,101,paid
""")

session = inp("calc/session.txt", """# a calculator session
price = 12
qty = 3
total = price * qty
total - 2 ** 3
discount = total / 7
total % 7
-total / 7
-total % 7
max(price, qty, 40) - min(price, qty)
abs(-5) + abs(5)
2 ** 10 ** 1
price > qty
price == qty * 4
missing + 1
total / (qty - 3)
2 ** -1
max()
avg(1, 2)
(price
price * * qty
qty = qty + 1
qty
1 < 2 < 3
""")

dangling_in = inp("dangling.txt", "if a then if b then c else d")
dangling_in2 = inp("dangling2.txt", "if a then b else if c then d else e")
amb_in = inp("ambiguous.txt", "1 + 2 * 3 + 4")
rr_in1 = inp("rr1.txt", "a, b: int")
rr_in2 = inp("rr2.txt", "a, b:")
unused_in = inp("unused.txt", "1 + 2 + 3")
eps_in = inp("epsilon.txt", "a b; ; c;")
eps_empty = inp("epsilon_empty.txt", "")
kw_in1 = inp("keyword1.txt", "SELECT NAME")
kw_in2 = inp("keyword2.txt", "SELECTED")
kw_in3 = inp("keyword3.txt", "SELECT SELECTED")
eq_in = inp("eq.txt", "a == b")
eq_in2 = inp("eq2.txt", "a = b")
unlexed_in = inp("unlexed.txt", "1 + 2 # sum\n+ 3")
handler_in1 = inp("handler1.txt", "1 + (2 + 3")
handler_in2 = inp("handler2.txt", "1 + )")
handler_in3 = inp("handler3.txt", "(1 + 2) + 3")
lines_in = inp("lines.txt", "one two\n\nthree\nfour five six\n")
lines_noeol = inp("lines_noeol.txt", "one\ntwo")
crlf_in = inp("crlf.txt", "one\r\ntwo\r\n")
right_in = inp("right.txt", "a, b, c, d")
right_bad = inp("right_bad.txt", "a, b,")
tok_multi = inp("multiline.txt", "x = 1 +\n  2 *\n\n    (3 - y)\n")
tok_unicode = inp("unicode.txt", "café = 1")
query_sample = inp("queries/sample.sql", "SELECT name, age FROM people\n  WHERE city = 'Oslo' AND age >= 30\nORDER BY age DESC LIMIT 2\n")

# ------------------------------------------------------------ jobs

section("building the parsers: states, default reductions, conflicts")
for g in [calc, json_g, query, dangling, dangling_prec, ambiguous, rr, unused,
          epsilon, keyword_prefix, eq_order, unlexed, handler, lines, right_list]:
    job("build " + g)

section("mistakes ParserGenerator refuses")
for g in [bad_name, bad_prec, dup_prec, bad_assoc, no_colon, bare_rule, undefined]:
    job("build " + g)

section("the lexer: tokens, positions and LexingError")
for g, i in [(calc, arith), (calc, tok_multi), (calc, badchar), (calc, badchar2),
             (calc, comment), (calc, empty), (calc, spaces), (calc, tok_unicode),
             (json_g, json_doc), (json_g, json_keyword), (json_g, json_single),
             (json_g, json_leading_zero), (keyword_prefix, kw_in2), (keyword_prefix, kw_in3),
             (eq_order, eq_in), (query, query_sample), (lines, crlf_in)]:
    job("tokens %s %s" % (g, i))

section("parse trees: precedence and associativity")
for i in [arith, paren, neg, powr, mixed, call, assign, cmp_ok, comment, newline]:
    job("parse %s %s" % (calc, i))

section("parse errors")
for i in [cmp_chain, trailing, two_ops, unclosed, extra, badchar, badchar2,
          empty, spaces, assign_bad]:
    job("parse %s %s" % (calc, i))

section("the conflict grammars at work")
for g, i in [(dangling, dangling_in), (dangling, dangling_in2), (dangling_prec, dangling_in),
             (dangling_prec, dangling_in2), (ambiguous, amb_in), (rr, rr_in1), (rr, rr_in2),
             (unused, unused_in), (epsilon, eps_in), (epsilon, eps_empty),
             (keyword_prefix, kw_in1), (keyword_prefix, kw_in2), (keyword_prefix, kw_in3),
             (eq_order, eq_in), (eq_order, eq_in2), (unlexed, unlexed_in),
             (handler, handler_in1), (handler, handler_in2), (handler, handler_in3),
             (lines, lines_in), (lines, lines_noeol), (lines, crlf_in),
             (right_list, right_in), (right_list, right_bad)]:
    job("parse %s %s" % (g, i))

section("JSON documents")
for i in [json_doc, json_nested, json_scalar, json_trailing, json_single,
          json_keyword, json_unterminated, json_leading_zero]:
    job("parse %s %s" % (json_g, i))

section("programs: a calculator session, a JSON formatter, SELECT over CSV")
job("!calc %s %s" % (calc, session))
job("!json %s %s %s %s %s" % (json_g, json_doc, json_nested, json_scalar, json_trailing))
job("!query %s %s" % (query, query_in))

put("jobs.txt", "\n".join(JOBS) + "\n")
with open(os.path.join(D, "files.txt"), "w") as f:
    f.write("\n".join(FILES) + "\n")
print("%d files, %d jobs" % (len(FILES), sum(1 for j in JOBS if not j.startswith("#"))))

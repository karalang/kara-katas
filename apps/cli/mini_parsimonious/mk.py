# Writes data/: the grammars and the inputs they read, plus jobs.txt and
# files.txt. Run as: python3 -s -P -B mk.py
import os

D = 'data'
files = []


def put(name, text):
    os.makedirs(os.path.dirname(os.path.join(D, name)), exist_ok=True)
    with open(os.path.join(D, name), 'w', newline='') as f:
        f.write(text)
    files.append(name)


# ---------------------------------------------------------------- grammars

put('grammars/calc.peg', r'''
# Integer arithmetic with the usual precedence and a few functions.
line    = _ expr
expr    = term (addop term)*
term    = factor (mulop factor)*
factor  = number / paren / neg / call
neg     = "-" _ factor
paren   = "(" _ expr ")" _
call    = name "(" _ args? ")" _
args    = expr ("," _ expr)*
addop   = ~r"[+-]" _
mulop   = ~r"[*/%]" _
number  = ~r"[0-9]+" _
name    = ~r"[a-z]+"
_       = ~r"[ \t]*"
''')

put('grammars/json.peg', r'''
value   = _ (object / array / string / number / true / false / null) _
object  = "{" _ members? "}"
members = pair ("," _ pair)*
pair    = string _ ":" value
array   = "[" _ items? "]"
items   = value ("," value)*
string  = ~r'"(?:[^"\\\x00-\x1f]|\\["\\/bfnrt]|\\u[0-9a-fA-F]{4})*"'
number  = ~r"-?(?:0|[1-9][0-9]*)"
true    = "true"
false   = "false"
null    = "null"
_       = ~r"\s*"
''')

put('grammars/ini.peg', '''
# An INI file: sections, key = value pairs, comments and blank lines.
file      = (blank / comment / section / pair)*
section   = "[" ~r"[^\\]\\n]+" "]" _ nl
pair      = _ key _ ~r"[:=]" _ val nl
key       = ~r"[A-Za-z0-9_.\\-]+"
val       = ~r"[^\\n]*"
comment   = _ ~r"[#;][^\\n]*" nl
blank     = _ nl
nl        = "\\n" / !~"."s
_         = ~r"[ \\t]*"
''')

put('grammars/query.peg', r'''
# Filters over records: comparisons, flags, and, or, not, parentheses.
query     = _ disj
disj      = conj (kw_or conj)*
conj      = neg (kw_and neg)*
neg       = (kw_not neg) / atom
atom      = group / cmp / flag
group     = "(" _ disj ")" _
cmp       = field op value
flag      = field !op
op        = ~r"<=|>=|!=|=|<|>|~" _
value     = (number / string) _
number    = ~r"-?[0-9]+"
string    = ~r'"[^"]*"'
field     = !keyword ~r"[a-z_]+" _
keyword   = ~r"(and|or|not)\b"
kw_or     = ~r"or\b" _
kw_and    = ~r"and\b" _
kw_not    = ~r"not\b" _
_         = ~r"\s*"
''')

put('grammars/greeting.peg', r'''
greeting = hello _ name punct?
hello    = ~"hello|hi"i
name     = ~r"[A-Z][a-z]+"
punct    = "!" / "."
_        = " "+
''')

put('grammars/quant.peg', r'''
row     = word{2} sep{1,} digit{,3} tail? &end rest
word    = ~"[a-z]+" " "
sep     = "-"
digit   = ~"[0-9]"
tail    = !"x" ~"[a-z]"
end     = ~"."s
rest    = ~r".*"s
''')

put('grammars/csv.peg', '''
file   = row*
row    = cell ("," cell)* "\\n"
cell   = quoted / bare
quoted = ~'"(?:[^"]|"")*"'
bare   = ~"[^,\\n]*"
''')

put('grammars/literals.peg', r'''
lits   = "tab\there" 'it\'s' "say \"hi\"" r"back\slash" u"café" "\x41" R"\n"
flags  = ~"[a-z]+"a ~" a  b "x ~"^x$"m ~"X"is
''')

put('grammars/alias.peg', '''
greeting   = salutation
salutation = "hi" / "hello"
''')

put('grammars/bad_precedence.peg', '''
expr = expr "+" num / num
num  = ~"[0-9]+"
''')

put('grammars/leftrec.peg', '''
expr = (expr "+" num) / num
num  = ~"[0-9]+"
''')

put('grammars/empty.peg', '''
# nothing but a comment
''')

put('grammars/bad_undefined.peg', '''
pair  = key "=" value
key   = ~"[a-z]+"
''')

put('grammars/bad_circular.peg', '''
a = b
b = c
c = a
''')

put('grammars/bad_mixed.peg', '''
a = "x" b"y"
''')

put('grammars/bad_missing_equals.peg', '''
greeting = "hi" name
name "bob"
''')

put('grammars/bad_syntax.peg', '''
greeting = "hi" name
name = = "bob"
''')

put('grammars/bad_regex.peg', '''
word = ~"[a-"
''')

# ------------------------------------------------------------------ inputs

put('inputs/calc.txt', '''1 + 2 * 3
(1 + 2) * 3
  10 - 4 - 3
-7 / 2
7 % -3
2 * (3 + 4) * 5 - 6 / 2
max(3, 9, 4) + min(8, 2)
abs(-12) * pow(2, 10)
100 / (5 - 5)
17 % (2 - 2)
sqrt(16)
pow(2)
1 +
2 3
()
-(-(-4))
''')

put('inputs/config.json', '''{
  "name": "inventory",
  "version": 3,
  "debug": false,
  "owners": ["ana", "bo\\u00e9", "chen"],
  "limits": {"items": 500, "per_page": -25, "nested": {"deep": [1, [2, [3, []]], {}]}},
  "notes": "line one\\nline \\"two\\"\\ttab \\/ slash \\ud83d\\ude00",
  "name": "renamed",
  "empty": null
}
''')
put('inputs/list.json', '[1, 2,3 , "four", true, null, [ ], { "k" : "v" }]\n')
put('inputs/trailing.json', '{"a": 1, "b": [1, 2,],}\n')
put('inputs/leading_zero.json', '{"port": 0800}\n')
put('inputs/unclosed.json', '{"a": [1, 2\n')

put('inputs/app.ini', '''; settings for the inventory service
[server]
host = 0.0.0.0
port=8080
  workers : 4

# logging
[logging]
level = INFO
file = /var/log/inventory.log
rotate = yes

[database]
url = postgres://inv@db.internal:5432/inventory
pool.size = 10
timeout =
[server]
port = 9090
''')
put('inputs/broken.ini', '''[main]
name = ok
this line has no separator
other = 1
''')
put('inputs/unclosed.ini', '''[main
a = 1
''')

put('inputs/people.csv', '''name,age,city,active,role
Asha,34,Pune,yes,engineer
Bram,27,Utrecht,no,designer
Chidi,45,Lagos,yes,manager
Dana,31,Pune,no,engineer
Eitan,52,Haifa,yes,engineer
Farah,23,Lahore,yes,intern
Goran,38,Split,no,manager
Hana,29,Osaka,yes,designer
''')
put('inputs/queries.txt', '''age > 30
city = "Pune"
active
not active
age >= 30 and role = "engineer"
role = "designer" or role = "intern"
active and (city = "Pune" or age < 25)
not (age < 30 or age > 40)
name ~ "an"
city != "Pune" and not active
salary > 10
age > "old"
age >
ages = 3
and = 3
role="manager"or age<24
''')

put('inputs/greet_ok.txt', 'Hello World!')
put('inputs/greet_two.txt', 'hi  Ada')
put('inputs/greet_lower.txt', 'hello world')
put('inputs/greet_extra.txt', 'hello Bob!!')
put('inputs/greet_more.txt', 'HI Ada and more')
put('inputs/quant.txt', 'ab cd ---42z tail\nend')
put('inputs/quant_x.txt', 'ab cd -1234x')
put('inputs/sum.txt', '1+2+3')
put('inputs/rows.csv', 'id,name,"note, with comma"\n7,"say ""hi""",\n')
put('inputs/one_row.csv', 'a,"b",c\n')
put('inputs/lits.txt', 'tab\thereit\'ssay "hi"back\\slashcaféA\\n')
put('inputs/empty.txt', '')

jobs = [
    'rules',
    'grammar grammars/calc.peg',
    'grammar grammars/json.peg',
    'grammar grammars/ini.peg',
    'grammar grammars/query.peg',
    'grammar grammars/greeting.peg',
    'grammar grammars/quant.peg',
    'grammar grammars/csv.peg',
    'grammar grammars/literals.peg',
    'grammar grammars/alias.peg',
    'grammar grammars/leftrec.peg',
    'grammar grammars/bad_precedence.peg',
    'grammar grammars/empty.peg',
    'grammar grammars/bad_undefined.peg',
    'grammar grammars/bad_circular.peg',
    'grammar grammars/bad_mixed.peg',
    'grammar grammars/bad_missing_equals.peg',
    'grammar grammars/bad_syntax.peg',
    'grammar grammars/bad_regex.peg',
    'tree grammars/greeting.peg inputs/greet_ok.txt',
    'tree grammars/greeting.peg inputs/greet_two.txt',
    'tree grammars/greeting.peg inputs/greet_lower.txt',
    'tree grammars/greeting.peg inputs/greet_extra.txt',
    'tree grammars/greeting.peg inputs/empty.txt',
    'match grammars/greeting.peg inputs/greet_more.txt',
    'match grammars/greeting.peg inputs/greet_lower.txt',
    'tree grammars/quant.peg inputs/quant.txt',
    'tree grammars/quant.peg inputs/quant_x.txt',
    'tree grammars/csv.peg inputs/rows.csv',
    'tree grammars/csv.peg inputs/one_row.csv row',
    'tree grammars/csv.peg inputs/rows.csv cell',
    'match grammars/csv.peg inputs/rows.csv cell',
    'tree grammars/literals.peg inputs/lits.txt',
    'tree grammars/alias.peg inputs/greet_two.txt',
    'tree grammars/leftrec.peg inputs/sum.txt',
    'tree grammars/leftrec.peg inputs/sum.txt num',
    'tree grammars/empty.peg inputs/sum.txt',
    '!calc inputs/calc.txt',
    '!json inputs/config.json',
    '!json inputs/list.json',
    '!json inputs/trailing.json',
    '!json inputs/leading_zero.json',
    '!json inputs/unclosed.json',
    '!ini inputs/app.ini',
    '!ini inputs/broken.ini',
    '!ini inputs/unclosed.ini',
    '!query inputs/people.csv inputs/queries.txt',
]
with open(D + '/jobs.txt', 'w') as f:
    f.write('\n'.join(jobs) + '\n')
with open(D + '/files.txt', 'w') as f:
    f.write('\n'.join(files) + '\n')
print(len(files), 'files,', len(jobs), 'jobs')

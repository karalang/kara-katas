# Writes the m4 inputs into data/ and the jobs into data/jobs.txt.
import os
os.makedirs("data/lib", exist_ok=True)
files = {}

files["basics.m4"] = r"""dnl basics.m4: defining macros and calling them
define(`hello', `Hello, $1!')dnl
hello(`world')
hello
define(`swap', `$2 $1')swap(a, b) swap(`a,b', c)
define(`count', `$#')count count() count(a) count(a,b,c) count((a,b),c)
define(`all', `[$*] [$@]')all(`x', y, `z,w')
define(`tenth', `$10 $11')tenth(a,b,c,d,e,f,g,h,i,j)
define(`me', `I am `$0'')me
define(`spaces', `[$1][$2]')spaces(   leading,
	tabs and newlines   , too)
`quoted text is not expanded: hello'
``nested' quotes' `'
define(`exch', `$2, $1')dnl
define(exch(`expansion text', `macro'))dnl
macro
undefine(`macro')macro
ifdef(`hello', `hello is defined', `hello is not defined')
ifdef(`nothing', `yes', `no')
ifelse(`a', `a', `same', `different') ifelse(`a', `b', `same', `different')
ifelse(`x', `y', `one', `x', `x', `two', `three')
ifelse(`only a comment')
define(`sign', `ifelse(eval(`$1 < 0'), 1, `negative', `$1', 0, `zero', `positive')')dnl
sign(-5) sign(0) sign(7)
pushdef(`level', `one')pushdef(`level', `two')level popdef(`level')level popdef(`level')level
define(`reverse', `ifelse(`$#', `0', , `$#', `1', ``$1'',
  `reverse(shift($@)), `$1'')')dnl
reverse(a, b, c, d)
shift(a, b, c) shift(a)
define(`fact', `ifelse(eval(`$1 <= 1'), 1, 1, `eval($1 * fact(decr($1)))')')dnl
fact(10)
indir(`hello', `indir')
define(`x-y', `odd name')indir(`x-y')
builtin(`len', `abcd')
define(`len', `my `len'')len(`abc') builtin(`len', `abc')
undefine(`len')len(`abc')
line __line__ of __file__ by __program__
define(`plain')[plain] define(`twice', `$1$1')twice(`ab')
dumpdef(`swap', `hello', `defn')dnl
define(`saved', defn(`swap'))saved(1, 2)
define(`deep', `$1$2')deep(define(`inner', `in')inner, `side')
"""

files["text.m4"] = r"""dnl text.m4: the string builtins
len(`hello world') len() len(`a,b')
index(`gnus, gnats, and armadillos', `nat') index(`abc', `x') index(`abc', `')
substr(`gnus, gnats, and armadillos', `6') substr(`gnus, gnats', `6', `5') substr(`abc', `5') substr(`abc', `1', `-1')
translit(`GNUs not Unix', `A-Z') translit(`GNUs not Unix', `a-z', `A-Z')
translit(`hello', `lo', `01') translit(`abcdef', `a-f', `fedcba') translit(`hello', `l-l')
incr(41) decr(0) incr(-1) incr(` 7')
define(`upcase', `translit(`$*', `a-z', `A-Z')')dnl
define(`downcase', `translit(`$*', `A-Z', `a-z')')dnl
define(`capitalize1',
  `regexp(`$1', `^\(\w\)\(\w*\)', `upcase(`\1')`'downcase(`\2')')')dnl
define(`capitalize', `patsubst(`$1', `\w+', `capitalize1(`\&')')')dnl
capitalize(`GNUs not unix, alpha BETA')
patsubst(`hello world', `o', `0') patsubst(`hello world', `o')
patsubst(`  trim me  ', `^ +\| +$')|
patsubst(`abc', `', `-') patsubst(`a,b,,c', `,', `;')
patsubst(`xaby', `\(a\)\(b\)', `\2\1') patsubst(`ab', `a\|ab', `[\&]')
patsubst(`one two  three', ` +', `_') patsubst(`a.b.c', `\.', `\\')
regexp(`GNUs not Unix', `\<[a-z]\w+') regexp(`GNUs not Unix', `\<Q\w*')
regexp(`GNUs not Unix', `\w\(\w+\)$', `*** \& *** \1 ***')
regexp(`GNUs not Unix', `\<Q\w*', `nothing')|
regexp(`version 1.4.19', `\([0-9]+\)\.\([0-9]+\)\.\([0-9]+\)', `major \1, minor \2, patch \3')
regexp(`key = value', `^\([a-z]+\) *= *\(.*\)$', `\2 for \1')
regexp(`abc', `[[:upper:]]') regexp(`aBc', `[[:upper:]]') regexp(`a+b', `a+b') regexp(`a+b', `a\+b')
define(`html_escape',
  `patsubst(patsubst(patsubst(`$1', `&', `&amp;'), `<', `&lt;'), `>', `&gt;')')dnl
html_escape(`if (a < b && c > d)')
format(`%s has %d items, %5d|%-5d|%05d|%+d', `cart', 3, 42, 42, 42, 42)
format(`%x %X %o %c %%', 255, 255, 8, 65)
format(`[%10s] [%-10s] [%.3s] [%*d]', `right', `left', `truncate', 6, 7)
format(`%d%%', 50) format(`no args')
define(`csv_quote', `"patsubst(`$1', `"', `""')"')dnl
csv_quote(`say "hi"')
define(`indent', `patsubst(`$1', `^', `    ')')dnl
indent(`line one
line two')
patsubst(`a
b', `$', `;') patsubst(`a
b', `a.b', `X') patsubst(`a
b', `a[^x]b', `X')
patsubst(`*ab', `*a', `X') patsubst(`a{2}', `a{2}', `X') patsubst(`ab^c', `b^c', `X') patsubst(`a\b', `[\]', `X')
patsubst(`hello', `l*', `-') patsubst(`foo bar', `\Bo', `0') patsubst(`ab', `\(a\)\|b', `[\1]') regexp(`abc', `b\|')
"""

files["eval.m4"] = r"""dnl eval.m4: integer arithmetic
eval(`1 + 2 * 3') eval(`(1 + 2) * 3') eval(`-7 / 2') eval(`-7 % 2') eval(`7 % -2')
eval(`2 ** 10') eval(`2 ** 3 ** 2') eval(`-2 ** 2') eval(`2 ** 0')
eval(`1 << 31') eval(`0x7fffffff + 1') eval(`-1 >> 1') eval(`1 << 33')
eval(`010 + 0b101 + 0x1f') eval(`0r36:zz') eval(`0r2:1010')
eval(`1 < 2') eval(`1 > 2') eval(`3 <= 3') eval(`3 >= 4') eval(`1 == 1') eval(`1 != 1')
eval(`5 > 3 && 2 > 1') eval(`0 || 0') eval(`!0') eval(`!5') eval(`~0') eval(`- -3')
eval(`6 & 3') eval(`6 | 3') eval(`6 ^ 3') eval(`1 ? 2 : 3') eval(`0 ? 2 : 3')
eval(`0 && 1 / 0') eval(`1 || 1 / 0')
eval(255, 16) eval(255, 2) eval(`-255', 16) eval(10, 10, 5) eval(`-10', 10, 5) eval(35, 36)
eval(6 & 3, 2, 8) eval(0, 2, 4) eval(`1') eval() eval(`  42  ')
define(`max', `ifelse(eval(`$1 > $2'), 1, `$1', `$2')')max(3, 8) max(9, 4)
define(`fib', `ifelse(eval(`$1 < 2'), 1, `$1', `eval(fib(decr($1)) + fib(eval($1 - 2)))')')dnl
fib(15)
define(`sum', `ifelse(`$#', `1', `$1', `eval(`$1 + 'sum(shift($@)))')')dnl
sum(1, 2, 3, 4, 5)
"""

files["loops.m4"] = r"""divert(`-1')
# forloop(var, from, to, stmt): the version from the GNU m4 manual
define(`forloop', `ifelse(eval(`($2) <= ($3)'), `1',
  `pushdef(`$1')_$0(`$1', eval(`$2'), eval(`$3'), `$4')popdef(`$1')')')
define(`_forloop',
  `define(`$1', `$2')$4`'ifelse(`$2', `$3', `',
    `$0(`$1', incr(`$2'), `$3', `$4')')')
# quoting helpers
define(`quote', `ifelse(`$#', `0', `', ``$*'')')
define(`dquote', ``$@'')
define(`dquote_elt', `ifelse(`$#', `0', `', `$#', `1', ```$1''',
  ```$1'',$0(shift($@))')')
# foreach(var, (list), stmt)
define(`foreach', `pushdef(`$1')_$0(`$1',
  (dquote(dquote_elt$2)), `$3')popdef(`$1')')
define(`_arg1', `$1')
define(`_foreach', `ifelse(`$2', `(`')', `',
  `define(`$1', _arg1$2)$3`'$0(`$1', (dquote(shift$2)), `$3')')')
# joinall(sep, args): the arguments with sep between them
define(`joinall', `ifelse(`$#', `1', `', `$#', `2', ``$2'',
  ``$2'$1$0(`$1', shift(shift($@)))')')
divert`'dnl
forloop(`i', `1', `8', `i ')
forloop(`i', `1', `3', `forloop(`j', `1', `3', `(i,j) ')
')dnl
forloop(`i', `5', `1', `never')
foreach(`x', `(foo, bar, baz)', `x-')
foreach(`x', `(`a, b', `c')', `[x]')
foreach(`x', `()', `<x>')
joinall(`, ', `one', `two', `three')
define(`squares', `forloop(`n', 1, $1, `n^2 = eval(n**2)
')')dnl
squares(5)dnl
define(`html_table', `<table>
foreach(`row', `($@)', `  <tr><td>row</td><td>len(row)</td></tr>
')</table>')dnl
html_table(`apple', `kiwi', `banana')
"""

files["divert.m4"] = r"""divert(1)this goes to diversion 1
divert(2)this goes to diversion 2
divert(0)dnl
start divnum
undivert(2)dnl
divert(3)three: divnum
divert(-1)this is discarded
define(`later', `defined while discarding')
divert`'dnl
after: later
m4wrap(`wrapped one
')m4wrap(`wrapped two
')dnl
divert(4)four
undivert(1)dnl
divert`'dnl
divert(1)one again
divert`'dnl
undivert(9)undivert(-1)dnl
end of the file
"""

files["site.m4"] = r"""include(`lib/common.m4')dnl
# nginx.conf for ENV, generated by m4 -- comments are not expanded: WORKERS
worker_processes WORKERS;
events { worker_connections CONNECTIONS; }
http {
SERVER(`80', `example.com')
SERVER(`8080', `api.example.com', `    location / { proxy_pass http://127.0.0.1:9000; }
')
ifdef(`EXTRA', `    include EXTRA;
')dnl
}
sinclude(`lib/local.m4')dnl
sinclude(`lib/missing.m4')dnl
"""

files["lib/common.m4"] = r"""divert(-1)
ifdef(`WORKERS', , `define(`WORKERS', `2')')
ifdef(`ENV', , `define(`ENV', `dev')')
define(`CONNECTIONS', `ifelse(ENV, `prod', `4096', `256')')
define(`SERVER', `    server {
        listen $1;
        server_name $2;
ifelse(ENV, `prod', `        ssl_certificate /etc/ssl/$2.pem;
')dnl
        root /srv/$2;
$3dnl
    }')
divert`'dnl
"""

files["lib/local.m4"] = r"""# local overrides: file __file__, line __line__
"""

files["quotes.m4"] = r"""dnl quotes.m4: changing the quotes and the comment delimiters
define(`hello', `Hello')dnl
# a comment: hello(`no expansion')
define(`cmt', `# inside a body: hello')cmt
changecom(`/*', `*/')dnl
/* hello
   still a comment */ hello # now hello
changecom`'dnl
# hello without comments
changecom(`#')dnl
changequote(`[', `]')dnl
define([greet], [Hi $1])greet([there]) [hello] `hello'
changequote([<<], [>>])dnl
<<hello>> <<<<nested>>>> [hello] <<a,b>>
changequote`'dnl
`back to normal' hello
changequote(`{', `}')dnl
{a {nested} quote} hello {}
define({show}, {[$1] [$#]})show({x, y}) show(x, y)
changequote`'dnl
define(`dq', `"$1"')dq(`with, comma') dq(with, comma)
"""

files["errors.m4"] = r"""dnl errors.m4: the warnings and errors m4 keeps going after
len(`a', `b')
index(`abc')
eval(`1 +')
eval(`1 / 0')
eval(`2 +* 3')
eval(`5 % 0')
eval(`1', `1')
eval(`1', `37')
incr(`abc')
substr(`abc', `x')
indir(`nosuch')
builtin(`nosuch')
include(`missing.m4')
sinclude(`missing.m4')ok
errprint(`custom message', `with two args
')dnl
regexp(`abc', `\(')
patsubst(`abc', `b', `\0\9')
undefined_name stays as it is
define()dnl
defn(`nosuch')
dnl(`x')
divert(`x')
after the errors
"""

files["eof.m4"] = r"""before
define(`broken', `this quote never closes
"""

files["eofarg.m4"] = r"""before
define(`broken', `x'
"""

files["exit.m4"] = r"""divert(1)diverted text
divert`'dnl
m4wrap(`wrapped
')dnl
visible
m4exit(`3')
not reached
"""

files["main.m4"] = r"""define(`VERSION', `1.2.3')dnl
first file, VERSION
"""
files["second.m4"] = r"""second file, VERSION, line __line__ of __file__
"""

for name, text in files.items():
    with open("data/" + name, "w") as f:
        f.write(text)

jobs = [
    "basics.m4",
    "text.m4",
    "eval.m4",
    "quotes.m4",
    "loops.m4",
    "divert.m4",
    "-DENV=prod -DWORKERS=8 -DEXTRA=mime.types site.m4",
    "site.m4",
    "-DENV=prod -UENV site.m4",
    "errors.m4",
    "eof.m4",
    "eofarg.m4",
    "exit.m4",
    "main.m4 second.m4",
    "-DVERSION=9 second.m4",
]
with open("data/jobs.txt", "w") as f:
    f.write("\n".join(jobs) + "\n")

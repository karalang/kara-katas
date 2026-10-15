dnl text.m4: the string builtins
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

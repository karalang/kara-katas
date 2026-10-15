dnl basics.m4: defining macros and calling them
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

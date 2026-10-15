dnl quotes.m4: changing the quotes and the comment delimiters
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

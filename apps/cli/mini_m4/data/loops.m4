divert(`-1')
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

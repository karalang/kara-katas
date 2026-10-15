dnl errors.m4: the warnings and errors m4 keeps going after
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

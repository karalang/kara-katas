dnl eval.m4: integer arithmetic
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

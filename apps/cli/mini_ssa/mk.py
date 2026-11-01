"""Writes data/ for mini_ssa: six programs in a three-address IR, and
data/jobs.txt with the jobs that analyse, optimize and run them.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)


def write(name, text):
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


# Integer arithmetic the way a front end lowers it: every value a local,
# every loop a back edge.
write("arith.ir", '''\
# Integer helpers, as a front end lowers them.

func gcd(a, b) {
entry:
  jmp test
test:
  z = b == 0
  br z, done, step
step:
  t = a % b
  a = b
  b = t
  jmp test
done:
  ret a
}

func pow(base, e) {
entry:
  r = 1
  jmp loop
loop:
  c = e > 0
  br c, body, done
body:
  odd = e & 1
  br odd, mul, sq
mul:
  r = r * base
  jmp sq
sq:
  base = base * base
  e = e >> 1
  jmp loop
done:
  ret r
}

func collatz(n) {
entry:
  steps = 0
  jmp head
head:
  one = n == 1
  br one, done, body
body:
  rem = n % 2
  br rem, odd, even
even:
  n = n / 2
  jmp next
odd:
  t = n * 3
  n = t + 1
  jmp next
next:
  steps = steps + 1
  jmp head
done:
  ret steps
}

func classify(n) {
entry:
  neg = n < 0
  br neg, negative, check
negative:
  r = -1
  jmp out
check:
  zero = n == 0
  br zero, isz, positive
isz:
  r = 0
  jmp out
positive:
  big = n > 100
  r = 1
  br big, huge, out
huge:
  r = 2
  jmp out
out:
  ret r
}

func isqrt(n) {
entry:
  lo = 0
  hi = n + 1
  jmp loop
loop:
  gap = hi - lo
  more = gap > 1
  br more, body, done
body:
  s = lo + hi
  mid = s / 2
  sq = mid * mid
  le = sq <= n
  br le, up, down
up:
  lo = mid
  jmp loop
down:
  hi = mid
  jmp loop
done:
  ret lo
}

func wrap() {
entry:
  big = 2147483647
  x = big + 1
  y = x - 1
  m = 65536 * 65536
  print x
  print y
  print m
  s = -7 / 2
  r = -7 % 2
  print s
  print r
  ret 0
}
''')

# What sparse conditional constant propagation sees that a plain constant
# folder does not: a branch on a known value, a loop whose variable never
# changes, and code only a constant branch reaches.
write("consts.ir", '''\
# Constants that only SCCP finds.

func flags(x) {
entry:
  debug = 0
  level = 3
  on = debug != 0
  br on, trace, work
trace:
  print 999
  level = 9
  jmp work
work:
  t = level * 4
  r = x + t
  ret r
}

func steady(n) {
entry:
  k = 1
  i = 0
  jmp loop
loop:
  c = i < n
  br c, body, done
body:
  odd = k != 1
  br odd, change, keep
change:
  k = k + 1
  jmp keep
keep:
  i = i + 1
  jmp loop
done:
  r = k * 10
  ret r
}

func table(sel) {
entry:
  a = 6
  b = 7
  p = a * b
  q = p - 2
  hit = q == 40
  br hit, yes, no
yes:
  r = sel + q
  jmp out
no:
  r = 0
  jmp out
out:
  ret r
}

func chain() {
entry:
  a = 2
  b = a
  c = b
  d = c * c
  e = d << 3
  f = e >> 1
  g = f ^ 5
  h = g | 1
  i = h & 255
  print i
  ret i
}

func zero_div(x) {
entry:
  z = 0
  big = x > 10
  br big, risky, safe
risky:
  q = x / z
  jmp safe
safe:
  ret x
}

func dead_end(x) {
entry:
  r = x * 2
  ret r
orphan:
  print 1
  jmp entry2
entry2:
  ret 0
}
''')

# Loops nested two deep, the shapes a dominator tree and a loop finder
# exist for.
write("loops.ir", '''\
# Loops, nested and in sequence.

func tri(n) {
entry:
  s = 0
  i = 1
  jmp head
head:
  c = i <= n
  br c, body, exit
body:
  s = s + i
  i = i + 1
  jmp head
exit:
  ret s
}

func grid(n) {
entry:
  total = 0
  i = 0
  jmp outer
outer:
  ci = i < n
  br ci, init, done
init:
  j = 0
  jmp inner
inner:
  cj = j < n
  br cj, cell, next
cell:
  p = i * j
  total = total + p
  j = j + 1
  jmp inner
next:
  i = i + 1
  jmp outer
done:
  ret total
}

func primes(n) {
entry:
  count = 0
  k = 2
  jmp outer
outer:
  more = k <= n
  br more, start, done
start:
  d = 2
  jmp trial
trial:
  dd = d * d
  past = dd > k
  br past, prime, test
test:
  m = k % d
  divides = m == 0
  br divides, composite, bump
bump:
  d = d + 1
  jmp trial
prime:
  count = count + 1
  jmp composite
composite:
  k = k + 1
  jmp outer
done:
  ret count
}

func fib(n) {
entry:
  a = 0
  b = 1
  i = 0
  jmp loop
loop:
  c = i < n
  br c, body, done
body:
  t = a + b
  a = b
  b = t
  i = i + 1
  jmp loop
done:
  ret a
}

func search(target) {
entry:
  i = 0
  found = -1
  jmp loop
loop:
  lim = i < 50
  br lim, body, done
body:
  sq = i * i
  hit = sq == target
  br hit, yes, step
yes:
  found = i
  jmp done
step:
  i = i + 1
  jmp loop
done:
  ret found
}

func two_phase(n) {
entry:
  i = 0
  acc = 0
  jmp up
up:
  cu = i < n
  br cu, upb, turn
upb:
  acc = acc + i
  i = i + 1
  jmp up
turn:
  jmp down
down:
  cd = i > 0
  br cd, downb, out
downb:
  i = i - 1
  acc = acc - 1
  jmp down
out:
  ret acc
}
''')

# The two programs every out-of-SSA pass is tested on: the swap problem
# (copies that must run in parallel) and the lost-copy problem (a value
# read after the loop that redefines it).
write("swap.ir", '''\
# Out-of-SSA hazards.

func swap(n) {
entry:
  a = 1
  b = 2
  i = 0
  jmp loop
loop:
  c = i < n
  br c, body, done
body:
  t = a
  a = b
  b = t
  i = i + 1
  jmp loop
done:
  r = a * 10
  r = r + b
  ret r
}

func lost(n) {
entry:
  x = 0
  jmp loop
loop:
  y = x
  x = x + 1
  c = x < n
  br c, loop, done
done:
  ret y
}

func rotate(n) {
entry:
  a = 1
  b = 2
  c = 3
  i = 0
  jmp loop
loop:
  go = i < n
  br go, body, done
body:
  t = a
  a = b
  b = c
  c = t
  i = i + 1
  jmp loop
done:
  r = a * 100
  s = b * 10
  r = r + s
  r = r + c
  ret r
}

func shuffle(n) {
entry:
  x = 5
  y = 9
  jmp loop
loop:
  print x
  t = x
  x = y
  y = t
  n = n - 1
  more = n > 0
  br more, loop, done
done:
  r = x - y
  ret r
}

func early(n) {
entry:
  v = 0
  jmp loop
loop:
  stop = n == 0
  br stop, done, step
step:
  v = v + n
  n = n - 1
  big = v > 20
  br big, done, loop
done:
  ret v
}
''')

# Calls, recursion and output: what the optimizer must leave alone.
write("calls.ir", '''\
# Calls and side effects.

func fact(n) {
entry:
  base = n <= 1
  br base, one, rec
one:
  ret 1
rec:
  m = n - 1
  r = call fact(m)
  p = n * r
  ret p
}

func fibr(n) {
entry:
  small = n < 2
  br small, leaf, rec
leaf:
  ret n
rec:
  a = n - 1
  b = n - 2
  x = call fibr(a)
  y = call fibr(b)
  s = x + y
  ret s
}

func even(n) {
entry:
  z = n == 0
  br z, yes, rec
yes:
  ret 1
rec:
  m = n - 1
  r = call odd(m)
  ret r
}

func odd(n) {
entry:
  z = n == 0
  br z, no, rec
no:
  ret 0
rec:
  m = n - 1
  r = call even(m)
  ret r
}

func ack(m, n) {
entry:
  mz = m == 0
  br mz, base, inner
base:
  r = n + 1
  ret r
inner:
  nz = n == 0
  br nz, down, both
down:
  m1 = m - 1
  r = call ack(m1, 1)
  ret r
both:
  n1 = n - 1
  t = call ack(m, n1)
  m1 = m - 1
  r = call ack(m1, t)
  ret r
}

func report(n) {
entry:
  i = 1
  jmp loop
loop:
  c = i <= n
  br c, body, done
body:
  f = call fact(i)
  print f
  i = i + 1
  jmp loop
done:
  unused = call fibr(10)
  call note(n)
  ret
}

func note(n) {
entry:
  k = n * 1000
  print k
  ret
}

func forever(n) {
entry:
  jmp loop
loop:
  n = n + 1
  jmp loop
}

func deep(n) {
entry:
  m = n + 1
  r = call deep(m)
  ret r
}
''')

# A program with the mistakes the analyses report: names read before any
# assignment reaches them, and dead stores.
write("warn.ir", '''\
# Names that may be read before they are set.

func maybe(c) {
entry:
  br c, set, skip
set:
  v = 10
  jmp skip
skip:
  r = v + 1
  ret r
}

func typo(n) {
entry:
  total = 0
  i = 0
  jmp loop
loop:
  go = i < n
  br go, body, done
body:
  totl = total + i
  i = i + 1
  jmp loop
done:
  ret totl
}

func stores(x) {
entry:
  a = x + 1
  a = x + 2
  b = a * 2
  b = 7
  c = b + a
  unused = c * c
  ret c
}
''')

PROGRAMS = ["arith.ir", "consts.ir", "loops.ir", "swap.ir", "calls.ir", "warn.ir"]

JOBS = []

# every analysis on a few functions
for f, fn in [("arith.ir", "gcd"), ("arith.ir", "collatz"), ("arith.ir", "classify"),
              ("loops.ir", "grid"), ("loops.ir", "primes"), ("loops.ir", "two_phase"),
              ("swap.ir", "lost"), ("swap.ir", "early")]:
    for mode in ["cfg", "dom", "live", "ssa", "opt", "out"]:
        JOBS.append(f"{mode} {f} {fn}")

for f, fn in [("arith.ir", "pow"), ("arith.ir", "isqrt"), ("arith.ir", "wrap"),
              ("consts.ir", "flags"), ("consts.ir", "steady"), ("consts.ir", "table"),
              ("consts.ir", "chain"), ("consts.ir", "zero_div"), ("consts.ir", "dead_end"),
              ("loops.ir", "tri"), ("loops.ir", "fib"), ("loops.ir", "search"),
              ("swap.ir", "swap"), ("swap.ir", "rotate"), ("swap.ir", "shuffle"),
              ("calls.ir", "fact"), ("calls.ir", "ack"), ("calls.ir", "report"),
              ("warn.ir", "maybe"), ("warn.ir", "typo"), ("warn.ir", "stores")]:
    for mode in ["ssa", "opt", "out"]:
        JOBS.append(f"{mode} {f} {fn}")

for f, fn in [("consts.ir", "dead_end"), ("calls.ir", "forever"), ("warn.ir", "typo")]:
    JOBS.append(f"cfg {f} {fn}")
    JOBS.append(f"live {f} {fn}")
JOBS.append("dom calls.ir ack")
JOBS.append("dom swap.ir shuffle")

RUNS = [
    ("arith.ir", "gcd 1071 462"), ("arith.ir", "gcd 17 5"), ("arith.ir", "gcd 0 9"),
    ("arith.ir", "pow 3 13"), ("arith.ir", "pow 2 31"), ("arith.ir", "pow 7 0"),
    ("arith.ir", "collatz 27"), ("arith.ir", "collatz 1"),
    ("arith.ir", "classify -5"), ("arith.ir", "classify 0"), ("arith.ir", "classify 42"),
    ("arith.ir", "classify 1000"),
    ("arith.ir", "isqrt 0"), ("arith.ir", "isqrt 99"), ("arith.ir", "isqrt 100"),
    ("arith.ir", "isqrt 123456"), ("arith.ir", "wrap"),
    ("consts.ir", "flags 5"), ("consts.ir", "steady 9"), ("consts.ir", "table 1"),
    ("consts.ir", "chain"), ("consts.ir", "zero_div 3"), ("consts.ir", "zero_div 30"),
    ("consts.ir", "dead_end 21"),
    ("loops.ir", "tri 100"), ("loops.ir", "tri 0"), ("loops.ir", "grid 7"),
    ("loops.ir", "primes 100"), ("loops.ir", "primes 2"), ("loops.ir", "fib 30"),
    ("loops.ir", "fib 50"), ("loops.ir", "search 1764"), ("loops.ir", "search 50"),
    ("loops.ir", "two_phase 10"),
    ("swap.ir", "swap 0"), ("swap.ir", "swap 1"), ("swap.ir", "swap 7"),
    ("swap.ir", "lost 5"), ("swap.ir", "lost 1"), ("swap.ir", "rotate 4"),
    ("swap.ir", "rotate 5"), ("swap.ir", "shuffle 3"), ("swap.ir", "early 4"),
    ("swap.ir", "early 9"),
    ("calls.ir", "fact 10"), ("calls.ir", "fact 13"), ("calls.ir", "fibr 15"),
    ("calls.ir", "even 7"), ("calls.ir", "odd 7"), ("calls.ir", "ack 2 3"),
    ("calls.ir", "report 5"), ("calls.ir", "forever 0"), ("calls.ir", "deep 0"),
    ("calls.ir", "fact"), ("calls.ir", "nosuch 1"),
    ("warn.ir", "maybe 1"), ("warn.ir", "maybe 0"), ("warn.ir", "typo 4"),
    ("warn.ir", "stores 3"),
]
for f, args in RUNS:
    JOBS.append(f"run {f} {args}")

# one-line programs: \\n separates lines; ` ;; ` starts the job's arguments
SNIPS = [
    # analyses of tiny shapes
    r"cfg func f() {\nentry:\n  ret 1\n}",
    r"dom func f(c) {\nentry:\n  br c, a, b\na:\n  jmp j\nb:\n  jmp j\nj:\n  ret c\n}",
    r"dom func f(n) {\nentry:\n  jmp l\nl:\n  n = n - 1\n  br n, l, x\nx:\n  ret n\n}",
    r"ssa func f(c) {\nentry:\n  x = 1\n  br c, a, j\na:\n  x = 2\n  jmp j\nj:\n  ret x\n}",
    r"opt func f(c) {\nentry:\n  x = 1\n  br c, a, j\na:\n  x = 1\n  jmp j\nj:\n  ret x\n}",
    r"opt func f() {\nentry:\n  x = 10\n  y = x / 3\n  z = x % 3\n  w = y * z\n  ret w\n}",
    r"opt func f(a) {\nentry:\n  x = a\n  y = x\n  z = y + 0\n  ret z\n}",
    r"opt func f(a) {\nentry:\n  x = a * 3\n  y = a * 4\n  ret x\n}",
    r"opt func f(a) {\nentry:\n  x = a / 0\n  ret 1\n}",
    r"opt func f(a) {\nentry:\n  jmp b\nb:\n  jmp c\nc:\n  jmp d\nd:\n  ret a\n}",
    r"opt func f(a) {\nentry:\n  br a, x, x\nx:\n  ret a\n}",
    r"out func f(a) {\nentry:\n  br a, x, x\nx:\n  ret a\n}",
    r"out func f(n) {\nentry:\n  a = 0\n  b = 1\n  jmp l\nl:\n  t = a\n  a = b\n  b = t\n  n = n - 1\n  br n, l, x\nx:\n  ret a\n}",
    r"opt func f() {\nentry:\n  x = 2147483647\n  y = x * 2\n  z = y >> 31\n  ret z\n}",
    r"opt func f() {\nentry:\n  x = -2147483648\n  y = x / -1\n  ret y\n}",
    r"opt func f() {\nentry:\n  a = 5 < 3\n  b = 5 >= 3\n  c = a == b\n  d = a != b\n  e = 1 << 40\n  print a\n  print b\n  print c\n  print d\n  print e\n  ret\n}",
    r"live func f(a) {\nentry:\n  b = a + c\n  ret b\n}",
    r"ssa func f(a) {\nentry:\n  b = a + c\n  ret b\n}",
    r"run func f(a) {\nentry:\n  b = a + c\n  ret b\n} ;; f 4",
    r"run func f() {\nentry:\n  x = 1 / 0\n  ret x\n} ;; f",
    r"run func f(a, b) {\nentry:\n  q = a / b\n  r = a % b\n  print q\n  print r\n  ret\n} ;; f -17 5",
    r"run func f(a) {\nentry:\n  x = a + 1\n  ret x\n} ;; f 2147483647",
    r"run func f() {\nentry:\n  ret\n}\nfunc g() {\nentry:\n  call f()\n  ret 3\n} ;; g",
    r"cfg func f() {\nentry:\n  ret\n} ;; g",
    # parse errors
    r"cfg ret 1",
    r"cfg func f( {\nentry:\n  ret\n}",
    r"cfg func f(a b) {\nentry:\n  ret\n}",
    r"cfg func f() {\n  ret\n}",
    r"cfg func f() {\nentry:\n  ret\n  ret\n}",
    r"cfg func f() {\nentry:\n  x = 1\n}",
    r"cfg func f() {\nentry:\n  jmp nowhere\n}",
    r"cfg func f() {\nentry:\n  jmp entry\n}",
    r"cfg func f() {\nentry:\n  ret\nentry:\n  ret\n}",
    r"cfg func f() {\nentry:\n  ret\n}\nfunc f() {\nentry:\n  ret\n}",
    r"cfg func f() {\n}",
    r"cfg func f() {\nentry:\n  ret\n",
    r"cfg func f() {\nentry:\n  x = 1 ** 2\n  ret\n}",
    r"cfg func f() {\nentry:\n  x = y z\n  ret\n}",
    r"cfg func f() {\nentry:\n  x.0 = 1\n  ret\n}",
    r"cfg func f() {\nentry:\n  x = 1 + 2a\n  ret\n}",
    r"cfg func f() {\nentry:\n  print 1 2\n  ret\n}",
    r"cfg func f() {\nentry:\n  br 1, a\na:\n  ret\n}",
    r"cfg func f() {\nentry:\n  jmp\n}",
    r"cfg func f() {\nentry:\n  ret 1 2\n}",
    r"cfg func f() {\nentry:\n  x = call g(1)\n  ret\n}",
    r"cfg func g(a) {\nentry:\n  ret a\n}\nfunc f() {\nentry:\n  x = call g(1, 2)\n  ret\n}",
    r"cfg func f() {\nentry:\n  x = call g 1\n  ret\n}",
    r"cfg func f() {\nentry:\n  frob x\n  ret\n}",
    r"cfg func f() {\nentry:\n  ret\n9lbl:\n  ret\n}",
    r"cfg func f() {\nentry:  # a comment\n  ret   # and another\n}  # trailing",
]
for s in SNIPS:
    JOBS.append("snip " + s)

with open(os.path.join("data", "jobs.txt"), "w", encoding="utf-8", newline="") as fh:
    fh.write("\n".join(JOBS) + "\n")
print(f"{len(PROGRAMS)} programs, {len(JOBS)} jobs")

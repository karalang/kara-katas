"""Writes data/ for mini_regalloc: six programs in mini_ssa's three-address
IR, and data/jobs.txt with the jobs that select instructions for them,
allocate registers and run the result.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)


def write(name, text):
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


# Four programs from mini_ssa: integer helpers, loops, the out-of-SSA
# shapes and calls.
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

# Register pressure: more values live at once than there are registers.
write("pressure.ir", '''\
# More live values than registers.

func spread(x) {
entry:
  a = x * 3
  b = x * 5
  c = x * 7
  d = x * 11
  e = x * 13
  f = x * 17
  g = x * 19
  h = x * 23
  s = a + b
  s = s + c
  s = s + d
  s = s + e
  s = s + f
  s = s + g
  s = s + h
  p = a * h
  q = b * g
  r = c * f
  t = d * e
  u = p - q
  u = u + r
  u = u - t
  v = s ^ u
  ret v
}

func accum(n) {
entry:
  s0 = 0
  s1 = 0
  s2 = 0
  s3 = 0
  s4 = 0
  s5 = 0
  i = 0
  jmp loop
loop:
  c = i < n
  br c, body, done
body:
  s0 = s0 + i
  t = i * i
  s1 = s1 + t
  t = t * i
  s2 = s2 ^ t
  s3 = s3 + 1
  s4 = s4 - i
  m = i & 3
  s5 = s5 + m
  i = i + 1
  jmp loop
done:
  print s0
  print s1
  print s2
  print s3
  print s4
  print s5
  r = s0 + s1
  r = r + s2
  r = r + s3
  r = r + s4
  r = r + s5
  ret r
}

func matfib(n) {
entry:
  a = 1
  b = 1
  c = 1
  d = 0
  ra = 1
  rb = 0
  rc = 0
  rd = 1
  jmp loop
loop:
  more = n > 0
  br more, body, done
body:
  odd = n & 1
  br odd, mul, square
mul:
  t1 = ra * a
  t2 = rb * c
  na = t1 + t2
  t1 = ra * b
  t2 = rb * d
  nb = t1 + t2
  t1 = rc * a
  t2 = rd * c
  nc = t1 + t2
  t1 = rc * b
  t2 = rd * d
  nd = t1 + t2
  ra = na
  rb = nb
  rc = nc
  rd = nd
  jmp square
square:
  t1 = a * a
  t2 = b * c
  na = t1 + t2
  t1 = a * b
  t2 = b * d
  nb = t1 + t2
  t1 = c * a
  t2 = d * c
  nc = t1 + t2
  t1 = c * b
  t2 = d * d
  nd = t1 + t2
  a = na
  b = nb
  c = nc
  d = nd
  n = n >> 1
  jmp loop
done:
  ret rb
}

func sq(x) {
entry:
  y = x * x
  ret y
}

func around(n) {
entry:
  a = n + 1
  b = n + 2
  c = n + 3
  d = n + 4
  e = call sq(a)
  f = call sq(b)
  g = call sq(c)
  h = call sq(d)
  s = a + b
  s = s + c
  s = s + d
  s = s + e
  s = s + f
  s = s + g
  s = s + h
  ret s
}

func checksum(n) {
entry:
  h = 5381
  k = 0
  jmp loop
loop:
  c = k < n
  br c, body, done
body:
  x = k * 31
  y = x ^ k
  z = h << 5
  h = z + h
  h = h + y
  w = h >> 7
  h = h ^ w
  k = k + 1
  jmp loop
done:
  print h
  ret h
}
''')

# The calling convention: four argument registers, a result in a0, and
# every register clobbered by a call.
write("abi.ir", '''\
# Arguments, results and values live across calls.

func add4(a, b, c, d) {
entry:
  s = a + b
  s = s + c
  s = s + d
  ret s
}

func sub2(a, b) {
entry:
  r = a - b
  ret r
}

func mix(x, y) {
entry:
  p = call add4(x, y, 1, 2)
  q = call add4(p, x, y, p)
  r = call add4(q, q, q, q)
  ret r
}

func flip(a, b) {
entry:
  x = call sub2(b, a)
  y = call sub2(a, b)
  z = call sub2(x, y)
  ret z
}

func chain(n) {
entry:
  z = n == 0
  br z, base, rec
base:
  ret 0
rec:
  m = n - 1
  k = n * n
  r = call chain(m)
  s = r + k
  ret s
}

func gcdr(a, b) {
entry:
  z = b == 0
  br z, done, rec
done:
  ret a
rec:
  t = a % b
  r = call gcdr(b, t)
  ret r
}

func tally(n) {
entry:
  i = 0
  acc = 0
  jmp loop
loop:
  c = i < n
  br c, body, done
body:
  v = call add4(i, acc, 1, 0)
  print v
  acc = v
  i = i + 1
  jmp loop
done:
  ret acc
}

func noargs() {
entry:
  call tally(3)
  r = call mix(1, 2)
  ret r
}
''')

JOBS = []
SEL = [("arith.ir", "gcd"), ("arith.ir", "classify"), ("loops.ir", "grid"), ("swap.ir", "lost"),
       ("calls.ir", "ack"), ("pressure.ir", "accum"), ("abi.ir", "mix"), ("abi.ir", "chain")]
for f, fn in SEL:
    JOBS.append(f"sel {f} {fn}")
    JOBS.append(f"live {f} {fn}")
    JOBS.append(f"graph {f} {fn}")
ALLOC = [("arith.ir", "gcd"), ("arith.ir", "collatz"), ("arith.ir", "isqrt"), ("loops.ir", "grid"),
         ("loops.ir", "primes"), ("swap.ir", "swap"), ("swap.ir", "rotate"), ("calls.ir", "fibr"),
         ("calls.ir", "report"), ("pressure.ir", "spread"), ("pressure.ir", "accum"),
         ("pressure.ir", "matfib"), ("pressure.ir", "around"), ("abi.ir", "mix"),
         ("abi.ir", "flip"), ("abi.ir", "chain"), ("abi.ir", "tally")]
for f, fn in ALLOC:
    for how in ("linear", "colour"):
        JOBS.append(f"{how} {f} {fn} 3")
for f, fn in [("pressure.ir", "spread"), ("pressure.ir", "matfib"), ("loops.ir", "primes")]:
    for how in ("linear", "colour"):
        JOBS.append(f"{how} {f} {fn} 2")
        JOBS.append(f"{how} {f} {fn} 8")
for f, fn in [("arith.ir", "pow"), ("loops.ir", "grid"), ("loops.ir", "primes"), ("swap.ir", "rotate"),
              ("calls.ir", "ack"), ("pressure.ir", "spread"), ("pressure.ir", "accum"),
              ("pressure.ir", "matfib"), ("pressure.ir", "around"), ("pressure.ir", "checksum"),
              ("abi.ir", "mix"), ("abi.ir", "tally")]:
    JOBS.append(f"compare {f} {fn}")

RUNS = [
    ("arith.ir", "gcd", "1071 462"), ("arith.ir", "pow", "3 13"), ("arith.ir", "collatz", "27"),
    ("arith.ir", "classify", "-5"), ("arith.ir", "classify", "1000"), ("arith.ir", "isqrt", "123456"),
    ("arith.ir", "wrap", ""),
    ("loops.ir", "tri", "100"), ("loops.ir", "grid", "7"), ("loops.ir", "primes", "100"),
    ("loops.ir", "fib", "50"), ("loops.ir", "search", "1764"), ("loops.ir", "two_phase", "10"),
    ("swap.ir", "swap", "7"), ("swap.ir", "lost", "5"), ("swap.ir", "rotate", "5"),
    ("swap.ir", "shuffle", "3"), ("swap.ir", "early", "9"),
    ("calls.ir", "fact", "12"), ("calls.ir", "fibr", "15"), ("calls.ir", "even", "9"),
    ("calls.ir", "ack", "2 3"), ("calls.ir", "report", "5"), ("calls.ir", "deep", "0"),
    ("pressure.ir", "spread", "9"), ("pressure.ir", "spread", "-1000"), ("pressure.ir", "accum", "50"),
    ("pressure.ir", "matfib", "40"), ("pressure.ir", "matfib", "90"), ("pressure.ir", "around", "6"),
    ("pressure.ir", "checksum", "200"),
    ("abi.ir", "mix", "3 4"), ("abi.ir", "flip", "10 3"), ("abi.ir", "chain", "30"),
    ("abi.ir", "gcdr", "1071 462"), ("abi.ir", "tally", "5"), ("abi.ir", "noargs", ""),
]
for f, fn, args in RUNS:
    for K in (2, 4):
        JOBS.append(f"run {f} {fn} {K} {args}".rstrip())
for f, fn, args in [("pressure.ir", "spread", "9"), ("pressure.ir", "matfib", "40"),
                    ("abi.ir", "chain", "30"), ("loops.ir", "primes", "100")]:
    for K in (3, 6, 8):
        JOBS.append(f"run {f} {fn} {K} {args}")
JOBS.append("run calls.ir forever 4 0")
JOBS.append("run calls.ir fact 4")
JOBS.append("run calls.ir nosuch 4 1")

SNIPS = [
    r"sel func f(a) {\nentry:\n  x = a + 1\n  y = 1 + a\n  z = 1 - a\n  w = a * 4\n  v = 3 < a\n  u = a << 2\n  ret u\n}",
    r"sel func f() {\nentry:\n  x = 3 + 4\n  print 9\n  ret 7\n}",
    r"sel func f(c) {\nentry:\n  br c, a, b\na:\n  ret 1\nb:\n  ret 2\n}",
    r"sel func f(c) {\nentry:\n  br c, b, a\na:\n  ret 1\nb:\n  ret 2\n}",
    r"sel func f(c) {\nentry:\n  br c, a, a\na:\n  ret c\n}",
    r"sel func f(c) {\nentry:\n  br 1, a, b\nb:\n  ret 2\na:\n  ret 1\n}",
    r"sel func f() {\nentry:\n  ret\ndead:\n  print 1\n  ret\n}",
    r"sel func f(a) {\nentry:\n  b = a + c\n  ret b\n}",
    r"sel func g(a, b, c, d) {\nentry:\n  ret d\n}\nfunc f() {\nentry:\n  x = call g(4, 3, 2, 1)\n  call g(x, x, x, x)\n  ret x\n} ;; f",
    r"sel func g(a, b, c, d, e) {\nentry:\n  ret e\n}",
    r"sel func g(a, b, c, d, e) {\nentry:\n  ret a\n}\nfunc f() {\nentry:\n  x = call g(1, 2, 3, 4, 5)\n  ret x\n} ;; f",
    r"live func f(a) {\nentry:\n  x = a + 1\n  y = x + 1\n  z = y + 1\n  ret z\n}",
    r"graph func f(a) {\nentry:\n  x = a + 1\n  y = x + 1\n  z = y + 1\n  ret z\n}",
    r"graph func f(a, b) {\nentry:\n  x = a\n  y = x + b\n  ret y\n}",
    r"linear func f(a, b) {\nentry:\n  x = a\n  y = x + b\n  ret y\n} ;; f 2",
    r"colour func f(a, b) {\nentry:\n  x = a\n  y = x + b\n  ret y\n} ;; f 2",
    r"linear func f(a) {\nentry:\n  x = a + 1\n  y = a + 2\n  z = a + 3\n  s = x + y\n  s = s + z\n  ret s\n} ;; f 2",
    r"colour func f(a) {\nentry:\n  x = a + 1\n  y = a + 2\n  z = a + 3\n  s = x + y\n  s = s + z\n  ret s\n} ;; f 2",
    r"linear func f(a) {\nentry:\n  x = a + 1\n  y = a + 2\n  z = a + 3\n  s = x + y\n  s = s + z\n  ret s\n} ;; f 1",
    r"run func f(a) {\nentry:\n  x = a + 1\n  y = a + 2\n  z = a + 3\n  s = x + y\n  s = s + z\n  ret s\n} ;; f 1 10",
    r"run func f(a) {\nentry:\n  x = 1 / a\n  ret x\n} ;; f 2 0",
    r"run func f(a, b) {\nentry:\n  q = a / b\n  r = a % b\n  print q\n  print r\n  ret\n} ;; f 2 -17 5",
    r"run func f(c) {\nentry:\n  br c, set, skip\nset:\n  v = 10\n  jmp skip\nskip:\n  r = v + 1\n  ret r\n} ;; f 2 0",
    r"run func f(c) {\nentry:\n  br c, set, skip\nset:\n  v = 10\n  jmp skip\nskip:\n  r = v + 1\n  ret r\n} ;; f 2 1",
    r"run func f() {\nentry:\n  x = 2147483647\n  y = x + 1\n  ret y\n} ;; f 2",
    r"linear func f() {\nentry:\n  ret\n} ;; g 2",
    r"sel ret 1",
    r"sel func f() {\nentry:\n  jmp entry\n}",
    r"sel func f() {\nentry:\n  x = call g()\n  ret\n}",
]
for s in SNIPS:
    JOBS.append("snip " + s)

with open(os.path.join("data", "jobs.txt"), "w", encoding="utf-8", newline="") as fh:
    fh.write("\n".join(JOBS) + "\n")
print(f"6 programs, {len(JOBS)} jobs")

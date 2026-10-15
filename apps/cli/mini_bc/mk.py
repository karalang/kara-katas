# Writes data/: the bc scripts the run feeds to bc, one per job, and
# data/jobs.txt naming them in order.
import os
os.makedirs("data", exist_ok=True)
scripts = []
def w(name, text):
    open("data/" + name, "w").write(text)
    scripts.append(name)

w("loan.bc", """\
/* Monthly payment and amortization for a fixed-rate loan, the way a
   shell script asks bc for it. */
define round2(x) {
    auto s, r
    s = scale
    scale = 0
    if (x < 0) r = -((-x * 100 + .5) / 1) else r = (x * 100 + .5) / 1
    scale = s
    return (r / 100)
}

define payment(p, rate, years) {
    auto r, n
    r = rate / 1200
    n = years * 12
    return (p * r / (1 - (1 + r) ^ -n))
}

scale = 10
principal = 250000
rate = 6.5
m = payment(principal, rate, 30)
print "monthly payment: ", round2(m), "\\n"

balance = principal
total = 0
for (month = 1; month <= 3; month++) {
    interest = round2(balance * rate / 1200)
    toward = round2(m) - interest
    balance = balance - toward
    total += interest
    print "month ", month, ": interest ", interest, ", principal ", toward, ", balance ", balance, "\\n"
}
print "interest so far: ", total, "\\n"
print "total of 360 payments: ", round2(m) * 360, "\\n"
round2(-2.345)
round2(1.005)
""")

w("bigint.bc", """\
# Exact integer work: factorials, Fibonacci, powers and number theory.
define fact(n) {
    if (n <= 1) return (1)
    return (n * fact(n - 1))
}
define fib(n) {
    auto a, b, t, i
    a = 0
    b = 1
    for (i = 0; i < n; i++) {
        t = a + b
        a = b
        b = t
    }
    return (a)
}
define gcd(a, b) {
    auto t
    while (b != 0) {
        t = a % b
        a = b
        b = t
    }
    return (a)
}
define lcm(a, b) {
    return (a / gcd(a, b) * b)
}
define powmod(b, e, m) {
    auto r
    r = 1
    b = b % m
    while (e > 0) {
        if (e % 2 == 1) r = r * b % m
        b = b * b % m
        e = e / 2
    }
    return (r)
}
define digitsum(n) {
    auto s
    s = 0
    while (n > 0) {
        s += n % 10
        n /= 10
    }
    return (s)
}
fact(25)
fact(100)
fib(90)
fib(300)
2^256
2^64 - 1
-(3^100)
gcd(1071, 462)
lcm(4, 6) ; lcm(21, 6)
powmod(4, 13, 497)
powmod(2, 10007, 10007)
digitsum(fact(100))
length(fact(100))
length(2^1000)
for (p = 2; p < 60; p++) {
    prime = 1
    for (d = 2; d * d <= p; d++) {
        if (p % d == 0) { prime = 0; break }
    }
    if (prime) print p, " "
}
print "\\n"
""")

w("series.bc", """\
/* Constants from series, without the -l library. */
define arctan(x) {
    auto term, sum, k, x2, prev
    sum = x
    term = x
    x2 = x * x
    k = 1
    prev = 0
    while (sum != prev) {
        prev = sum
        term = -term * x2
        k += 2
        sum += term / k
    }
    return (sum)
}
define exp1() {
    auto term, sum, n
    sum = 1
    term = 1
    n = 0
    while (term > 0) {
        n += 1
        term = term / n
        sum += term
    }
    return (sum)
}
scale = 60
pi = 16 * arctan(1/5) - 4 * arctan(1/239)
scale = 50
pi / 1
e = exp1()
e
scale = 70
sqrt(2)
phi = (1 + sqrt(5)) / 2
phi
scale = 20
sqrt(10^40 + 1)
sqrt(.0004)
sqrt(123456789)
scale = 3
sqrt(2.00000)
22 / 7 - pi
""")

w("scale.bc", """\
# How scale decides the digits of each result.
scale
7 / 2
scale = 4
7 / 2
1 / 3 * 3
2 / 3
-7 / 3
0.5 * 0.25
1.25 * 1.25 * 1.25
123.456 * 1
1.000 + 2
3.14159 - 3.1
10 % 3
scale = 0
10 % 3
-10 % 3
10 % -3
7.5 % 2
scale = 2
7.5 % 2
1.5 ^ 3
.1 ^ 3
2 ^ -2
scale = 6
2 ^ -2
(-2) ^ 3
-2 ^ 2
x = 123.4500
length(x); scale(x)
length(.005); scale(.005)
length(0)
1.50
0.00
-0
007.10
.5 == 0.50
-1.5 < -1
3 > 2 > 1
a = 3 < 4
a
1 && 0 ; 2 || 0 ; !7 ; !0
n = 0
0 && (n = 5)
n
1 || (n = 6)
n
(m = 9)
m
c = 1.5
c++
c
++c
c--
--c
c += 2.25 ; c
c -= 1 ; c
c *= 3 ; c
c /= 2 ; c
c %= 2 ; c
c ^= 2 ; c
42
last + 1
. * 2
""")

w("bases.bc", """\
# Base conversion: obase for output, ibase for input.
obase = 16
255
-255
4096
3735928559
10.5
4096.0625
.5
0
obase = 2
10
5.75
2^20
obase = 8
511
obase = 60
3725
100000.5
.5
obase = 100
123456
5.5
obase = 1000
123456789
obase = 7
100
scale = 2
1 / 7
scale = 0
obase = 10
ibase = 16
FF
A
1A
FFFF + 1
.8
1.C
ibase = 2
101
1.1
.001
11111111
ibase = A
10
obase = 16
2^300
""")

w("functions.bc", """\
/* Functions: dynamic scope, arrays by value and by reference, void
   functions and recursion. */
x = 10
define f() { return (x * 2) }
define g(x) { return (f()) }
f()
g(3)
x
define h() {
    auto x
    x = 100
    return (f())
}
h()
define bump(x) {
    x = x + 1
    return (x)
}
bump(x)
x
a[0] = 1; a[1] = 2; a[2] = 3
define sum(v[], n) {
    auto i, t
    for (i = 0; i < n; i++) t += v[i]
    return (t)
}
sum(a[], 3)
define clobber(v[]) {
    v[0] = 99
    return (v[0])
}
clobber(a[])
a[0]
define setall(*v[], n, val) {
    auto i
    for (i = 0; i < n; i++) v[i] = val
}
setall(a[], 3, 7)
a[0] + a[1] + a[2]
define void greet(name) {
    print "hello, number ", name, "\\n"
}
greet(42)
define ack(m, n) {
    if (m == 0) return (n + 1)
    if (n == 0) return (ack(m - 1, 1))
    return (ack(m - 1, ack(m, n - 1)))
}
ack(2, 3)
define hanoi(n) {
    if (n == 0) return
    return (2 * hanoi(n - 1) + 1)
}
hanoi(10)
define noret() { y = 5 }
noret()
y
define counter() {
    auto i, s[]
    for (i = 0; i < 5; i++) s[i] = i * i
    return (s[4])
}
counter()
z[3]
define collatz(n) {
    auto steps
    while (n != 1) {
        if (n % 2 == 0) n /= 2 else n = 3 * n + 1
        steps += 1
    }
    return (steps)
}
collatz(27)
i = 0
while (1) {
    i += 1
    if (i == 3) continue
    if (i > 6) break
    print i, " "
}
print "\\n"
for (;;) { break }
for (j = 0; j < 3; j++) if (j == 1) print "one\\n" else print "not one\\n"
if (0) 5 else if (1) 6 else 7
""")

w("report.bc", """\
# A small invoice, formatted with print.
scale = 2
qty[0] = 3 ; price[0] = 19.99
qty[1] = 1 ; price[1] = 249.00
qty[2] = 12 ; price[2] = 0.35
"Invoice 2026-114
"
subtotal = 0
for (i = 0; i < 3; i++) {
    line = qty[i] * price[i]
    subtotal += line
    print "  item ", i + 1, ":\\t", qty[i], " x ", price[i], "\\t= ", line, "\\n"
}
tax = subtotal * 0.0825
print "subtotal\\t", subtotal, "\\ntax\\t\\t", tax, "\\ntotal\\t\\t", subtotal + tax, "\\n"
print "\\qquoted\\q and a backslash: \\\\\\n"
"a string statement keeps \\n as written\\n"
print "a long line: ", 2^200, "\\n"
"abc"; 2^300
""")

w("errors.bc", """\
1 + 2
3 +
4 + * 5
6
(7 + 8
x = 3 @ 2
y = 1; z = ; 9
y
10 )
define f(n) { return (n * 2) }
f(21
f(21)
11 # still running
if (0) quit
12
""")

open("data/jobs.txt", "w").write("".join(s + "\n" for s in scripts))

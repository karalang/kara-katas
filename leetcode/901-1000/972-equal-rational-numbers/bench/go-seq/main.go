// Benchmark: LeetCode #972 Equal Rational Numbers -- the ★ arm, both as
// fractions in lowest terms, on 1000 random pairs of strings. Mirrors
// is_rational_equal.kara, .c, .rs and .py.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func gcd(a, b int64) int64 {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}

func fraction(s string) (int64, int64) {
	var whole, rep, nines int64
	shift := int64(1)
	part := 0
	for i := 0; i < len(s); i++ {
		c := s[i]
		if c == '.' {
			part = 1
		} else if c == '(' {
			part = 2
		} else if c != ')' {
			d := int64(c - '0')
			if part == 2 {
				rep = rep*10 + d
				nines = nines*10 + 9
			} else {
				whole = whole*10 + d
				if part == 1 {
					shift *= 10
				}
			}
		}
	}
	num, den := whole, shift
	if nines != 0 {
		num, den = whole*nines+rep, shift*nines
	}
	g := gcd(num, den)
	return num / g, den / g
}

func isRationalEqual(s, t string) bool {
	a, da := fraction(s)
	b, db := fraction(t)
	return a == b && da == db
}

var seed int64 = 972

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type Num struct {
	Int      int64
	Non, Rep string
	Dot      bool
}

func digits(n int64) string {
	var b strings.Builder
	for i := int64(0); i < n; i++ {
		b.WriteByte(byte('0' + nextRandom()%10))
	}
	return b.String()
}

func text(x Num) string {
	s := strconv.FormatInt(x.Int, 10)
	if x.Dot || x.Non != "" || x.Rep != "" {
		s += "."
	}
	s += x.Non
	if x.Rep != "" {
		s += "(" + x.Rep + ")"
	}
	return s
}

func randomNum() Num {
	length := 1 + nextRandom()%4
	v := nextRandom() % 10
	for i := int64(1); i < length; i++ {
		v = v*10 + nextRandom()%10
	}
	non := digits(nextRandom() % 5)
	rep := ""
	if nextRandom()%3 != 0 {
		rep = digits(1 + nextRandom()%4)
	}
	return Num{v, non, rep, nextRandom()%2 == 0}
}

func variant(x Num) Num {
	y := x
	steps := 1 + nextRandom()%3
	for s := int64(0); s < steps; s++ {
		kind := nextRandom() % 7
		r := len(y.Rep)
		if kind == 0 && r > 0 && len(y.Non) < 4 {
			y.Non += y.Rep[:1]
			y.Rep = y.Rep[1:] + y.Rep[:1]
		} else if kind == 1 && r > 0 && 2*r <= 4 {
			y.Rep = y.Rep + y.Rep
		} else if kind == 2 && r == 0 && len(y.Non) < 4 {
			y.Non += "0"
		} else if kind == 3 && r == 0 {
			y.Rep = "0"
		} else if kind == 4 && r == 0 {
			if y.Non != "" && y.Non[len(y.Non)-1] != '0' {
				y.Non = y.Non[:len(y.Non)-1] + string(y.Non[len(y.Non)-1]-1)
				y.Rep = "9"
			} else if y.Non == "" && y.Int > 0 {
				y.Int--
				y.Rep = "9"
			}
		} else if kind == 5 && r > 0 && strings.Trim(y.Rep, "0") == "" {
			y.Rep = ""
			y.Dot = true
		} else if kind == 6 && r%2 == 0 && r > 0 && y.Rep[:r/2] == y.Rep[r/2:] {
			y.Rep = y.Rep[:r/2]
		}
	}
	return y
}

func nudge(s string) string {
	var places []int
	for i := 0; i < len(s); i++ {
		if s[i] >= '0' && s[i] <= '9' {
			places = append(places, i)
		}
	}
	at := places[nextRandom()%int64(len(places))]
	old := int64(s[at] - '0')
	nw := nextRandom() % 9
	if nw >= old {
		nw++
	}
	if at == 0 && nw == 0 && len(s) > 1 && s[1] >= '0' && s[1] <= '9' {
		nw = 1 + old%9
		if nw == old {
			nw = 9
		}
	}
	return s[:at] + strconv.FormatInt(nw, 10) + s[at+1:]
}

func randomPair(c int) (string, string) {
	x := randomNum()
	if c%3 == 0 {
		return text(x), text(variant(x))
	}
	if c%3 == 1 {
		y := text(variant(x))
		return text(x), nudge(y)
	}
	return text(x), text(randomNum())
}

func main() {
	rounds, count := 1000, 1000
	ss := make([]string, count)
	ts := make([]string, count)
	for c := 0; c < count; c++ {
		ss[c], ts[c] = randomPair(c)
	}
	equal, check := int64(0), int64(0)
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			k := (r + i) % count
			if isRationalEqual(ss[k], ts[k]) {
				equal++
				check = (check*2 + 1) % 1000000007
			} else {
				check = check * 2 % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over %d pairs: %d equal, checksum %d\n", rounds, count, equal, check)
}

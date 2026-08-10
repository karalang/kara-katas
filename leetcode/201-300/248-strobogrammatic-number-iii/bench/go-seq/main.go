// Benchmark workload for LeetCode #248 — Strobogrammatic Number III (Go mirror).
// Mirrors strobogrammatic_count.kara algorithm-for-algorithm.
package main

import (
	"fmt"
	"strconv"
)

var pairA = [5]string{"0", "1", "6", "8", "9"}
var pairB = [5]string{"0", "1", "9", "8", "6"}

func pow5(e int64) int64 {
	a := int64(1)
	for i := int64(0); i < e; i++ {
		a *= 5
	}
	return a
}

func countOfLength(l int64) int64 {
	if l <= 0 {
		return 0
	}
	if l == 1 {
		return 3
	}
	t := 4 * pow5(l/2-1)
	if l%2 == 1 {
		t *= 3
	}
	return t
}

func build(k, n int64) []string {
	out := []string{}
	if k == 0 {
		return append(out, "")
	}
	if k == 1 {
		return append(out, "0", "1", "8")
	}
	for _, s := range build(k-2, n) {
		for p := 0; p < 5; p++ {
			if pairA[p] == "0" && k == n {
				continue
			}
			out = append(out, pairA[p]+s+pairB[p])
		}
	}
	return out
}

func cmpDigits(a, b string) int64 {
	if len(a) != len(b) {
		if len(a) < len(b) {
			return -1
		}
		return 1
	}
	for i := 0; i < len(a); i++ {
		if a[i] != b[i] {
			if a[i] < b[i] {
				return -1
			}
			return 1
		}
	}
	return 0
}

func countBounded(l int64, low, high string, useLo, useHi bool) int64 {
	var n int64
	for _, s := range build(l, l) {
		keep := true
		if useLo && cmpDigits(s, low) < 0 {
			keep = false
		}
		if useHi && cmpDigits(s, high) > 0 {
			keep = false
		}
		if keep {
			n++
		}
	}
	return n
}

func countInRange(low, high string) int64 {
	ll, hl := int64(len(low)), int64(len(high))
	if ll > hl {
		return 0
	}
	if ll == hl {
		if cmpDigits(low, high) > 0 {
			return 0
		}
		return countBounded(ll, low, high, true, true)
	}
	total := countBounded(ll, low, high, true, false)
	total += countBounded(hl, low, high, false, true)
	for l := ll + 1; l < hl; l++ {
		total += countOfLength(l)
	}
	return total
}

func main() {
	var queries int64 = 1000
	var state int64 = 248248
	var sink int64 = 0

	for q := int64(0); q < queries; q++ {
		state = (state*1103515245 + 12345) & 2147483647
		da := (state/65536)%8 + 1
		state = (state*1103515245 + 12345) & 2147483647
		db := (state/65536)%8 + 1
		state = (state*1103515245 + 12345) & 2147483647
		ra := (state/65536)%9000 + 1
		state = (state*1103515245 + 12345) & 2147483647
		rb := (state/65536)%9000 + 1

		a := ra
		for i := int64(1); i < da; i++ {
			a = a*10%1000000000000000 + (i % 10)
		}
		b := rb
		for j := int64(1); j < db; j++ {
			b = b*10%1000000000000000 + (j % 10)
		}
		if a > b {
			a, b = b, a
		}

		sink = (sink + countInRange(strconv.FormatInt(a, 10), strconv.FormatInt(b, 10))) % 1000000007
	}
	fmt.Println(sink)
}

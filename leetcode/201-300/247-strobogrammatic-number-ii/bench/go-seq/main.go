// Benchmark workload for LeetCode #247 — Strobogrammatic Number II (Go mirror).
// Mirrors strobogrammatic_ii.kara algorithm-for-algorithm.
package main

import "fmt"

var pairA = [5]string{"0", "1", "6", "8", "9"}
var pairB = [5]string{"0", "1", "9", "8", "6"}

func build(k, n int64) []string {
	out := []string{}
	if k == 0 {
		return append(out, "")
	}
	if k == 1 {
		return append(out, "0", "1", "8")
	}
	inner := build(k-2, n)
	for _, s := range inner {
		for p := 0; p < 5; p++ {
			if k == n && pairA[p] == "0" {
				continue
			}
			out = append(out, pairA[p]+s+pairB[p])
		}
	}
	return out
}

func isStrobogrammatic(s string) bool {
	b := []byte(s)
	if len(b) == 0 {
		return true
	}
	lo, hi := 0, len(b)-1
	for lo <= hi {
		x, y := int64(b[lo]), int64(b[hi])
		ok := (x == 48 && y == 48) || (x == 49 && y == 49) || (x == 56 && y == 56) ||
			(x == 54 && y == 57) || (x == 57 && y == 54)
		if !ok {
			return false
		}
		lo++
		hi--
	}
	return true
}

func main() {
	var n int64 = 16
	var rounds int64 = 12
	var sink int64 = 0
	for r := int64(0); r < rounds; r++ {
		got := build(n, n)
		for _, s := range got {
			if isStrobogrammatic(s) {
				for _, c := range []byte(s) {
					sink = (sink*31 + int64(c)) % 1000000007
				}
			}
		}
	}
	fmt.Println(sink)
}

// Benchmark workload for LeetCode #263 — Ugly Number (Go mirror).
// Mirrors ugly_sweep.kara algorithm-for-algorithm.
package main

import (
	"fmt"
	"math"
)

func gcd(a, b int64) int64 {
	x, y := a, b
	for y != 0 {
		t := x % y
		x = y
		y = t
	}
	return x
}

func isUgly(n int64) bool {
	if n <= 0 {
		return false
	}
	m := n
	g := gcd(m, 30)
	for g > 1 {
		m /= g
		g = gcd(m, 30)
	}
	return m == 1
}

func main() {
	var n int64 = 10000000
	var limit int64 = math.MaxInt64

	ring := make([]int64, 0, 64)
	var rs int64 = 7717
	for k := 0; k < 64; k++ {
		var v int64 = 1
		for steps := int64(0); steps < 40; steps++ {
			rs = (rs*1103515245 + 12345) & 2147483647
			pick := (rs / 65536) % 3
			var f int64 = 2
			if pick == 1 {
				f = 3
			} else if pick == 2 {
				f = 5
			}
			if v <= limit/f {
				v *= f
			} else {
				steps = 40
			}
		}
		ring = append(ring, v)
	}

	var state int64 = 263263
	var uglies int64 = 0
	var digest int64 = 0
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		hi := state
		state = (state*1103515245 + 12345) & 2147483647
		probe := hi*2147483648 + state
		if i%512 == 0 {
			probe = ring[(i/512)%64]
		}
		var bit int64 = 0
		if isUgly(probe) {
			uglies++
			bit = 1
		}
		digest = (digest*131 + bit*7 + probe%1000003) % 1000000007
	}

	fmt.Println(uglies)
	fmt.Println(digest)
}

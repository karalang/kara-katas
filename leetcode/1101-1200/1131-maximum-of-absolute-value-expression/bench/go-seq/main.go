// LeetCode #1131: Maximum of Absolute Value Expression -- the bench in Go,
// the same algorithm and workload as max_abs_val_expr.kara: each array its
// own []int64, the same 8 pairs of 40000 values and 400 rounds.
package main

import (
	"fmt"
	"math"
)

func maxAbsValExpr(arr1, arr2 []int64) int64 {
	signs := [4][2]int64{{1, 1}, {1, -1}, {-1, 1}, {-1, -1}}
	var best int64
	for _, s := range signs {
		p, q := s[0], s[1]
		high := int64(math.MinInt64)
		low := int64(math.MaxInt64)
		for i := range arr1 {
			v := p*arr1[i] + q*arr2[i] + int64(i)
			if v > high {
				high = v
			}
			if v < low {
				low = v
			}
		}
		if high-low > best {
			best = high - low
		}
	}
	return best
}

var seed int64 = 1131

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func value() int64 {
	high := nextRandom()
	low := nextRandom()
	return (high*32768+low)%2000001 - 1000000
}

func main() {
	firsts := make([][]int64, 0, 8)
	seconds := make([][]int64, 0, 8)
	for j := 0; j < 8; j++ {
		a := make([]int64, 40000)
		for i := range a {
			a[i] = value()
		}
		b := make([]int64, 40000)
		for i := range b {
			b[i] = value()
		}
		firsts = append(firsts, a)
		seconds = append(seconds, b)
	}
	var total, check int64
	for round := int64(0); round < 400; round++ {
		for j := int64(0); j < 8; j++ {
			at := (round*7919 + j*104729) % 40000
			firsts[j][at] = ((firsts[j][at]+1000000)*7+12345)%2000001 - 1000000
			seconds[j][at] = ((seconds[j][at]+1000000)*11+54321)%2000001 - 1000000
			r := maxAbsValExpr(firsts[j], seconds[j])
			total += r
			check = (check*31 + r) % 1000000007
		}
	}
	fmt.Printf("400 rounds over 8 pairs of 40000 values: answers total %d, checksum %d\n", total, check)
}

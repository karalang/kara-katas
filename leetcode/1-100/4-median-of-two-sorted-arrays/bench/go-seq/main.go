// LeetCode 4 — binary-search-partition O(log min(m, n)) Median of Two
// Sorted Arrays, Go single-threaded mirror.
// Algorithmic peer of bench/binary_search_partition.{kara,rs,c,py}. Same
// M = N = 1_000_000, R = 1_000, K = 10_000_000 rotated-input workload.
// Stdout sink: 20_019_970_000_000.
//
// Idiomatic Go: two `[]int64` slices built once, `middlePairOff` called
// 10M times. math.MinInt64 / math.MaxInt64 stand in for the ±∞ sentinels
// (matches Kara/Rust's `i64.MIN` / `i64.MAX` choice; Python uses ±(1<<62)
// which is a different but workload-equivalent sentinel).
package main

import (
	"fmt"
	"math"
)

func middlePairOff(a []int64, aOff, aLen int64, b []int64, bOff, bLen int64) (int64, int64) {
	if aLen > bLen {
		return middlePairOff(b, bOff, bLen, a, aOff, aLen)
	}
	half := (aLen + bLen + 1) / 2
	lo, hi := int64(0), aLen
	for lo <= hi {
		i := (lo + hi) / 2
		j := half - i
		var leftA, rightA, leftB, rightB int64
		if i > 0 {
			leftA = a[aOff+i-1]
		} else {
			leftA = math.MinInt64
		}
		if i < aLen {
			rightA = a[aOff+i]
		} else {
			rightA = math.MaxInt64
		}
		if j > 0 {
			leftB = b[bOff+j-1]
		} else {
			leftB = math.MinInt64
		}
		if j < bLen {
			rightB = b[bOff+j]
		} else {
			rightB = math.MaxInt64
		}
		if leftA > rightB {
			hi = i - 1
		} else if leftB > rightA {
			lo = i + 1
		} else {
			lower := leftA
			if leftB > lower {
				lower = leftB
			}
			if (aLen+bLen)%2 == 1 {
				return lower, lower
			}
			upper := rightA
			if rightB < upper {
				upper = rightB
			}
			return lower, upper
		}
	}
	panic("unreachable")
}

func main() {
	const M = 1000000
	const N = 1000000
	const R = 1000
	const K = 10000000

	baseA := make([]int64, M+R)
	baseB := make([]int64, N+R)
	for p := int64(0); p < M+R; p++ {
		baseA[p] = 2 * p
	}
	for p := int64(0); p < N+R; p++ {
		baseB[p] = 2*p + 1
	}

	var sum int64
	for k := int64(0); k < K; k++ {
		off := k % R
		lower, upper := middlePairOff(baseA, off, M, baseB, off, N)
		sum += lower + upper
	}
	fmt.Println(sum)
}

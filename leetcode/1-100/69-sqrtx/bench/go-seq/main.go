// Benchmark workload — Sqrt(x) (LeetCode #69).
// Go single-threaded mirror of bench/sqrtx.{kara,rs,c}. The ★'s binary search
// for floor(sqrt(x)) run K=3_000_000 times over a Knuth-multiplicative sweep of
// x across [0, 2^31), folding results into a rolling polynomial hash. No
// allocation — a pure compute/branch benchmark of the search loop.
// See ../README.md § Benchmarks.

package main

import "fmt"

func mySqrt(x int64) int64 {
	var lo, hi, ans int64 = 0, x, 0
	for lo <= hi {
		mid := lo + (hi-lo)/2
		if mid*mid <= x {
			ans = mid
			lo = mid + 1
		} else {
			hi = mid - 1
		}
	}
	return ans
}

func main() {
	const total int64 = 3000000
	const modulus int64 = 1000000007
	const rng int64 = 2147483648 // 2^31

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		x := (k * 2654435761) % rng
		r := mySqrt(x)
		acc = (acc*131 + r) % modulus
	}
	fmt.Println(acc)
}

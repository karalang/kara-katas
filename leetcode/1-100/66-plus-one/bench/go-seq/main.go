// Benchmark workload — Plus One (LeetCode #66).
// Go single-threaded mirror of bench/plus_one.{kara,rs,c}. A fixed-width (W=9)
// decimal digit buffer driven as a base-10 counter: the ★'s reverse-scan carry
// applied in place K times, folding a rotating digit into a rolling
// polynomial-hash sink. In place, no per-iter allocation. K < 10^9 so the
// counter never overflows 9 digits. See ../README.md § Benchmarks.

package main

import "fmt"

func main() {
	const total int64 = 80000000
	const modulus int64 = 1000000007
	const W = 9

	var digits [W]int64

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		i := W - 1
		for i >= 0 {
			if digits[i] < 9 {
				digits[i]++
				break // carry absorbed
			}
			digits[i] = 0
			i--
		}
		acc = (acc*131 + digits[k%int64(W)]) % modulus
	}

	fmt.Println(acc)
}

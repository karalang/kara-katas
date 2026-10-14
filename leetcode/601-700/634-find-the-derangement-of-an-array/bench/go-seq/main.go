// LeetCode 634 -- Find the Derangement of An Array, bench mirror in Go.
//
// The ★ arm of find_derangement.kara: D(n) = (n - 1) * (D(n - 1) +
// D(n - 2)) modulo 10^9 + 7, kept in two variables. Same values of n,
// same output line.
package main

import "fmt"

const MOD = 1000000007

func findDerangement(n int64) int64 {
	var before, last int64 = 1, 0
	for i := int64(2); i < n+1; i++ {
		next := (i - 1) * ((last + before) % MOD) % MOD
		before = last
		last = next
	}
	return last
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(634)
	sizes := []int64{}
	for i := 0; i < 100; i++ {
		wide := nextRandom(&seed) * 32768
		wide += nextRandom(&seed)
		sizes = append(sizes, 1+wide%1000000)
	}
	var total, checksum int64
	for _, n := range sizes {
		d := findDerangement(n)
		total = (total + d) % MOD
		checksum = (checksum*31 + d) % MOD
	}
	fmt.Printf("%d values of n: total %d, checksum %d\n", len(sizes), total, checksum)
}

// Benchmark for #440: mirror of find_kth_number.kara (counting down the
// denary tree) on 1,000,000 random queries with n up to 10^9.
package main

import "fmt"

// The numbers in [1, n] that start with prefix.
func countUnder(prefix, n int64) int64 {
	count := int64(0)
	first := prefix
	last := prefix
	for first <= n {
		count += min(n, last) - first + 1
		first *= 10
		last = last*10 + 9
	}
	return count
}

func findKthNumber(n, k int64) int64 {
	current := int64(1)
	left := k - 1
	for left > 0 {
		under := countUnder(current, n)
		if under <= left {
			left -= under
			current++
		} else {
			left--
			current *= 10
		}
	}
	return current
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const queries = 1000000
	seed := int64(440)
	total := int64(0)
	checksum := int64(0)
	for q := 0; q < queries; q++ {
		a := nextRandom(&seed)
		n := 1 + (a*32768+nextRandom(&seed))%1000000000
		b := nextRandom(&seed)
		k := 1 + (b*32768+nextRandom(&seed))%n
		x := findKthNumber(n, k)
		total += x
		checksum = (checksum*31 + x) % 1000000007
	}
	fmt.Printf("%d queries with n up to 10^9: total %d, checksum %d\n", queries, total, checksum)
}

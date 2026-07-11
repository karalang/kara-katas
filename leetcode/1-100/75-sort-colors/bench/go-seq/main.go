// Benchmark workload — Sort Colors (LeetCode #75).
// Go single-threaded mirror of bench/sort_colors.{kara,rs,c}. Dutch National Flag
// one-pass sort over an []int64 allocated ONCE (n=500) and reused: each of
// K=200,000 iterations refills it in place with a k-dependent {0,1,2} pattern,
// sorts in place, and folds the result into a rolling polynomial hash. The
// measured work is the sort's data-dependent branches and swaps, not allocation.
// See ../README.md § Benchmarks.

package main

import "fmt"

func sortColors(a []int64) {
	n := int64(len(a))
	if n == 0 {
		return
	}
	low, mid, high := int64(0), int64(0), n-1
	for mid <= high {
		if a[mid] == 0 {
			a[low], a[mid] = a[mid], a[low]
			low++
			mid++
		} else if a[mid] == 1 {
			mid++
		} else {
			a[mid], a[high] = a[high], a[mid]
			high--
		}
	}
}

func main() {
	const n int64 = 500
	const total int64 = 200000
	const modulus int64 = 1000000007

	a := make([]int64, n)

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		for j := int64(0); j < n; j++ {
			a[j] = (j*7 + k*13) % 3
		}
		sortColors(a)
		for j := int64(0); j < n; j++ {
			acc = (acc*131 + a[j]) % modulus
		}
	}
	fmt.Println(acc)
}

// Benchmark workload — Permutation Sequence (LeetCode #60), NEXT-PERM solver.
// Go mirror of ../permutation_sequence_nextperm.kara. Same M=9 rotated (n,k)
// cases, K=333, next_permutation iterated k-1 times (O(k·n)) over a fresh
// []int64 — see that file's header for rationale.

package main

import "fmt"

var ntab = []int64{9, 8, 9, 7, 8, 9, 6, 7, 9}
var ktab = []int64{362880, 40320, 181440, 5040, 20160, 300000, 720, 2520, 250000}

const (
	mSizes = 9
	kIters = 333
)

func nextPermutation(a []int64) {
	length := int64(len(a))
	i := length - 2
	for i >= 0 && a[i] >= a[i+1] {
		i--
	}
	if i >= 0 {
		j := length - 1
		for a[j] <= a[i] {
			j--
		}
		a[i], a[j] = a[j], a[i]
	}
	lo, hi := i+1, length-1
	for lo < hi {
		a[lo], a[hi] = a[hi], a[lo]
		lo++
		hi--
	}
}

func getPermutation(n, k int64) []int64 {
	a := make([]int64, n)
	for i := int64(0); i < n; i++ {
		a[i] = i + 1
	}
	for step := int64(0); step < k-1; step++ {
		nextPermutation(a)
	}
	return a
}

func checksum(perm []int64, n int64) int64 {
	var s int64 = 0
	for i := int64(0); i < n; i++ {
		s += perm[i] * (i + 1)
	}
	return s
}

func main() {
	var total int64 = 0
	for k := int64(0); k < kIters; k++ {
		idx := k % mSizes
		perm := getPermutation(ntab[idx], ktab[idx])
		total += checksum(perm, ntab[idx])
	}
	fmt.Println(total)
}

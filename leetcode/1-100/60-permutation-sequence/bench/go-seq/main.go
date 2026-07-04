// Benchmark workload — Permutation Sequence (LeetCode #60), FACTORIAL solver.
// Go mirror of ../permutation_sequence.kara. Same M=9 rotated (n,k) cases,
// K=500k, factorial-number-system generator over fresh []int64 slices,
// position-weighted checksum, and sink — see that file's header for rationale.

package main

import "fmt"

var ntab = []int64{9, 8, 9, 7, 8, 9, 6, 7, 9}
var ktab = []int64{362880, 40320, 181440, 5040, 20160, 300000, 720, 2520, 250000}

const (
	mSizes = 9
	kIters = 500000
)

func getPermutation(n, k int64) []int64 {
	fact := make([]int64, n+1)
	fact[0] = 1
	for i := int64(1); i <= n; i++ {
		fact[i] = fact[i-1] * i
	}
	digits := make([]int64, n)
	for i := int64(0); i < n; i++ {
		digits[i] = i + 1
	}
	result := make([]int64, 0, n)
	kk := k - 1
	for pos := int64(0); pos < n; pos++ {
		block := fact[n-1-pos]
		idx := kk / block
		kk %= block
		result = append(result, digits[idx])
		digits = append(digits[:idx], digits[idx+1:]...)
	}
	return result
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

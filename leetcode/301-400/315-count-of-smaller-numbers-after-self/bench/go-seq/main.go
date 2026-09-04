// Benchmark lane for LeetCode 315 — Go mirror of bench/count_smaller.kara.
// Generate N values once, then PASSES Fenwick-tree passes (sort+dedup for the
// ranks, then per element a binary search, a prefix query and a point update,
// right to left), each after swapping two elements chosen from the checksum.
package main

import (
	"fmt"
	"sort"
)

const (
	N      = 200000
	PASSES = 24
	MASK   = int64(1073741823)
)

func lcg(s int64) int64 { return (s*1103515245 + 12345) & 0x7fffffff }

func lowerBound(s []int64, x int64) int64 {
	lo, hi := int64(0), int64(len(s))
	for lo < hi {
		mid := (lo + hi) / 2
		if s[mid] < x {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return lo
}

func countSmaller(nums []int64) []int64 {
	n := len(nums)
	distinct := make([]int64, n)
	copy(distinct, nums)
	sort.Slice(distinct, func(a, b int) bool { return distinct[a] < distinct[b] })
	m := 0
	for i := 0; i < n; i++ {
		if i == 0 || distinct[i] != distinct[i-1] {
			distinct[m] = distinct[i]
			m++
		}
	}
	distinct = distinct[:m]
	tree := make([]int64, m+1)
	counts := make([]int64, n)
	for i := n - 1; i >= 0; i-- {
		r := lowerBound(distinct, nums[i])
		var total int64
		for x := r; x > 0; x -= x & -x {
			total += tree[x]
		}
		counts[i] = total
		for x := r + 1; x <= int64(m); x += x & -x {
			tree[x]++
		}
	}
	return counts
}

func main() {
	seed := int64(315)
	nums := make([]int64, N)
	for i := 0; i < N; i++ {
		seed = lcg(seed)
		nums[i] = seed%200001 - 100000
	}
	checksum := int64(0)
	for pass := 0; pass < PASSES; pass++ {
		i := checksum % N
		j := (checksum*7 + 13) % N
		nums[i], nums[j] = nums[j], nums[i]
		counts := countSmaller(nums)
		var total int64
		for _, c := range counts {
			total += c
		}
		checksum = (checksum*31 + total) & MASK
		nums[i], nums[j] = nums[j], nums[i]
	}
	fmt.Printf("checksum %d\n", checksum)
}

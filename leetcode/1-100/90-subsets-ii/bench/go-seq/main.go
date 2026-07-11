// Benchmark workload — Subsets II (LeetCode #90).
// Go mirror of ../subsets_ii.kara. Enumerate-and-fold over the emit-at-node dedup
// backtracking of a sorted multiset (8 distinct values x2 => 3^8 unique subsets); the
// path slice is appended/resliced (Kara's reused Vec push/pop), K=2700 iterations.
package main

import "fmt"

func enumerate(nums []int64, start int64, path []int64, acc int64) (int64, []int64) {
	plen := int64(len(path))
	a := (acc*131 + (plen + 1)) % 1000000007
	for _, x := range path {
		a = (a*131 + (x + 1)) % 1000000007
	}
	n := int64(len(nums))
	for i := start; i < n; i++ {
		if i == start || nums[i] != nums[i-1] {
			path = append(path, nums[i])
			a, path = enumerate(nums, i+1, path, a)
			path = path[:len(path)-1]
		}
	}
	return a, path
}

func main() {
	const d = 8
	const r = 2
	const total = 2700
	const modulus = 1000000007
	nums := make([]int64, 0, d*r)
	for v := int64(0); v < d; v++ {
		for c := int64(0); c < r; c++ {
			nums = append(nums, v)
		}
	}
	var sum int64 = 0
	for iter := int64(0); iter < total; iter++ {
		path := make([]int64, 0, d)
		rr, _ := enumerate(nums, 0, path, iter)
		sum = (sum*131 + rr) % modulus
	}
	fmt.Println(sum)
}

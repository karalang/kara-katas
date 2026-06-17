// LeetCode #35 bench — Go (mirror of search_insert.kara).
//
// Half-open lower_bound style: one searchInsert (first index >= target) per query
// over a fixed strictly-increasing array of distinct values, TOTAL queries with
// cycling targets, each index folded into a checksum (single goroutine — seq).
package main

import "fmt"

func searchInsert(nums []int64, length, target int64) int64 {
	lo, hi := int64(0), length
	for lo < hi {
		mid := lo + (hi-lo)/2
		if nums[mid] < target {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return lo
}

func main() {
	const n int64 = 4096
	const total int64 = 14000000
	const modulus int64 = 1000000007

	nums := make([]int64, 0, n)
	for p := int64(0); p < n; p++ {
		nums = append(nums, 2*p)
	}

	span := 2 * n
	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		target := k % span
		idx := searchInsert(nums, n, target)
		acc = (acc*31 + idx) % modulus
	}

	fmt.Println(acc)
}

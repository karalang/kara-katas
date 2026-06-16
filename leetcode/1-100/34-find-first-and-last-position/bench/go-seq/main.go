// LeetCode #34 bench — Go (mirror of search_range.kara).
//
// Two-bounds style: lower_bound + upper_bound per query over a fixed sorted array
// with duplicate runs, TOTAL queries with cycling targets, both endpoints folded
// into a checksum (single goroutine — seq).
package main

import "fmt"

func lowerBound(nums []int64, length, target int64) int64 {
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

func upperBound(nums []int64, length, target int64) int64 {
	lo, hi := int64(0), length
	for lo < hi {
		mid := lo + (hi-lo)/2
		if nums[mid] <= target {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return lo
}

func main() {
	const n int64 = 4096
	const run int64 = 4
	const total int64 = 14000000
	const modulus int64 = 1000000007

	nums := make([]int64, 0, n)
	for p := int64(0); p < n; p++ {
		nums = append(nums, 2*(p/run))
	}

	span := 2 * n
	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		target := k % span
		lo := lowerBound(nums, n, target)
		var first, last int64 = -1, -1
		if lo < n && nums[lo] == target {
			first = lo
			last = upperBound(nums, n, target) - 1
		}
		acc = (acc*31 + (first + 1)) % modulus
		acc = (acc*31 + (last + 1)) % modulus
	}

	fmt.Println(acc)
}

package main

import "fmt"

// Benchmark workload for LeetCode #209 — Minimum Size Subarray Sum.
func minSubarrayLen(target int64, nums []int64, n int64) int64 {
	var left, sum int64 = 0, 0
	var best int64 = -1
	for right := int64(0); right < n; right++ {
		sum += nums[right]
		for sum >= target {
			length := right - left + 1
			if best == -1 || length < best {
				best = length
			}
			sum -= nums[left]
			left++
		}
	}
	if best == -1 {
		return 0
	}
	return best
}

func main() {
	var n int64 = 200000
	var targets int64 = 290

	nums := make([]int64, 0, n)
	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		nums = append(nums, 1+state%100) // 1..100, all positive
	}

	var sink int64 = 0
	for t := int64(0); t < targets; t++ {
		target := 200 + t*80
		sink += minSubarrayLen(target, nums, n)
	}

	fmt.Println(sink)
}

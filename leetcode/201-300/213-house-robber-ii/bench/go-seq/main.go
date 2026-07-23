package main

import "fmt"

// Benchmark workload for LeetCode #213 — House Robber II.
func robLinear(nums []int64, lo, hi int64) int64 {
	var prev, cur int64 = 0, 0
	for i := lo; i < hi; i++ {
		take := prev + nums[i]
		var next int64
		if take > cur {
			next = take
		} else {
			next = cur
		}
		prev = cur
		cur = next
	}
	return cur
}

func robWindow(nums []int64, s, w int64) int64 {
	if w == 1 {
		return nums[s]
	}
	skipLast := robLinear(nums, s, s+w-1)
	skipFirst := robLinear(nums, s+1, s+w)
	if skipLast > skipFirst {
		return skipLast
	}
	return skipFirst
}

func main() {
	var n int64 = 100000
	var window int64 = 2000
	var windows int64 = 130000

	nums := make([]int64, 0, n)
	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		nums = append(nums, 1+state%1000) // 1..1000, all positive
	}

	span := n - window
	var sink int64 = 0
	for w := int64(0); w < windows; w++ {
		s := (w * 977) % span
		sink += robWindow(nums, s, window)
	}

	fmt.Println(sink)
}

package main

import "fmt"

func maxI64(a, b int64) int64 {
	if a > b {
		return a
	}
	return b
}

func rob(nums []int64, n int64) int64 {
	var prev2 int64 = 0
	var prev int64 = 0
	for i := int64(0); i < n; i++ {
		cur := maxI64(prev, prev2+nums[i])
		prev2 = prev
		prev = cur
	}
	return prev
}

func main() {
	var n int64 = 5000
	var passes int64 = 90000

	nums := make([]int64, n)
	var state int64 = 12345
	for b := int64(0); b < n; b++ {
		state = (state*1103515245 + 12345) & 2147483647
		nums[b] = (state >> 16) % 1000
	}

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		state = (state*1103515245 + 12345) & 2147483647
		idx := state % n
		nums[idx] = (state >> 16) % 1000
		sink += rob(nums, n)
	}
	fmt.Println(sink)
}

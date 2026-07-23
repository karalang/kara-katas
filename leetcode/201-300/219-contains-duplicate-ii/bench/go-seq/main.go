package main

import "fmt"

func countNearby(nums []int64, k int64) int64 {
	last := make(map[int64]int64)
	n := int64(len(nums))
	var hits int64 = 0
	for i := int64(0); i < n; i++ {
		x := nums[i]
		if j, ok := last[x]; ok {
			if i-j <= k {
				hits++
			}
		}
		last[x] = i
	}
	return hits
}

func main() {
	var n, kmax, m int64 = 1000000, 40, 49999

	nums := make([]int64, 0, n)
	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		nums = append(nums, state%m)
	}

	var sink int64 = 0
	for k := int64(1); k <= kmax; k++ {
		sink += countNearby(nums, k)
	}
	fmt.Println(sink)
}

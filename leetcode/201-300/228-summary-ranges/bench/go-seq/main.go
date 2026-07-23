package main

import "fmt"

func summaryMetric(nums []int64, n int64) int64 {
	var i int64 = 1
	start := nums[0]
	var ranges int64 = 0
	var esum int64 = 0
	for i <= n {
		if i == n || nums[i] != nums[i-1]+1 {
			end := nums[i-1]
			ranges += 1
			esum += start + end
			if i < n {
				start = nums[i]
			}
		}
		i += 1
	}
	return ranges + esum
}

func main() {
	var n int64 = 1000000
	var passes int64 = 250

	nums := make([]int64, 0, n)
	var state int64 = 12345
	var v int64 = 0
	for c := int64(0); c < n; c++ {
		state = (state*1103515245 + 12345) & 2147483647
		v = v + 1 + (state % 3)
		nums = append(nums, v)
	}

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		sink += summaryMetric(nums, n)
	}
	fmt.Println(sink)
}

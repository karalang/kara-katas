// LeetCode 152 — Maximum Product Subarray, Go seq mirror.
package main

import "fmt"

func maxProduct(nums []int64) int64 {
	if len(nums) == 0 {
		return 0
	}
	best, curMax, curMin := nums[0], nums[0], nums[0]
	for _, x := range nums[1:] {
		if x < 0 {
			curMax, curMin = curMin, curMax
		}
		if p := curMax * x; p > x {
			curMax = p
		} else {
			curMax = x
		}
		if p := curMin * x; p < x {
			curMin = p
		} else {
			curMin = x
		}
		if curMax > best {
			best = curMax
		}
	}
	return best
}

func main() {
	const N = 2_000_000
	data := make([]int64, N)
	state := int64(12345)
	for i := 0; i < N; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		data[i] = (state % 5) - 2
	}
	var sum int64
	for k := 0; k < 10; k++ {
		sum += maxProduct(data)
	}
	fmt.Println(sum)
}

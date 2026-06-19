// LeetCode #42 bench mirror — Go, the converging two-pointer solver (★).
//
// Mirrors bench/trapping_rain_water.kara: advance the shorter outer wall, settling each
// column with its running max. Buffer reused in place each iteration with a k-dependent
// jagged terrain. Same workload + sink as every other mirror.
package main

import "fmt"

func trap(height []int64, n int64) int64 {
	var left int64 = 0
	right := n - 1
	var leftMax, rightMax int64 = 0, 0
	var water int64 = 0
	for left < right {
		if height[left] < height[right] {
			if height[left] >= leftMax {
				leftMax = height[left]
			} else {
				water += leftMax - height[left]
			}
			left++
		} else {
			if height[right] >= rightMax {
				rightMax = height[right]
			} else {
				water += rightMax - height[right]
			}
			right--
		}
	}
	return water
}

func main() {
	var total int64 = 200000
	var n int64 = 1000
	var modulus int64 = 1000000007

	height := make([]int64, n)
	for i := int64(0); i < n; i++ {
		height[i] = (i * 37) % 100
	}

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		height[k%n] = (k * 19) % 100
		ans := trap(height, n)
		acc = (acc*131 + ans) % modulus
	}

	fmt.Println(acc)
}

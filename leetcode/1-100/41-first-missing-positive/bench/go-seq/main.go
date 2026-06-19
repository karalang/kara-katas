// LeetCode #41 bench mirror — Go, the in-place cyclic-sort solver (★).
//
// Mirrors bench/first_missing_positive.kara: swap each in-range value to its home index
// v-1, then scan for the first slot not holding its home value. Buffer reused in place each
// iteration. Same workload + sink as every other mirror.
package main

import "fmt"

func firstMissingPositive(nums []int64, n int64) int64 {
	var i int64 = 0
	for i < n {
		v := nums[i]
		if v >= 1 && v <= n && nums[v-1] != v {
			nums[v-1], nums[i] = v, nums[v-1]
		} else {
			i++
		}
	}
	for j := int64(0); j < n; j++ {
		if nums[j] != j+1 {
			return j + 1
		}
	}
	return n + 1
}

func main() {
	var total int64 = 200000
	var n int64 = 100
	var modulus int64 = 1000000007

	nums := make([]int64, n)

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		rot := k % n
		for i := int64(0); i < n; i++ {
			nums[i] = ((i + rot) % n) + 1
		}
		nums[k%n] = n + 7

		ans := firstMissingPositive(nums, n)
		acc = (acc*131 + ans) % modulus
	}

	fmt.Println(acc)
}

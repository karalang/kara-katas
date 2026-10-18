// LeetCode #724: Find Pivot Index -- the total, then one running sum.
// Benchmark mirror of the Kara star arm: the total once, then a walk
// from the left keeping the sum of the numbers passed, stopping at the
// first index whose left sum equals what is left on the right.
package main

import "fmt"

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func pivotIndex(nums []int64) int64 {
	var total int64
	for _, x := range nums {
		total += x
	}
	var left int64
	for i := range nums {
		if left == total-left-nums[i] {
			return int64(i)
		}
		left += nums[i]
	}
	return -1
}

func main() {
	seed := int64(724)
	arrays := make([][]int64, 0, 50)
	for k := 0; k < 50; k++ {
		nums := make([]int64, 0, 9999)
		for j := 0; j < 4999; j++ {
			nums = append(nums, nextRandom(&seed)%2001-1000)
		}
		nums = append(nums, nextRandom(&seed)%2001-1000)
		for j := 0; j < 4999; j++ {
			nums = append(nums, nums[4998-j])
		}
		arrays = append(arrays, nums)
	}
	var sum int64
	for round := 0; round < 1000; round++ {
		for k := 0; k < 50; k++ {
			p := (round*7919 + k*31) % 9999
			arrays[k][p] = -arrays[k][p]
			sum += pivotIndex(arrays[k])
		}
	}
	fmt.Printf("1000 rounds of 50 arrays of 9999 numbers: sum %d\n", sum)
}

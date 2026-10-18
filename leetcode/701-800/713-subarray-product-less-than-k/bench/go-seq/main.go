// LeetCode #713: Subarray Product Less Than K -- a sliding window.
// Benchmark mirror of the Kara star arm: extend the window right; while
// its product is k or more, drop numbers from the left; count the
// subarrays ending at each right end.
package main

import "fmt"

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func numSubarrayProductLessThanK(nums []int64, k int64) int64 {
	if k <= 1 {
		return 0
	}
	product, left, count := int64(1), 0, int64(0)
	for right := range nums {
		product *= nums[right]
		for product >= k {
			product /= nums[left]
			left++
		}
		count += int64(right - left + 1)
	}
	return count
}

func main() {
	seed := int64(713)
	tops := []int64{2, 3, 5, 10, 20, 50, 100, 200, 500, 1000}
	var arrays [][]int64
	for _, t := range tops {
		nums := make([]int64, 30000)
		for i := range nums {
			nums[i] = 1 + nextRandom(&seed)%t
		}
		arrays = append(arrays, nums)
	}
	sum := int64(0)
	for round := 0; round < 200; round++ {
		for _, nums := range arrays {
			sum += numSubarrayProductLessThanK(nums, 1000000)
		}
	}
	fmt.Printf("200 rounds of 10 arrays of 30000, k = 1000000: sum %d\n", sum)
}

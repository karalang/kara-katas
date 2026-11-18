// LeetCode #2270: Number of Ways to Split Array -- the bench, the ★ arm.
package main

import "fmt"

func waysToSplitArray(nums []int64) int64 {
	var total int64
	for _, x := range nums {
		total += x
	}
	var left, ways int64
	for i := 0; i < len(nums)-1; i++ {
		left += nums[i]
		if left >= total-left {
			ways++
		}
	}
	return ways
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2270

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for t := 0; t < 100; t++ {
		nums := make([]int64, 0)
		for i := 0; i < 100000; i++ {
			nums = append(nums, nextRandom()%200001-100000)
		}
		check = (check*31 + waysToSplitArray(nums)) % 1000000007
	}
	fmt.Printf("100 arrays of 10^5: checksum %d\n", check)
}

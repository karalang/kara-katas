// LeetCode #1150: Check If a Number Is Majority Element in a Sorted Array
// -- the Go mirror of the ★ arm: the run's start by `sort.Search`, then
// the value n / 2 places on.
package main

import (
	"fmt"
	"sort"
)

func isMajorityElement(nums []int64, target int64) bool {
	n := len(nums)
	first := sort.Search(n, func(i int) bool { return nums[i] >= target })
	return first+n/2 < n && nums[first+n/2] == target
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func big(seed *int64) int64 {
	a := nextRandom(seed)
	return (a*32768+nextRandom(seed))%1000000000 + 1
}

func list(seed *int64) []int64 {
	copies := 450 + nextRandom(seed)%101
	v := big(seed)
	nums := make([]int64, 0, 1000)
	for i := int64(0); i < copies; i++ {
		nums = append(nums, v)
	}
	for i := copies; i < 1000; i++ {
		nums = append(nums, big(seed))
	}
	sort.Slice(nums, func(i, j int) bool { return nums[i] < nums[j] })
	return nums
}

func main() {
	seed := int64(1150)
	lists := make([][]int64, 64)
	for i := range lists {
		lists[i] = list(&seed)
	}
	yes, check := int64(0), int64(0)
	for q := int64(0); q < 10000000; q++ {
		nums := lists[q%64]
		kind := nextRandom(&seed) % 4
		var target int64
		switch kind {
		case 0:
			target = nums[nextRandom(&seed)%1000]
		case 1:
			target = nums[500]
		case 2:
			target = nums[nextRandom(&seed)%1000] + 1
		default:
			target = big(&seed)
		}
		if isMajorityElement(nums, target) {
			yes++
			check = (check*31 + q) % 1000000007
		}
	}
	fmt.Printf("10000000 queries over 64 lists of 1000 values: majority %d, checksum %d\n", yes, check)
}

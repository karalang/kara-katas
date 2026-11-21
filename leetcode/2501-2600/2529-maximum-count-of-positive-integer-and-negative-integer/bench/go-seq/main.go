// LeetCode #2529: Maximum Count of Positive Integer and Negative Integer
// -- Go mirror of the benchmark (count.kara): the same lists, passes,
// order and checksum.
package main

import (
	"fmt"
	"sort"
)

func firstWhere(nums []int64, above int64) int64 {
	lo, hi := int64(0), int64(len(nums))
	for lo < hi {
		mid := lo + (hi-lo)/2
		if nums[mid] > above {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

func maximumCount(nums []int64) int64 {
	negatives := firstWhere(nums, -1)
	positives := int64(len(nums)) - firstWhere(nums, 0)
	return max(negatives, positives)
}

var seed int64 = 2529

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]int64, 1000)
	for t := range lists {
		shift := nextRandom()%4001 - 2000
		nums := make([]int64, 2000)
		for j := range nums {
			nums[j] = min(max(nextRandom()%4001-2000+shift, -2000), 2000)
		}
		sort.Slice(nums, func(a, b int) bool { return nums[a] < nums[b] })
		lists[t] = nums
	}
	const passes = 3000
	var check int64
	for p := int64(0); p < passes; p++ {
		start := check % 1000
		for i := int64(0); i < 1000; i++ {
			check = (check*31 + maximumCount(lists[(start+i)%1000]) + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 1000 lists of 2000 numbers: checksum %d\n", passes, check)
}

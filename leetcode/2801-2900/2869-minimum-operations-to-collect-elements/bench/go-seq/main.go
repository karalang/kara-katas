// LeetCode #2869: Minimum Operations to Collect Elements -- the bench,
// as collect.kara: 50000 arrays of 50 values, each answered 20 times by
// the bit-mask arm.
package main

import (
	"fmt"
	"slices"
)

func minOperations(nums []int64, k int64) int64 {
	full := int64(1)<<k - 1
	var mask int64
	n := int64(len(nums))
	for i := n - 1; i >= 0; i-- {
		if nums[i] <= k {
			mask |= int64(1) << (nums[i] - 1)
		}
		if mask == full {
			return n - i
		}
	}
	return n
}

var seed int64 = 2869

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, n = 50000, 20, 50
	all := make([][]int64, count)
	ks := make([]int64, count)
	for c := 0; c < count; c++ {
		nums := make([]int64, n)
		for i := range nums {
			nums[i] = nextRandom()%n + 1
		}
		nums[nextRandom()%n] = 1
		reach := int64(1)
		for slices.Contains(nums, reach+1) {
			reach++
		}
		all[c] = nums
		ks[c] = nextRandom()%reach + 1
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			ops := minOperations(all[c], ks[c])
			total += ops
			check = (check*31 + ops + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: %d operations, checksum %d\n", count, n, rounds, total, check)
}

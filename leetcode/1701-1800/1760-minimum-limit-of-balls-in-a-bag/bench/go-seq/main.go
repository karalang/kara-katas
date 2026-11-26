// LeetCode #1760: Minimum Limit of Balls in a Bag -- the bench in Go,
// mirroring minimum_size.kara: a binary search on the penalty.
package main

import (
	"fmt"
	"slices"
)

func operations(nums []int32, penalty int64) int64 {
	total := int64(0)
	for _, x := range nums {
		total += int64(x-1) / penalty
	}
	return total
}

func minimumSize(nums []int32, maxOperations int32) int32 {
	lo, hi := int32(1), slices.Max(nums)
	for lo < hi {
		mid := lo + (hi-lo)/2
		if operations(nums, int64(mid)) <= int64(maxOperations) {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

func main() {
	seed := int64(1760)
	bags := make([]int32, 0, 100000)
	for i := 0; i < 100000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		high := seed / 65536
		seed = (seed*1103515245 + 12345) % 2147483648
		bags = append(bags, int32(1+(high*32768+seed/65536)%1000000000))
	}
	check := int64(0)
	for call := int64(0); call < 100; call++ {
		at := (check + call*7919) % 100000
		bags[at] = int32(1 + (check*13+call)%1000000000)
		ops := 1 + (check+call*104729)%1000000000
		check = (check*31 + int64(minimumSize(bags, int32(ops)))) % 1000000007
	}
	fmt.Printf("100 calls over 100000 bags: checksum %d\n", check)
}

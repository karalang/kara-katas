// LeetCode #2892: Minimizing Array After Replacing Pairs With Their
// Product -- the bench, as
// product.kara: 50 arrays of 10^5 values, each with its k, answered 20
// times by the greedy arm.
package main

import (
	"fmt"
	"slices"
)

func minArrayLength(nums []int64, k int64) int64 {
	if slices.Contains(nums, 0) {
		return 1
	}
	var runs int64 = 1
	product := nums[0]
	for _, x := range nums[1:] {
		if product*x <= k {
			product *= x
		} else {
			runs++
			product = x
		}
	}
	return runs
}

var seed int64 = 2892

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	const count, rounds, n = 50, 20, 100000
	arrays := make([][]int64, count)
	ks := make([]int64, count)
	for c := range arrays {
		nums := make([]int64, n)
		for i := range nums {
			if nextRandom()%2 == 0 {
				nums[i] = 1
			} else {
				nums[i] = nextRandom()%1000 + 1
			}
		}
		if c%10 == 0 {
			nums[n-1-c] = 0
		}
		arrays[c] = nums
		ks[c] = wide()%1000000000 + 1
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for c, nums := range arrays {
			length := minArrayLength(nums, ks[c])
			total += length
			check = (check*31 + length + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: lengths total %d, checksum %d\n", count, n, rounds, total, check)
}

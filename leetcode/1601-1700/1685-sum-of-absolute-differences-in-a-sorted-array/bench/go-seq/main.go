// LeetCode #1685: Sum of Absolute Differences in a Sorted Array -- the
// bench's Go mirror: the ★ arm on 50 random sorted arrays of 100000 values,
// all drawn first, each answered 20 times.
package main

import (
	"fmt"
	"slices"
)

func sumDifferences(nums []int32) []int32 {
	n := int64(len(nums))
	var total int32
	for _, x := range nums {
		total += x
	}
	var before int32
	result := make([]int32, 0, n)
	for i := int64(0); i < n; i++ {
		x := int64(nums[i])
		after := int64(total) - int64(before) - x
		result = append(result, int32(x*i-int64(before)+after-x*(n-1-i)))
		before += int32(x)
	}
	return result
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1685

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, size, rounds = 50, 100000, 20
	arrays := make([][]int32, 0, count)
	for c := 0; c < count; c++ {
		nums := make([]int32, size)
		for i := range nums {
			nums[i] = int32(nextRandom()%10000 + 1)
		}
		slices.Sort(nums)
		arrays = append(arrays, nums)
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			answer := sumDifferences(nums)
			first, middle, last := int64(answer[0]), int64(answer[size/2]), int64(answer[size-1])
			total += middle
			check = (check*31 + first + middle + last + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: middles sum to %d, checksum %d\n", count, size, rounds, total, check)
}

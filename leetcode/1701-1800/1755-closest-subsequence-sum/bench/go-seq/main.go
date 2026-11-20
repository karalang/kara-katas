// LeetCode #1755: Closest Subsequence Sum -- the bench (closest.kara in
// Go): meet in the middle with binary search.
package main

import (
	"fmt"
	"math"
	"math/bits"
	"slices"
	"sort"
)

func subsetSums(values []int32) []int32 {
	count := 1 << len(values)
	sums := make([]int32, count)
	for mask := 1; mask < count; mask++ {
		sums[mask] = sums[mask&(mask-1)] + values[bits.TrailingZeros(uint(mask))]
	}
	return sums
}

func minAbsDifference(nums []int32, goal int32) int32 {
	half := len(nums) / 2
	left := subsetSums(nums[:half])
	right := subsetSums(nums[half:])
	slices.Sort(right)
	best := int32(math.MaxInt32)
	for _, l := range left {
		rest := goal - l
		at := sort.Search(len(right), func(j int) bool { return right[j] >= rest })
		if at < len(right) {
			best = min(best, right[at]-rest)
		}
		if at > 0 {
			best = min(best, rest-right[at-1])
		}
	}
	return best
}

var seed int64 = 1755

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	const count, n = 8, 40
	nums := make([][]int32, count)
	goals := make([]int32, count)
	for c := range nums {
		nums[c] = make([]int32, n)
		for i := range nums[c] {
			nums[c][i] = int32(wide()%20000001 - 10000000)
		}
		goals[c] = int32(wide()%200000001 - 100000000)
	}
	var sum, check int64
	for c := range nums {
		answer := int64(minAbsDifference(nums[c], goals[c]))
		sum += answer
		check = (check*31 + answer) % 1000000007
	}
	fmt.Printf("%d problems of %d values: differences add to %d, checksum %d\n", count, n, sum, check)
}

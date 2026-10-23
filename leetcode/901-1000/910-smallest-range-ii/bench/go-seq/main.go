// LeetCode #910: Smallest Range II -- bench program, Go.
//
// The sorted values split in two, over 500,000 numbers up to 10^4 built
// once. Each round solves them with a k that changes from round to round,
// folds the score into a checksum and changes one number.
package main

import (
	"fmt"
	"slices"
)

func smallestRangeII(nums []int64, k int64) int64 {
	a := slices.Clone(nums)
	slices.Sort(a)
	n := len(a)
	best := a[n-1] - a[0]
	for i := 0; i < n-1; i++ {
		hi := max(a[i]+k, a[n-1]-k)
		lo := min(a[0]+k, a[i+1]-k)
		best = min(best, hi-lo)
	}
	return best
}

var seed int64 = 910

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var n int64 = 500000
	var rounds int64 = 40
	nums := make([]int64, n)
	for i := int64(0); i < n; i++ {
		nums[i] = nextRandom() % 10001
	}
	var total, check int64
	for round := int64(0); round < rounds; round++ {
		got := smallestRangeII(nums, round*373%5001)
		total += got
		check = (check*31 + got) % 1000000007
		nums[round*7919%n] = nextRandom() % 10001
	}
	fmt.Printf("%d rounds over %d numbers: scores summing to %d, checksum %d\n", rounds, n, total, check)
}

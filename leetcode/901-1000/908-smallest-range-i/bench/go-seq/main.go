// LeetCode #908: Smallest Range I -- bench program, Go.
//
// The largest and smallest values, over 500,000 numbers up to 10^4 built
// once. Each round scores them with a k that changes from round to round,
// folds the score into a checksum and changes one number.
package main

import "fmt"

func smallestRangeI(nums []int64, k int64) int64 {
	lo, hi := nums[0], nums[0]
	for i := 1; i < len(nums); i++ {
		if nums[i] < lo {
			lo = nums[i]
		}
		if nums[i] > hi {
			hi = nums[i]
		}
	}
	score := hi - lo - 2*k
	if score < 0 {
		return 0
	}
	return score
}

var seed int64 = 908

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var n int64 = 500000
	var rounds int64 = 500
	nums := make([]int64, n)
	for i := int64(0); i < n; i++ {
		nums[i] = nextRandom() % 10001
	}
	var total, check int64
	for round := int64(0); round < rounds; round++ {
		got := smallestRangeI(nums, round*37%5001)
		total += got
		check = (check*31 + got) % 1000000007
		nums[round*7919%n] = nextRandom() % 10001
	}
	fmt.Printf("%d rounds over %d numbers: scores summing to %d, checksum %d\n", rounds, n, total, check)
}

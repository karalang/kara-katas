// LeetCode #2760: Longest Even Odd Subarray With Threshold -- the bench
// (threshold.kara in Go): one pass with the length of the good run ending
// at each number.
package main

import "fmt"

func longestAlternatingSubarray(nums []int64, threshold int64) int64 {
	var best, run int64
	for i, x := range nums {
		if x > threshold {
			run = 0
		} else if run > 0 && x%2 != nums[i-1]%2 {
			run++
		} else if x%2 == 0 {
			run = 1
		} else {
			run = 0
		}
		best = max(best, run)
	}
	return best
}

var seed int64 = 2760

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds = 100000, 10
	nums := make([][]int64, count)
	thresholds := make([]int64, count)
	for k := range nums {
		a := make([]int64, 100)
		for i := range a {
			a[i] = nextRandom()%100 + 1
		}
		nums[k] = a
		thresholds[k] = nextRandom()%100 + 1
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for k := range nums {
			length := longestAlternatingSubarray(nums[k], thresholds[k])
			sum += length
			check = (check*31 + length + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 100, %d rounds: lengths sum to %d, checksum %d\n", count, rounds, sum, check)
}

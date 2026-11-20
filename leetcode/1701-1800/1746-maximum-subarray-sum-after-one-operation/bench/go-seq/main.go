// LeetCode #1746: Maximum Subarray Sum After One Operation -- the bench
// (square.kara in Go): Kadane's scan with two states.
package main

import (
	"fmt"
	"math"
)

func maxSumAfterOperation(nums []int32) int32 {
	var plain, squared int32
	best := int32(math.MinInt32)
	for _, x := range nums {
		squared = max(squared+x, max(plain, 0)+x*x)
		plain = max(plain, 0) + x
		best = max(best, squared)
	}
	return best
}

var seed int64 = 1746

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, n = 20, 40, 100000
	arrays := make([][]int32, count)
	for c := range arrays {
		arrays[c] = make([]int32, n)
		for i := range arrays[c] {
			arrays[c][i] = int32(nextRandom()%20001 - 10000)
		}
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			answer := int64(maxSumAfterOperation(nums))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: sums add to %d, checksum %d\n", count, n, rounds, sum, check)
}

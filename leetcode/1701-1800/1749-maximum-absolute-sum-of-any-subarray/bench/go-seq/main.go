// LeetCode #1749: Maximum Absolute Sum of Any Subarray -- the bench
// (abs.kara in Go): Kadane's scan both ways.
package main

import "fmt"

func maxAbsoluteSum(nums []int32) int32 {
	var high, low, best int32
	for _, x := range nums {
		high = max(high, 0) + x
		low = min(low, 0) + x
		best = max(best, max(high, -low))
	}
	return best
}

var seed int64 = 1749

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
			answer := int64(maxAbsoluteSum(nums))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: answers add to %d, checksum %d\n", count, n, rounds, sum, check)
}

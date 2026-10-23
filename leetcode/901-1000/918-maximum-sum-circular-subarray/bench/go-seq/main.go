// LeetCode #918: Maximum Sum Circular Subarray -- bench: Go mirror of
// Kadane for the largest and the smallest sum in
// max_subarray_sum_circular.kara.
package main

import "fmt"

func maxSubarraySumCircular(nums []int64) int64 {
	var total, bestHere, worstHere int64
	best, worst := nums[0], nums[0]
	for _, v := range nums {
		total += v
		bestHere = max(v, bestHere+v)
		best = max(best, bestHere)
		worstHere = min(v, worstHere+v)
		worst = min(worst, worstHere)
	}
	if best < 0 {
		return best
	}
	return max(best, total-worst)
}

var seed int64 = 918

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func value() int64 {
	high := nextRandom()
	return (high*2+nextRandom()%2)%60001 - 30000
}

func main() {
	rounds := 4000
	var n int64 = 30000
	nums := make([]int64, n)
	for i := range nums {
		nums[i] = value()
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		i := nextRandom() % n
		old := nums[i]
		nums[i] = value()
		a := maxSubarraySumCircular(nums)
		total += a
		check = (check*1000003 + a) % 1000000007
		nums[i] = old
	}
	fmt.Printf("%d rounds over %d values: answers summing to %d, checksum %d\n", rounds, n, total, check)
}

// LeetCode #2256: Minimum Average Difference -- the benchmark's Go mirror
// of average.kara: one pass with the total known, the first index whose
// two rounded-down averages are nearest.
package main

import "fmt"

func minimumAverageDifference(nums []int64) int64 {
	n := int64(len(nums))
	var total int64
	for _, v := range nums {
		total += v
	}
	var left, best int64
	bestGap := int64(-1)
	for i := int64(0); i < n; i++ {
		left += nums[i]
		right := total - left
		leftAverage := left / (i + 1)
		var rightAverage int64
		if i+1 != n {
			rightAverage = right / (n - i - 1)
		}
		gap := leftAverage - rightAverage
		if gap < 0 {
			gap = -gap
		}
		if bestGap < 0 || gap < bestGap {
			bestGap = gap
			best = i
		}
	}
	return best
}

var seed int64 = 2256

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	var check int64
	for t := 0; t < 20; t++ {
		nums := make([]int64, 100000)
		for i := range nums {
			nums[i] = wideRandom() % 100001
		}
		check = (check*31 + minimumAverageDifference(nums) + 1) % 1000000007
	}
	fmt.Printf("20 cases of 10^5 values: checksum %d\n", check)
}

// LeetCode #1330 bench, Go mirror of the Kāra bench: the ★ arm (the prefix,
// suffix and inside reversals' best gains in one pass) on 20 arrays of
// 3 * 10^4 values, the constraints' longest, within 30000 of 0, built once.
// Then 75 passes, each setting one value of every array from the checksum
// so far, answering it and folding the answer plus the pass into the
// checksum.
package main

import (
	"fmt"
	"math"
)

func abs32(x int32) int32 {
	if x < 0 {
		return -x
	}
	return x
}

func maxValueAfterReverse(nums []int32) int32 {
	n := len(nums)
	var total, gain int32
	highLow, lowHigh := int32(math.MinInt32), int32(math.MaxInt32)
	for i := 0; i < n-1; i++ {
		a, b := nums[i], nums[i+1]
		d := abs32(a - b)
		total += d
		gain = max(gain, abs32(nums[0]-b)-d)
		gain = max(gain, abs32(nums[n-1]-a)-d)
		highLow = max(highLow, min(a, b))
		lowHigh = min(lowHigh, max(a, b))
	}
	if n > 1 {
		gain = max(gain, 2*(highLow-lowHigh))
	}
	return total + gain
}

var seed int64 = 1330

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 30000
	arrays := make([][]int32, 20)
	for t := range arrays {
		arrays[t] = make([]int32, n)
		for i := range arrays[t] {
			arrays[t][i] = int32(nextRandom()%60001 - 30000)
		}
	}
	var check int64
	for pass := int64(0); pass < 75; pass++ {
		for t := 0; t < 20; t++ {
			arrays[t][check%n] = int32((check/7)%60001 - 30000)
			got := maxValueAfterReverse(arrays[t])
			check = (check*31 + int64(got) + pass) % 1000000007
		}
	}
	fmt.Printf("75 passes over 20 arrays of 3 * 10^4: checksum %d\n", check)
}

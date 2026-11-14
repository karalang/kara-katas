// LeetCode #1558: Minimum Numbers of Function Calls to Make Target Array --
// bench: the ★ arm (every value's 1 bits, and the widest value's length
// less one) over 20 arrays of 100000 values, built once, each asked 30
// times. Go mirror of calls.kara.
package main

import (
	"fmt"
	"math/bits"
)

func minOperations(nums []int64) int64 {
	var increments, widest int64
	for _, x := range nums {
		increments += int64(bits.OnesCount64(uint64(x)))
		if x > 0 {
			length := int64(64 - bits.LeadingZeros64(uint64(x)))
			if length > widest {
				widest = length
			}
		}
	}
	if widest-1 > 0 {
		return increments + widest - 1
	}
	return increments
}

var seed int64 = 1558

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	arrays := make([][]int64, 0, 20)
	for a := 0; a < 20; a++ {
		nums := make([]int64, 0, 100000)
		for i := 0; i < 100000; i++ {
			b := nextRandom()%30 + 1
			draw := nextRandom() * 32768
			draw += nextRandom()
			nums = append(nums, draw%(int64(1)<<b))
		}
		arrays = append(arrays, nums)
	}
	var check, total int64
	for pass := 0; pass < 30; pass++ {
		for _, nums := range arrays {
			calls := minOperations(nums)
			total += calls
			check = mix(check, calls)
		}
	}
	fmt.Printf("30 passes over 20 arrays of 100000 values: %d calls, checksum %d\n", total, check)
}

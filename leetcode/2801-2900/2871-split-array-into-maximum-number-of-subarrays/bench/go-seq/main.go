// LeetCode #2871: Split Array Into Maximum Number of Subarrays -- the
// bench, as split.kara: 50 arrays of 10^5 values, each answered 10 times
// by the greedy arm.
package main

import "fmt"

func maxSubarrays(nums []int64) int64 {
	var parts int64
	running := int64(-1)
	for _, v := range nums {
		running &= v
		if running == 0 {
			parts++
			running = -1
		}
	}
	return max(parts, 1)
}

var seed int64 = 2871

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	const count, rounds, n = 50, 10, 100000
	arrays := make([][]int64, count)
	for c := range arrays {
		nums := make([]int64, n)
		for i := range nums {
			if c%2 == 0 {
				nums[i] = wide() % 1000001
			} else {
				a := wide()
				nums[i] = (a | wide()) % 1000001
			}
		}
		arrays[c] = nums
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			parts := maxSubarrays(nums)
			total += parts
			check = (check*31 + parts + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: %d subarrays, checksum %d\n", count, n, rounds, total, check)
}

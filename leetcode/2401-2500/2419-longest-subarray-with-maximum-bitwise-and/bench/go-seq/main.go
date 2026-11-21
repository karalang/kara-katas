// LeetCode #2419: Longest Subarray With Maximum Bitwise AND -- the bench,
// the ★ arm in Go: one scan keeping the largest value so far and the run
// of it ending here.
package main

import "fmt"

func longestSubarray(nums []int64) int64 {
	var top, run, best int64
	for _, x := range nums {
		if x > top {
			top, run, best = x, 0, 0
		}
		if x == top {
			run++
			if run > best {
				best = run
			}
		} else {
			run = 0
		}
	}
	return best
}

var seed int64 = 2419

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var arrays [][]int64
	for i := int64(0); i < 10; i++ {
		nums := make([]int64, 0, 100000)
		for k := 0; k < 100000; k++ {
			if k > 0 && nextRandom()%2 == 0 {
				nums = append(nums, nums[k-1])
			} else {
				nums = append(nums, 1+nextRandom()%(2+100*i))
			}
		}
		arrays = append(arrays, nums)
	}
	var check int64
	for p := int64(0); p < 500; p++ {
		for _, nums := range arrays {
			check = (check*31 + longestSubarray(nums) + p) % 1000000007
		}
	}
	fmt.Printf("500 passes over 10 arrays of 10^5 values: checksum %d\n", check)
}

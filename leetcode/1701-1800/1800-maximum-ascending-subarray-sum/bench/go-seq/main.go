// LeetCode #1800: Maximum Ascending Subarray Sum -- the bench in Go: the ★
// arm over 4000 random lists of 100 numbers built once, 400000 calls.
package main

import "fmt"

func maxAscendingSum(nums []int32) int32 {
	run := nums[0]
	best := run
	for i := 1; i < len(nums); i++ {
		if nums[i] > nums[i-1] {
			run += nums[i]
		} else {
			run = nums[i]
		}
		best = max(best, run)
	}
	return best
}

var seed int64 = 1800

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]int32, 4000)
	for l := range lists {
		lists[l] = make([]int32, 100)
		for x := range lists[l] {
			lists[l][x] = int32(1 + nextRandom()%100)
		}
	}
	var check int64
	for call := int64(0); call < 400000; call++ {
		check = (check*31 + int64(maxAscendingSum(lists[(check+call)%4000]))) % 1000000007
	}
	fmt.Printf("400000 calls over 4000 lists of 100 numbers: checksum %d\n", check)
}

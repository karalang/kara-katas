// LeetCode #1793: Maximum Score of a Good Subarray -- the bench in Go: the ★
// arm over 200 random lists of 1000 numbers built once, 40000 calls.
package main

import "fmt"

func maximumScore(nums []int32, k int32) int32 {
	n := int64(len(nums))
	i, j := int64(k), int64(k)
	low := nums[i]
	best := low
	for i > 0 || j < n-1 {
		var left, right int32
		if i > 0 {
			left = nums[i-1]
		}
		if j < n-1 {
			right = nums[j+1]
		}
		if left > right {
			i--
			low = min(low, left)
		} else {
			j++
			low = min(low, right)
		}
		best = max(best, low*int32(j-i+1))
	}
	return best
}

var seed int64 = 1793

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]int32, 200)
	for l := range lists {
		lists[l] = make([]int32, 1000)
		for x := range lists[l] {
			lists[l][x] = int32(1 + nextRandom()%20000)
		}
	}
	var check int64
	for call := int64(0); call < 40000; call++ {
		k := check % 1000
		check = (check*31 + int64(maximumScore(lists[(check+call)%200], int32(k)))) % 1000000007
	}
	fmt.Printf("40000 calls over 200 lists of 1000 numbers: checksum %d\n", check)
}

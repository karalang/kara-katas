// LeetCode #1493: Longest Subarray of 1's After Deleting One Element -- the
// bench in Go, mirroring longest_subarray.kara: a sliding window holding at
// most one 0.
package main

import "fmt"

func longestSubarray(nums []int32) int32 {
	var best, zeros, left int64
	for right := int64(0); right < int64(len(nums)); right++ {
		if nums[right] == 0 {
			zeros++
		}
		for zeros > 1 {
			if nums[left] == 0 {
				zeros--
			}
			left++
		}
		if right-left > best {
			best = right - left
		}
	}
	return int32(best)
}

func main() {
	var seed int64 = 1493
	nums := make([]int32, 0, 100000)
	for i := 0; i < 100000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		if seed/65536%10 == 0 {
			nums = append(nums, 0)
		} else {
			nums = append(nums, 1)
		}
	}
	var check int64
	for call := int64(0); call < 1000; call++ {
		at := (check + call*7919) % 100000
		nums[at] = 1 - nums[at]
		check = (check*31 + int64(longestSubarray(nums)) + 1) % 1000000007
	}
	fmt.Printf("1000 calls over 100000 digits: checksum %d\n", check)
}

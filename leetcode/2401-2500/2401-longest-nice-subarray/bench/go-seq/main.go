// LeetCode #2401: Longest Nice Subarray -- the bench, the ★ arm in Go: a
// sliding window keeping the OR of its values, values leaving from the
// left by XOR until the new one fits.

package main

import "fmt"

var seed int64 = 2401

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func longestNiceSubarray(nums []int64) int64 {
	var used, left, best int64
	for right := int64(0); right < int64(len(nums)); right++ {
		for used&nums[right] != 0 {
			used ^= nums[left]
			left++
		}
		used |= nums[right]
		if right-left+1 > best {
			best = right - left + 1
		}
	}
	return best
}

func main() {
	arrays := make([][]int64, 20)
	for a := range arrays {
		nums := make([]int64, 100000)
		for i := range nums {
			x := int64(1) << (nextRandom() % 30)
			if nextRandom()%2 == 0 {
				x |= int64(1) << (nextRandom() % 30)
			}
			nums[i] = x
		}
		arrays[a] = nums
	}
	var check int64
	for p := int64(0); p < 20; p++ {
		for _, nums := range arrays {
			check = (check*31 + longestNiceSubarray(nums) + p) % 1000000007
		}
	}
	fmt.Printf("20 passes over 20 arrays of 10^5 values: checksum %d\n", check)
}

// LeetCode #1752: Check if Array Is Sorted and Rotated -- the bench
// (rotated.kara in Go): count the drops.
package main

import (
	"fmt"
	"slices"
)

func checkRotated(nums []int32) bool {
	drops := 0
	for i := 0; i+1 < len(nums); i++ {
		if nums[i] > nums[i+1] {
			drops++
		}
	}
	wrap := 0
	if nums[len(nums)-1] > nums[0] {
		wrap = 1
	}
	return drops+wrap <= 1
}

var seed int64 = 1752

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, n = 100000, 5, 100
	arrays := make([][]int32, count)
	for c := range arrays {
		nums := make([]int32, n)
		for i := range nums {
			nums[i] = int32(nextRandom()%100 + 1)
		}
		if nextRandom()%2 == 0 {
			slices.Sort(nums)
			k := nextRandom() % n
			nums = append(nums[k:], nums[:k]...)
		}
		arrays[c] = nums
	}
	var yes, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			answer := checkRotated(nums)
			var a int64 = 1
			if answer {
				yes++
				a = 2
			}
			check = (check*31 + a + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: %d sorted and rotated, checksum %d\n", count, n, rounds, yes, check)
}

// LeetCode #1121: Divide Array Into Increasing Sequences -- the bench in
// Go: the ★ arm over 4 sorted arrays of 100000 values, each round copying
// one value over its neighbour and answering for a new `k`.
package main

import (
	"fmt"
	"sort"
)

var seed int64 = 1121

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func canDivideIntoSubsequences(nums []int32, k int32) bool {
	var longest, run int64
	for i := range nums {
		if i > 0 && nums[i] == nums[i-1] {
			run++
		} else {
			run = 1
		}
		if run > longest {
			longest = run
		}
	}
	return longest*int64(k) <= int64(len(nums))
}

func main() {
	const n = 100000
	tops := []int64{2000, 1000, 500, 200}
	arrays := make([][]int32, 0, len(tops))
	for _, top := range tops {
		nums := make([]int32, n)
		for i := range nums {
			nums[i] = int32(nextRandom()%top + 1)
		}
		sort.Slice(nums, func(a, b int) bool { return nums[a] < nums[b] })
		arrays = append(arrays, nums)
	}
	var yes, check int64
	for round := 0; round < 250; round++ {
		for j := range arrays {
			at := (round*7919+j*104729)%(n-2) + 1
			if round%2 == 0 {
				arrays[j][at] = arrays[j][at+1]
			} else {
				arrays[j][at] = arrays[j][at-1]
			}
			k := int32((round*13+j*7)%2000 + 1)
			r := canDivideIntoSubsequences(arrays[j], k)
			bit := int64(2)
			if r {
				yes++
				bit = 1
			}
			check = (check*31 + bit + int64(k)) % 1000000007
		}
	}
	fmt.Printf("250 rounds over 4 arrays of 100000 values: %d can be divided, checksum %d\n", yes, check)
}

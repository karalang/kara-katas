// LeetCode #1133: Largest Unique Number -- the bench in Go, the same
// algorithm and workload as largest_unique_number.kara: each array its own
// []int64, a fixed array of 1001 counts per call, the same 256 arrays of
// 2000 values and 1000 rounds.
package main

import "fmt"

func largestUniqueNumber(nums []int64) int64 {
	var count [1001]int64
	for _, x := range nums {
		count[x]++
	}
	for v := 1000; v >= 0; v-- {
		if count[v] == 1 {
			return int64(v)
		}
	}
	return -1
}

var seed int64 = 1133

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 0, 256)
	for j := 0; j < 256; j++ {
		nums := make([]int64, 2000)
		for i := range nums {
			nums[i] = nextRandom() % 1001
		}
		arrays = append(arrays, nums)
	}
	var total, check int64
	for round := int64(0); round < 1000; round++ {
		for j := int64(0); j < 256; j++ {
			at := (round*7919 + j*104729) % 2000
			arrays[j][at] = (arrays[j][at]*7 + 13) % 1001
			r := largestUniqueNumber(arrays[j])
			total += r
			check = (check*31 + r + 1) % 1000000007
		}
	}
	fmt.Printf("1000 rounds over 256 arrays of 2000 values: answers total %d, checksum %d\n", total, check)
}

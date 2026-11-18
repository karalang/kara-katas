// LeetCode #2294: Partition Array Such That Maximum Difference Is K --
// the bench, the ★ arm in Go. Sort a copy, then open a group at each
// number more than k above the one that opened the last.
package main

import (
	"fmt"
	"slices"
)

func partitionArray(nums []int64, k int64) int64 {
	sorted := slices.Clone(nums)
	slices.Sort(sorted)
	var groups, low int64 = 0, -1
	for _, x := range sorted {
		if groups == 0 || x-low > k {
			groups++
			low = x
		}
	}
	return groups
}

var seed int64 = 2294

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 20)
	for a := range arrays {
		nums := make([]int64, 100000)
		for i := range nums {
			hi := nextRandom()
			nums[i] = (hi*32768 + nextRandom()) % 100001
		}
		arrays[a] = nums
	}
	var check int64
	for p := int64(0); p < 5; p++ {
		for a := range arrays {
			check = (check*31 + partitionArray(arrays[a], 7*int64(a)+p)) % 1000000007
		}
	}
	fmt.Printf("5 passes over 20 arrays of 10^5: checksum %d\n", check)
}

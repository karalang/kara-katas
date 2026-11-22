// LeetCode #2870: Minimum Number of Operations to Make Array Empty --
// the bench, as empty.kara: 50 arrays of 10^5 values, each answered 10
// times by the sorted-runs arm.
package main

import (
	"fmt"
	"slices"
)

func minOperations(nums []int64) int64 {
	sorted := slices.Clone(nums)
	slices.Sort(sorted)
	var ops int64
	for i := 0; i < len(sorted); {
		j := i
		for j < len(sorted) && sorted[j] == sorted[i] {
			j++
		}
		f := int64(j - i)
		if f == 1 {
			return -1
		}
		ops += (f + 2) / 3
		i = j
	}
	return ops
}

var seed int64 = 2870

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
		nums := make([]int64, 0, n)
		for len(nums) < n {
			v := wide()%1000000 + 1
			copies := nextRandom()%7 + 2
			if copies > int64(n-len(nums)) {
				copies = int64(n - len(nums))
			}
			for k := int64(0); k < copies; k++ {
				nums = append(nums, v)
			}
		}
		for i := n - 1; i >= 1; i-- {
			j := wide() % int64(i+1)
			nums[i], nums[j] = nums[j], nums[i]
		}
		arrays[c] = nums
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			ops := minOperations(nums)
			total += ops
			check = (check*31 + ops + 1 + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: %d operations, checksum %d\n", count, n, rounds, total, check)
}

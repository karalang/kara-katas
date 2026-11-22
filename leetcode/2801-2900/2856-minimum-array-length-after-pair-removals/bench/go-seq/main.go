// LeetCode #2856: Minimum Array Length After Pair Removals -- the bench:
// the ★ arm over 5000 sorted arrays of 1000 values, each from 1 to k for
// k up to 1000, one time in four with a run of one value making up to
// three quarters, all drawn first, then each answered 50 times.
package main

import (
	"fmt"
	"slices"
)

func minLengthAfterRemovals(nums []int64) int64 {
	n := int64(len(nums))
	var most, run int64
	for i := range nums {
		if i > 0 && nums[i] == nums[i-1] {
			run++
		} else {
			run = 1
		}
		most = max(most, run)
	}
	if 2*most > n {
		return 2*most - n
	}
	return n % 2
}

var seed int64 = 2856

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, n = 5000, 50, 1000
	arrays := make([][]int64, 0, count)
	for a := 0; a < count; a++ {
		k := nextRandom()%1000 + 1
		nums := make([]int64, n)
		for i := range nums {
			nums[i] = nextRandom()%k + 1
		}
		if nextRandom()%4 == 0 {
			run := nextRandom() % (3*n/4 + 1)
			v := nextRandom()%1000 + 1
			for i := int64(0); i < run; i++ {
				nums[i] = v
			}
		}
		slices.Sort(nums)
		arrays = append(arrays, nums)
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			left := minLengthAfterRemovals(nums)
			total += left
			check = (check*31 + left + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays, %d rounds: %d left, checksum %d\n", count, rounds, total, check)
}

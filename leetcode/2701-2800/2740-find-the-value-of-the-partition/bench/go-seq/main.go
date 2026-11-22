// LeetCode #2740: Find the Value of the Partition -- the bench
// (partition.kara in Go): sort a copy, and the least gap between
// neighbours.
package main

import (
	"fmt"
	"math"
	"slices"
)

func findValueOfPartition(nums []int64) int64 {
	slices.Sort(nums)
	best := int64(math.MaxInt64)
	for i := 1; i < len(nums); i++ {
		best = min(best, nums[i]-nums[i-1])
	}
	return best
}

var seed int64 = 2740

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, n, rounds = 20, 100000, 10
	arrays := make([][]int64, 0, count)
	for c := 0; c < count; c++ {
		nums := make([]int64, 0, n)
		for i := 0; i < n; i++ {
			hi := nextRandom()
			lo := nextRandom()
			nums = append(nums, (hi*32768+lo)%1000000000+1)
		}
		arrays = append(arrays, nums)
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			value := findValueOfPartition(slices.Clone(nums))
			sum += value
			check = (check*31 + value + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d numbers, %d rounds: values sum to %d, checksum %d\n", count, n, rounds, sum, check)
}

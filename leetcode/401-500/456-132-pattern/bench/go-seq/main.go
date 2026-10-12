// Benchmark for #456: mirror of pattern132.kara (the ★ arm, one stack
// from the right) on the same workload.
package main

import (
	"fmt"
	"math"
)

func find132pattern(nums []int64) bool {
	stack := make([]int64, 0)
	third := int64(math.MinInt64)
	for i := len(nums) - 1; i >= 0; i-- {
		if nums[i] < third {
			return true
		}
		for len(stack) > 0 && stack[len(stack)-1] < nums[i] {
			third = stack[len(stack)-1]
			stack = stack[:len(stack)-1]
		}
		stack = append(stack, nums[i])
	}
	return false
}

// ---- benchmark --------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const arrays = 10
	const n = 1000000
	const rounds = 5
	var seed int64 = 456
	all := make([][]int64, 0, arrays)
	for a := 0; a < arrays; a++ {
		nums := make([]int64, 0)
		var top int64 = 1000000000
		for int64(len(nums)) < n {
			run := min(1+nextRandom(&seed)%1000, n-int64(len(nums)))
			low := top - run*10 - 1 - nextRandom(&seed)%100
			for t := int64(0); t < run; t++ {
				nums = append(nums, low+t*10+nextRandom(&seed)%10)
			}
			top = low
		}
		all = append(all, nums)
	}
	found := 0
	var checksum int64
	for r := 0; r < rounds; r++ {
		for a := 0; a < arrays; a++ {
			hi := nextRandom(&seed)
			lo := nextRandom(&seed)
			at := (hi*65536 + lo) % n
			old := all[a][at]
			hi = nextRandom(&seed)
			lo = nextRandom(&seed)
			value := (hi*65536+lo)%2000000001 - 1000000000
			if nextRandom(&seed)%2 == 0 {
				all[a][at] = value
			}
			has := find132pattern(all[a])
			all[a][at] = old
			var mark int64
			if has {
				found++
				mark = at + 1
			}
			checksum = (checksum*31 + mark) % 1000000007
		}
	}
	fmt.Printf("%d rounds on %d arrays of %d: %d with the pattern, checksum %d\n", rounds, arrays, n, found, checksum)
}

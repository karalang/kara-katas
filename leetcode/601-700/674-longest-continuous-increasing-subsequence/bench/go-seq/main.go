// Benchmark for #674: one pass with a running length, as the Kara ★
// arm.
package main

import "fmt"

func findLengthOfLCIS(nums []int64) int64 {
	var best, run int64
	for i := 0; i < len(nums); i++ {
		if i > 0 && nums[i-1] < nums[i] {
			run++
		} else {
			run = 1
		}
		if run > best {
			best = run
		}
	}
	return best
}

func main() {
	var arrays int64 = 100
	var size int64 = 10000
	var rounds int64 = 20000
	var seed int64 = 674
	all := make([][]int64, 0)
	for a := int64(0); a < arrays; a++ {
		nums := make([]int64, 0)
		for i := int64(0); i < size; i++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			nums = append(nums, seed/65536%1000)
		}
		all = append(all, nums)
	}
	var sum int64
	for r := int64(0); r < rounds; r++ {
		a := r % arrays
		all[a][r*7919%size] = r % 1000
		sum = (sum*31 + findLengthOfLCIS(all[a])) % 1000000007
	}
	fmt.Printf("%d rounds over %d arrays of %d: checksum %d\n", rounds, arrays, size, sum)
}

// Benchmark for #377: mirror of combination_sum4.kara.
package main

import "fmt"

const capCount int64 = 2147483648

func combinationSum4(nums []int64, target int64) int64 {
	ways := make([]int64, target+1)
	ways[0] = 1
	for t := int64(1); t <= target; t++ {
		for _, x := range nums {
			if x <= t {
				s := ways[t] + ways[t-x]
				if s > capCount {
					s = capCount
				}
				ways[t] = s
			}
		}
	}
	return ways[target]
}

func main() {
	seed := int64(377)
	checksum := int64(0)
	for c := 0; c < 2000; c++ {
		nums := make([]int64, 0, 200)
		for len(nums) < 200 {
			seed = (seed*1103515245 + 12345) % 2147483648
			v := 125 + (seed/65536)%875
			seen := false
			for _, y := range nums {
				if y == v {
					seen = true
					break
				}
			}
			if !seen {
				nums = append(nums, v)
			}
		}
		checksum = (checksum*1009 + combinationSum4(nums, 1000)) % 1000000007
	}
	fmt.Printf("checksum %d\n", checksum)
}

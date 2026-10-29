// LeetCode #1018: Binary Prefix Divisible By 5 -- bench
// Mirrors ../prefix.kara; see ../../README.md § Benchmarks.
package main

import "fmt"

func prefixesDivBy5(nums []int64) []bool {
	answer := []bool{}
	var r int64
	for _, bit := range nums {
		r = (r*2 + bit) % 5
		answer = append(answer, r == 0)
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	var length int64 = 2000000
	var rounds int64 = 50
	var seed int64 = 1018
	nums := []int64{}
	for i := int64(0); i < length; i++ {
		nums = append(nums, nextRandom(&seed)%2)
	}
	var trues, sum int64
	for round := int64(0); round < rounds; round++ {
		at := round * 39989 % length
		nums[at] = 1 - nums[at]
		answer := prefixesDivBy5(nums)
		for i := range answer {
			if answer[i] {
				trues++
				sum = (sum + int64(i)) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over %d bits: %d true, index sum %d\n", rounds, length, trues, sum)
}

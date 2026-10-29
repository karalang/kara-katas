// LeetCode #1027: Longest Arithmetic Subsequence -- bench
// Mirrors ../longest_arith.kara; see ../../README.md § Benchmarks.

package main

import "fmt"

func longestArithSeqLength(nums []int64) int64 {
	n := len(nums)
	run := make([][]int64, n)
	for i := range run {
		run[i] = make([]int64, 1001)
	}
	best := int64(2)
	for i := 1; i < n; i++ {
		for j := 0; j < i; j++ {
			d := nums[i] - nums[j] + 500
			length := int64(2)
			if run[j][d] > 0 {
				length = run[j][d] + 1
			}
			if length > run[i][d] {
				run[i][d] = length
			}
			best = max(best, length)
		}
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds = 40, 3
	tops := []int64{5, 50, 500, 500}
	seed := int64(1027)
	arrays := [][]int64{}
	for k := 0; k < count; k++ {
		nums := make([]int64, 0, 1000)
		for m := 0; m < 1000; m++ {
			nums = append(nums, nextRandom(&seed)%(tops[k%4]+1))
		}
		arrays = append(arrays, nums)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, nums := range arrays {
			answer := longestArithSeqLength(nums)
			total += answer
			check = (check*131 + answer) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 1000 values, %d rounds: sum %d, checksum %d\n", count, rounds, total, check)
}

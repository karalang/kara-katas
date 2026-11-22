// LeetCode #2733: Neither Minimum nor Maximum -- the bench (neither.kara
// in Go): the least and the greatest in one pass, then the first number
// that is neither.
package main

import "fmt"

func findNonMinOrMax(nums []int64) int64 {
	low, high := nums[0], nums[0]
	for _, x := range nums {
		low = min(low, x)
		high = max(high, x)
	}
	for _, x := range nums {
		if x != low && x != high {
			return x
		}
	}
	return -1
}

var seed int64 = 2733

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds = 2000, 3000
	arrays := [][]int64{}
	for k := 0; k < count; k++ {
		n := nextRandom()%100 + 1
		all := make([]int64, 100)
		for i := range all {
			all[i] = int64(i + 1)
		}
		for i := int64(99); i >= 1; i-- {
			j := nextRandom() % (i + 1)
			all[i], all[j] = all[j], all[i]
		}
		arrays = append(arrays, all[:n])
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			answer := findNonMinOrMax(nums)
			sum += answer
			check = (check*31 + answer + 1 + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays, %d rounds: answers sum to %d, checksum %d\n", count, rounds, sum, check)
}

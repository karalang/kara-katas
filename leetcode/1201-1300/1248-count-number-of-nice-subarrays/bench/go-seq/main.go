// LeetCode #1248 bench, in Go: the ★ arm (prefix counts of odd values in
// a slice indexed by count) on 50 random arrays of 50000 values built
// once, each with its own chance of an odd value, each asked with 10
// random k; every answer folded into a checksum.
package main

import "fmt"

func numberOfSubarrays(nums []int64, k int64) int64 {
	prefixes := make([]int64, len(nums)+1)
	prefixes[0] = 1
	var odd, nice int64
	for _, v := range nums {
		odd += v % 2
		if odd >= k {
			nice += prefixes[odd-k]
		}
		prefixes[odd]++
	}
	return nice
}

var seed int64 = 1248

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 0, 50)
	for a := 0; a < 50; a++ {
		percent := nextRandom() % 101
		nums := make([]int64, 0, 50000)
		for i := 0; i < 50000; i++ {
			v := nextRandom()%50000 + 1
			if nextRandom()%100 < percent {
				nums = append(nums, 2*v-1)
			} else {
				nums = append(nums, 2*v)
			}
		}
		arrays = append(arrays, nums)
	}
	var check int64
	for _, nums := range arrays {
		var odd int64
		for _, v := range nums {
			if v%2 == 1 {
				odd++
			}
		}
		for r := 0; r < 100; r++ {
			k := nextRandom()%(odd+1) + 1
			check = (check*131 + numberOfSubarrays(nums, k)) % 1000000007
		}
	}
	fmt.Printf("50 arrays of 50000 values, 100 k each: checksum %d\n", check)
}

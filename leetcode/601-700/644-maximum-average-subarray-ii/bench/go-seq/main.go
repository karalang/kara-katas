// Benchmark for #644: mirror of max_average_ii.kara (the ★ arm: binary
// search on the average) on the same workload.
package main

import "fmt"

// The start and end of a subarray of `k` or more values averaging at
// least `m`, or (-1, -1) if there is none.
func reaches(prefix []int64, k int64, m float64) (int64, int64) {
	var lowest int64 = 0
	for end := k; end < int64(len(prefix)); end++ {
		c := end - k
		if float64(prefix[c]-prefix[lowest]) < m*float64(c-lowest) {
			lowest = c
		}
		if float64(prefix[end]-prefix[lowest]) >= m*float64(end-lowest) {
			return lowest, end
		}
	}
	return -1, -1
}

func findMaxAverage(nums []int64, k int64) float64 {
	prefix := []int64{0}
	for _, x := range nums {
		prefix = append(prefix, prefix[len(prefix)-1]+x)
	}
	lo := float64(nums[0])
	hi := float64(nums[0])
	for _, x := range nums {
		v := float64(x)
		if v < lo {
			lo = v
		}
		if v > hi {
			hi = v
		}
	}
	bestStart, bestEnd := int64(0), int64(len(nums))
	for it := 0; it < 100; it++ {
		mid := (lo + hi) / 2.0
		start, end := reaches(prefix, k, mid)
		if start == -1 {
			hi = mid
		} else {
			lo = mid
			bestStart, bestEnd = start, end
		}
	}
	return float64(prefix[bestEnd]-prefix[bestStart]) / float64(bestEnd-bestStart)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	var seed int64 = 644
	arrays := make([][]int64, 0, 20)
	for a := 0; a < 20; a++ {
		nums := make([]int64, 0, 100000)
		for i := 0; i < 100000; i++ {
			nums = append(nums, nextRandom(&seed)%20001-10000)
		}
		arrays = append(arrays, nums)
	}
	var rounds int64 = 40
	total := 0.0
	for r := int64(0); r < rounds; r++ {
		k := 1 + (r*7919)%100000
		total += findMaxAverage(arrays[r%20], k)
	}
	fmt.Printf("%d rounds over 20 arrays of 100000 values: answers adding to %.5f\n", rounds, total)
}

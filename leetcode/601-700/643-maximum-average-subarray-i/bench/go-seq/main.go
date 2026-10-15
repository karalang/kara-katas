// Benchmark for #643: mirror of max_average.kara (the ★ arm: a sliding
// sum) on the same workload.
package main

import "fmt"

func findMaxAverage(nums []int64, k int) float64 {
	var sum int64
	for i := 0; i < k; i++ {
		sum += nums[i]
	}
	best := sum
	for i := k; i < len(nums); i++ {
		sum += nums[i] - nums[i-k]
		if sum > best {
			best = sum
		}
	}
	return float64(best) / float64(k)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(643)
	arrays := [][]int64{}
	for a := 0; a < 20; a++ {
		nums := make([]int64, 0, 100000)
		for i := 0; i < 100000; i++ {
			nums = append(nums, nextRandom(&seed)%20001-10000)
		}
		arrays = append(arrays, nums)
	}
	rounds := 4000
	total := 0.0
	for r := 0; r < rounds; r++ {
		k := 1 + (r*7919)%100000
		total += findMaxAverage(arrays[r%20], k)
	}
	fmt.Printf("%d rounds over 20 arrays of 100000 values: answers adding to %.5f\n", rounds, total)
}

// LeetCode #719: Find K-th Smallest Pair Distance -- binary search on
// the distance. Benchmark mirror of the Kara star arm: sort a copy,
// then find the least distance with at least k pairs, counting pairs
// with two pointers.
package main

import (
	"fmt"
	"slices"
)

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func smallestDistancePair(nums []int64, k int64) int64 {
	sorted := slices.Clone(nums)
	slices.Sort(sorted)
	n := len(sorted)
	lo, hi := int64(0), sorted[n-1]-sorted[0]
	for lo < hi {
		mid := (lo + hi) / 2
		count := int64(0)
		left := 0
		for right := 0; right < n; right++ {
			for sorted[right]-sorted[left] > mid {
				left++
			}
			count += int64(right - left)
		}
		if count >= k {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

func main() {
	seed := int64(719)
	var arrays [][]int64
	for a := 0; a < 40; a++ {
		nums := make([]int64, 5000)
		for i := range nums {
			hi := nextRandom(&seed)
			lo := nextRandom(&seed)
			nums[i] = (hi*32768 + lo) % 1000001
		}
		arrays = append(arrays, nums)
	}
	pairs := int64(5000 * 4999 / 2)
	sum := int64(0)
	for round := int64(0); round < 25; round++ {
		for a := int64(0); a < 40; a++ {
			k := 1 + (round*7919+a*104729)%pairs
			sum += smallestDistancePair(arrays[a], k)
		}
	}
	fmt.Printf("25 rounds of 40 arrays of 5000 numbers: sum %d\n", sum)
}

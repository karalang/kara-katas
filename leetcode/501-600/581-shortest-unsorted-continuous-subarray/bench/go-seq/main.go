// Benchmark for #581: Go mirror of the ★ arm (two sweeps); see
// ../find_unsorted_subarray.kara.
package main

import (
	"fmt"
	"slices"
)

func findUnsortedSubarray(nums []int64) int64 {
	n := int64(len(nums))
	largest := nums[0]
	var end int64 = -1
	for i := int64(1); i < n; i++ {
		if nums[i] < largest {
			end = i
		} else {
			largest = nums[i]
		}
	}
	smallest := nums[n-1]
	var start int64 = 0
	for i := n - 2; i >= 0; i-- {
		if nums[i] > smallest {
			start = i
		} else {
			smallest = nums[i]
		}
	}
	if end == -1 {
		return 0
	}
	return end - start + 1
}

// ---- benchmark --------------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	high := nextRandom(seed) * 32768
	return high + nextRandom(seed)
}

func main() {
	var count int64 = 100
	var rounds int64 = 600
	var seed int64 = 581
	cases := make([][]int64, 0, count)
	for g := int64(0); g < count; g++ {
		nums := make([]int64, 0, 10000)
		for i := 0; i < 10000; i++ {
			nums = append(nums, wide(&seed)%200001-100000)
		}
		slices.Sort(nums)
		swaps := 1 + nextRandom(&seed)%3
		for s := int64(0); s < swaps; s++ {
			i := wide(&seed) % 10000
			j := wide(&seed) % 10000
			nums[i], nums[j] = nums[j], nums[i]
		}
		cases = append(cases, nums)
	}
	var total int64 = 0
	var checksum int64 = 0
	for round := int64(0); round < rounds; round++ {
		for g := int64(0); g < count; g++ {
			p := (round*7 + g) % count
			got := findUnsortedSubarray(cases[p])
			total += got
			checksum = (checksum*31 + got) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 10000 values, %d rounds: total %d, checksum %d\n", count, rounds, total, checksum)
}

// LeetCode #718: Maximum Length of Repeated Subarray -- one rolling row.
// Benchmark mirror of the Kara star arm: the length of the common run
// ending at each pair of places, one row at a time, walked downwards.
package main

import "fmt"

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func findLength(nums1, nums2 []int64) int64 {
	m, n := len(nums1), len(nums2)
	run := make([]int64, n+1)
	best := int64(0)
	for i := 1; i <= m; i++ {
		for j := n; j >= 1; j-- {
			if nums1[i-1] == nums2[j-1] {
				run[j] = run[j-1] + 1
				if run[j] > best {
					best = run[j]
				}
			} else {
				run[j] = 0
			}
		}
	}
	return best
}

func main() {
	seed := int64(718)
	var arrays [][]int64
	for a := 0; a < 60; a++ {
		nums := make([]int64, 1000)
		for i := range nums {
			nums[i] = nextRandom(&seed) % 10
		}
		arrays = append(arrays, nums)
	}
	sum := int64(0)
	for round := 0; round < 40; round++ {
		for k := 0; k < 20; k++ {
			sum += findLength(arrays[k], arrays[(k+round+1)%60])
		}
	}
	fmt.Printf("40 rounds of 20 pairs of 1000 numbers: sum %d\n", sum)
}

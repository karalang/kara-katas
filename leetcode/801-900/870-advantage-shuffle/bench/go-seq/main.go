// LeetCode #870: Advantage Shuffle -- Go mirror of the bench program (the
// ★ arm, greedy from the largest), with a stable sort of the indices as
// in the Kāra program.
package main

import (
	"fmt"
	"sort"
)

func advantageCount(nums1, nums2 []int64) []int64 {
	n := len(nums1)
	sorted := append([]int64(nil), nums1...)
	sort.Slice(sorted, func(a, b int) bool { return sorted[a] < sorted[b] })
	order := make([]int, n)
	for i := range order {
		order[i] = i
	}
	sort.SliceStable(order, func(a, b int) bool { return nums2[order[a]] > nums2[order[b]] })
	result := make([]int64, n)
	lo, hi := 0, n-1
	for _, i := range order {
		if sorted[hi] > nums2[i] {
			result[i] = sorted[hi]
			hi--
		} else {
			result[i] = sorted[lo]
			lo++
		}
	}
	return result
}

var seed int64 = 870

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomVec(n int) []int64 {
	v := make([]int64, n)
	for i := range v {
		hi := nextRandom()
		lo := nextRandom()
		v[i] = (hi*32768 + lo) % 1000000001
	}
	return v
}

func main() {
	var wins, check int64
	for r := 0; r < 20; r++ {
		nums1 := randomVec(100000)
		nums2 := randomVec(100000)
		result := advantageCount(nums1, nums2)
		for i := range result {
			if result[i] > nums2[i] {
				wins++
			}
			check = (check + result[i]*int64(i+1)) % 1000000007
		}
	}
	fmt.Printf("20 pairs of 100000 values: %d wins, checksum %d\n", wins, check)
}

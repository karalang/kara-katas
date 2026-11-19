// LeetCode #2333: Minimum Sum of Squared Difference -- the bench, the ★
// arm in Go: the gaps counted by size, the largest dropped a level at a
// time while the moves cover them, and the moves left taking that many
// of the rest one lower.
package main

import "fmt"

func minSumSquareDiff(nums1, nums2 []int64, k1, k2 int64) int64 {
	count := make([]int64, 100001)
	var top int64
	for i := range nums1 {
		gap := nums1[i] - nums2[i]
		if gap < 0 {
			gap = -gap
		}
		count[gap]++
		if gap > top {
			top = gap
		}
	}
	moves := k1 + k2
	level := top
	for level > 0 && moves >= count[level] {
		moves -= count[level]
		count[level-1] += count[level]
		count[level] = 0
		level--
	}
	if level > 0 {
		count[level] -= moves
		count[level-1] += moves
	}
	var total int64
	for gap := int64(1); gap <= level; gap++ {
		total += count[gap] * gap * gap
	}
	return total
}

func scrambled(index int64) int64 {
	return index * 2654435761 % 2147483647
}

func main() {
	nums1 := make([][]int64, 10)
	nums2 := make([][]int64, 10)
	for c := int64(0); c < 10; c++ {
		nums1[c] = make([]int64, 20000)
		nums2[c] = make([]int64, 20000)
		for i := int64(0); i < 20000; i++ {
			nums1[c][i] = scrambled(c*40000+i) % 100001
			nums2[c][i] = scrambled(c*40000+20000+i) % 100001
		}
	}
	var check int64
	for p := int64(0); p < 10; p++ {
		for c := int64(0); c < 10; c++ {
			k1 := (10*c + p) * 3000000 % 400000000
			k2 := (7*p + c) * 5000000 % 300000000
			check = (check*31 + minSumSquareDiff(nums1[c], nums2[c], k1, k2)) % 1000000007
		}
	}
	fmt.Printf("10 passes over 10 cases of 2*10^4 pairs: checksum %d\n", check)
}

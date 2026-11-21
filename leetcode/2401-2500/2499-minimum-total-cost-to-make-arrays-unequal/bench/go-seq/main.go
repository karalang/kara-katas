// LeetCode #2499: Minimum Total Cost to Make Arrays Unequal -- Go mirror
// of the benchmark (unequal.kara): the same pairs, passes and checksum.
package main

import "fmt"

var seed int64 = 2499

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func minimumTotalCost(nums1, nums2 []int64) int64 {
	n := int64(len(nums1))
	count := make([]int64, n+1)
	var equal, cost int64
	for i := int64(0); i < n; i++ {
		if nums1[i] == nums2[i] {
			count[nums1[i]]++
			equal++
			cost += i
		}
	}
	var mode int64
	for v := int64(1); v <= n; v++ {
		if count[v] > count[mode] {
			mode = v
		}
	}
	short := 2*count[mode] - equal
	for j := int64(0); j < n && short > 0; j++ {
		if nums1[j] != nums2[j] && nums1[j] != mode && nums2[j] != mode {
			cost += j
			short--
		}
	}
	if short > 0 {
		return -1
	}
	return cost
}

func main() {
	const n int64 = 100000
	const passes int64 = 33
	firsts := make([][]int64, 20)
	seconds := make([][]int64, 20)
	for q := 0; q < 20; q++ {
		nums1 := make([]int64, n)
		nums2 := make([]int64, n)
		for i := int64(0); i < n; i++ {
			a := nextRandom()%4 + 1
			nums1[i] = a
			if nextRandom()%2 == 0 {
				nums2[i] = a
			} else {
				nums2[i] = nextRandom()%4 + 1
			}
		}
		firsts[q] = nums1
		seconds[q] = nums2
	}
	var check int64
	for p := int64(0); p < passes; p++ {
		for q := 0; q < 20; q++ {
			at := check % n
			was := seconds[q][at]
			if (check/n+p)%2 == 0 {
				seconds[q][at] = firsts[q][at]
			} else {
				seconds[q][at] = check%4 + 1
			}
			check = (check*31 + minimumTotalCost(firsts[q], seconds[q]) + 1 + p) % 1000000007
			seconds[q][at] = was
		}
	}
	fmt.Printf("%d passes over 20 pairs of 10^5: checksum %d\n", passes, check)
}

// LeetCode #2426: Number of Pairs Satisfying Inequality -- the bench, the
// ★ arm: with `a[i] = nums1[i] - nums2[i]`, a merge sort counting the
// pairs `i < j` with `a[i] <= a[j] + diff`.
package main

import "fmt"

func countPairs(a []int64, lo, hi int, diff int64) int64 {
	if hi-lo < 2 {
		return 0
	}
	mid := (lo + hi) / 2
	count := countPairs(a, lo, mid, diff) + countPairs(a, mid, hi, diff)
	p := lo
	for j := mid; j < hi; j++ {
		for p < mid && a[p] <= a[j]+diff {
			p++
		}
		count += int64(p - lo)
	}
	var merged []int64
	i, j := lo, mid
	for i < mid || j < hi {
		if j == hi || (i < mid && a[i] <= a[j]) {
			merged = append(merged, a[i])
			i++
		} else {
			merged = append(merged, a[j])
			j++
		}
	}
	copy(a[lo:hi], merged)
	return count
}

func numberOfPairs(nums1, nums2 []int64, diff int64) int64 {
	var a []int64
	for i := range nums1 {
		a = append(a, nums1[i]-nums2[i])
	}
	return countPairs(a, 0, len(a), diff)
}

var seed int64 = 2426

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var firsts, seconds [][]int64
	for c := 0; c < 10; c++ {
		var nums1, nums2 []int64
		for k := 0; k < 100000; k++ {
			nums1 = append(nums1, nextRandom()%20001-10000)
			nums2 = append(nums2, nextRandom()%20001-10000)
		}
		firsts = append(firsts, nums1)
		seconds = append(seconds, nums2)
	}
	var check int64
	for p := int64(0); p < 4; p++ {
		for c := 0; c < 10; c++ {
			diff := 2000*int64(c) - 10000 + p - 2
			check = (check*31 + numberOfPairs(firsts[c], seconds[c], diff) + p) % 1000000007
		}
	}
	fmt.Printf("4 passes over 10 cases of 10^5 values: checksum %d\n", check)
}

// LeetCode #1537: Get the Maximum Score -- bench: the ★ arm over 100
// random pairs of arrays built from 100000 values each, steps up to 50,
// built once and answered 20 times. Go mirror of score.kara.
package main

import "fmt"

func maxSum(nums1, nums2 []int64) int64 {
	n, m := len(nums1), len(nums2)
	i, j := 0, 0
	var a, b int64
	for i < n || j < m {
		if i < n && (j == m || nums1[i] < nums2[j]) {
			a += nums1[i]
			i++
		} else if j < m && (i == n || nums2[j] < nums1[i]) {
			b += nums2[j]
			j++
		} else {
			best := max(a, b) + nums1[i]
			a, b = best, best
			i++
			j++
		}
	}
	return max(a, b) % 1000000007
}

var seed int64 = 1537

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func arrays(count, gap int64) ([]int64, []int64) {
	var first, second []int64
	var value int64
	both := nextRandom()%30 + 1
	for k := int64(0); k < count; k++ {
		value += nextRandom()%gap + 1
		roll := nextRandom() % 100
		if roll < both {
			first = append(first, value)
			second = append(second, value)
		} else if roll < 50+both/2 {
			first = append(first, value)
		} else {
			second = append(second, value)
		}
	}
	if len(first) == 0 {
		first = append(first, value+1)
	}
	if len(second) == 0 {
		second = append(second, value+2)
	}
	return first, second
}

func main() {
	firsts := make([][]int64, 100)
	seconds := make([][]int64, 100)
	for k := 0; k < 100; k++ {
		firsts[k], seconds[k] = arrays(100000, 50)
	}
	var check int64
	for pass := 0; pass < 20; pass++ {
		for k := 0; k < 100; k++ {
			check = mix(check, maxSum(firsts[k], seconds[k]))
		}
	}
	fmt.Printf("20 passes over 100 pairs of 100000 values: checksum %d\n", check)
}

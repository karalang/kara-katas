// LeetCode #2407: Longest Increasing Subsequence II -- the bench, the ★
// arm in Go: a bottom-up segment tree over the values, the longest ending
// at x one more than the tree's maximum over x - k to x - 1.

package main

import "fmt"

var seed int64 = 2407

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func lengthOfLIS(nums []int64, k int64) int64 {
	top := nums[0]
	for _, x := range nums {
		top = max(top, x)
	}
	size := int64(1)
	for size <= top {
		size *= 2
	}
	tree := make([]int64, 2*size)
	best := int64(0)
	for _, x := range nums {
		lo, hi, longest := max(x-k, 0)+size, x-1+size+1, int64(0)
		for lo < hi {
			if lo%2 == 1 {
				longest = max(longest, tree[lo])
				lo++
			}
			if hi%2 == 1 {
				hi--
				longest = max(longest, tree[hi])
			}
			lo /= 2
			hi /= 2
		}
		at := x + size
		tree[at] = max(tree[at], longest+1)
		best = max(best, longest+1)
		for at /= 2; at > 0; at /= 2 {
			tree[at] = max(tree[2*at], tree[2*at+1])
		}
	}
	return best
}

func main() {
	arrays := make([][]int64, 5)
	for i := range arrays {
		nums := make([]int64, 100000)
		for j := range nums {
			nums[j] = 1 + (nextRandom()*32768+nextRandom())%100000
		}
		arrays[i] = nums
	}
	var check int64
	for p := int64(0); p < 4; p++ {
		k := int64(1)
		for _, nums := range arrays {
			check = (check*31 + lengthOfLIS(nums, k) + p) % 1000000007
			k *= 10
		}
	}
	fmt.Printf("4 passes over 5 arrays of 10^5 values: checksum %d\n", check)
}

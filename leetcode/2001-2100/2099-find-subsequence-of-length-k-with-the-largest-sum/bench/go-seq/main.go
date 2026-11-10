// LeetCode #2099: Find Subsequence of Length K With the Largest Sum -- Go
// mirror of the ★ arm's benchmark (largest_sum.kara): the same 20000 lists
// of 1000 numbers, the positions sorted by value and the chosen put back
// in order.
package main

import (
	"fmt"
	"sort"
)

func maxSubsequence(nums []int64, k int) []int64 {
	order := make([]int, len(nums))
	for i := range order {
		order[i] = i
	}
	sort.Slice(order, func(x, y int) bool {
		a, b := order[x], order[y]
		if nums[a] != nums[b] {
			return nums[a] > nums[b]
		}
		return a < b
	})
	chosen := append([]int(nil), order[:k]...)
	sort.Ints(chosen)
	out := make([]int64, k)
	for j, i := range chosen {
		out[j] = nums[i]
	}
	return out
}

var seed int64 = 2099

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

func main() {
	total := 0
	var check int64
	for r := 0; r < 20000; r++ {
		nums := make([]int64, 1000)
		for i := range nums {
			nums[i] = wideRandom()%200001 - 100000
		}
		k := int(nextRandom()%1000 + 1)
		got := maxSubsequence(nums, k)
		total += len(got)
		for _, x := range got {
			check = (check*31 + x + 100000) % 1000000007
		}
	}
	fmt.Printf("20000 answers: %d numbers, checksum %d\n", total, check)
}

// LeetCode #2817: Minimum Absolute Difference Between Elements With
// Constraint -- the bench in Go: the ★ arm over 10 arrays of 10^5
// distinct numbers up to 10^9, shuffled, x from 0 to 10^5 - 1, all drawn
// first, then each answered 3 times. Go's library has no ordered set, so
// the window is a slice kept in order by `slices.BinarySearch` and
// `slices.Insert`, as Python's `bisect.insort` does.
package main

import (
	"fmt"
	"math"
	"slices"
)

func minAbsoluteDifference(nums []int64, x int) int64 {
	behind := make([]int64, 0, len(nums))
	best := int64(math.MaxInt64)
	for i := x; i < len(nums); i++ {
		w := nums[i-x]
		at, _ := slices.BinarySearch(behind, w)
		behind = slices.Insert(behind, at, w)
		v := nums[i]
		k, _ := slices.BinarySearch(behind, v)
		if k < len(behind) {
			best = min(best, behind[k]-v)
		}
		if k > 0 {
			best = min(best, v-behind[k-1])
		}
		if best == 0 {
			break
		}
	}
	return best
}

var seed int64 = 2817

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	count, rounds := 10, 3
	var n int64 = 100000
	cases := make([][]int64, count)
	xs := make([]int, count)
	for c := range cases {
		nums := make([]int64, n)
		for i := range nums {
			nums[i] = int64(i)*10000 + wide()%10000 + 1
		}
		for i := n - 1; i >= 1; i-- {
			j := wide() % (i + 1)
			nums[i], nums[j] = nums[j], nums[i]
		}
		cases[c] = nums
		xs[c] = int(wide() % n)
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := range cases {
			a := minAbsoluteDifference(cases[c], xs[c])
			total += a
			check = (check*31 + a + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: differences sum to %d, checksum %d\n", count, n, rounds, total, check)
}

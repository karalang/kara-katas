// LeetCode #2809: Minimum Time to Make Array Sum At Most x -- the bench in
// Go: the ★ arm over 20 cases of 1000 pairs, nums1 up to 1000 and nums2
// up to 2, x from 3 * 10^5 to 5 * 10^5, all drawn first, then each
// answered 20 times.
package main

import (
	"fmt"
	"sort"
)

type pair struct{ b, a int64 }

func minimumTime(nums1, nums2 []int64, x int64) int64 {
	n := len(nums1)
	pairs := make([]pair, n)
	for i := range pairs {
		pairs[i] = pair{nums2[i], nums1[i]}
	}
	sort.Slice(pairs, func(i, j int) bool {
		if pairs[i].b != pairs[j].b {
			return pairs[i].b < pairs[j].b
		}
		return pairs[i].a < pairs[j].a
	})
	best := make([]int64, n+1)
	for i, p := range pairs {
		for j := i + 1; j >= 1; j-- {
			if take := best[j-1] + p.a + int64(j)*p.b; take > best[j] {
				best[j] = take
			}
		}
	}
	var sum1, sum2 int64
	for i := 0; i < n; i++ {
		sum1 += nums1[i]
		sum2 += nums2[i]
	}
	for t := 0; t <= n; t++ {
		if sum1+int64(t)*sum2-best[t] <= x {
			return int64(t)
		}
	}
	return -1
}

var seed int64 = 2809

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count := 20
	rounds := 20
	nums1 := make([][]int64, count)
	nums2 := make([][]int64, count)
	xs := make([]int64, count)
	for c := 0; c < count; c++ {
		nums1[c] = make([]int64, 1000)
		for i := range nums1[c] {
			nums1[c][i] = nextRandom() % 1001
		}
		nums2[c] = make([]int64, 1000)
		for i := range nums2[c] {
			nums2[c][i] = nextRandom() % 3
		}
		xs[c] = 300000 + (nextRandom()*32768+nextRandom())%200000
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := 0; c < count; c++ {
			a := minimumTime(nums1[c], nums2[c], xs[c])
			total += a
			check = (check*31 + a + 1 + r) % 1000000007
		}
	}
	fmt.Printf("%d cases of 1000 pairs, %d rounds: times sum to %d, checksum %d\n", count, rounds, total, check)
}

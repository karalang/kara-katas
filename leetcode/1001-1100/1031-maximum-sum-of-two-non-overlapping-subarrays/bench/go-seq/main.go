// LeetCode #1031: Maximum Sum of Two Non-Overlapping Subarrays -- bench
// Mirrors ../max_two.kara; see ../../README.md § Benchmarks.

package main

import "fmt"

func maxSumTwoNoOverlap(nums []int64, firstLen, secondLen int) int64 {
	n := len(nums)
	prefix := make([]int64, n+1)
	for i := 0; i < n; i++ {
		prefix[i+1] = prefix[i] + nums[i]
	}
	var best, bestFirst, bestSecond int64
	for i := firstLen + secondLen; i <= n; i++ {
		bestFirst = max(bestFirst, prefix[i-secondLen]-prefix[i-secondLen-firstLen])
		bestSecond = max(bestSecond, prefix[i-firstLen]-prefix[i-firstLen-secondLen])
		best = max(best, bestFirst+prefix[i]-prefix[i-secondLen], bestSecond+prefix[i]-prefix[i-firstLen])
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

type kase struct {
	nums                []int64
	firstLen, secondLen int
}

func main() {
	const count, rounds = 1000, 200
	seed := int64(1031)
	cases := []kase{}
	for k := 0; k < count; k++ {
		nums := []int64{}
		for i := 0; i < 1000; i++ {
			nums = append(nums, nextRandom(&seed)%1001)
		}
		firstLen := int(nextRandom(&seed)%999 + 1)
		secondLen := int(nextRandom(&seed)%int64(1000-firstLen) + 1)
		cases = append(cases, kase{nums, firstLen, secondLen})
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, c := range cases {
			answer := maxSumTwoNoOverlap(c.nums, c.firstLen, c.secondLen)
			total += answer
			check = (check*131 + answer) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 1000 values, %d rounds: sum %d, checksum %d\n", count, rounds, total, check)
}

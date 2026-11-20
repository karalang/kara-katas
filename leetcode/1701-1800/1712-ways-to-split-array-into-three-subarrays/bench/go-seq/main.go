// LeetCode #1712: Ways to Split Array Into Three Subarrays -- the Go
// mirror of the bench (split.kara): prefix sums, and for each end of the
// left part two `sort.Search` binary searches, on 20 random arrays of
// 100000 values, each answered 10 times.
package main

import (
	"fmt"
	"sort"
)

func waysToSplit(nums []int32) int32 {
	n := len(nums)
	prefix := make([]int64, 1, n+1)
	for _, x := range nums {
		prefix = append(prefix, prefix[len(prefix)-1]+int64(x))
	}
	total := prefix[n]
	var ways int64
	for i := 1; i < n-1; i++ {
		left := prefix[i]
		lo := max(sort.Search(len(prefix), func(k int) bool { return prefix[k] >= 2*left }), i+1)
		hi := min(sort.Search(len(prefix), func(k int) bool { return 2*prefix[k] > total+left }), n)
		if hi > lo {
			ways += int64(hi - lo)
		}
	}
	return int32(ways % 1000000007)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 20
	var rounds int64 = 10
	n := 100000
	var seed int64 = 1712
	arrays := make([][]int32, count)
	for p := 0; p < count; p++ {
		arrays[p] = make([]int32, n)
		for i := 0; i < n; i++ {
			arrays[p][i] = int32(nextRandom(&seed) % 10001)
		}
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			answer := int64(waysToSplit(nums))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: answers sum to %d, checksum %d\n", count, n, rounds, sum, check)
}

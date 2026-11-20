// LeetCode #1695: Maximum Erasure Value -- the bench's Go mirror: the ★ arm
// on 50 random arrays of 100000 values up to 10^4, all drawn first, each
// answered 60 times.
package main

import "fmt"

func maximumUniqueSubarray(nums []int32) int32 {
	last := make([]int64, 10001)
	for i := range last {
		last[i] = -1
	}
	prefix := make([]int32, len(nums)+1)
	var start int64
	var best int32
	for i, v := range nums {
		prefix[i+1] = prefix[i] + v
		start = max(start, last[v]+1)
		last[v] = int64(i)
		best = max(best, prefix[i+1]-prefix[start])
	}
	return best
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1695

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, n = 50, 60, 100000
	arrays := make([][]int32, count)
	for c := range arrays {
		arrays[c] = make([]int32, n)
		for i := range arrays[c] {
			arrays[c][i] = int32(nextRandom()%10000 + 1)
		}
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			answer := int64(maximumUniqueSubarray(nums))
			total += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: answers sum to %d, checksum %d\n", count, n, rounds, total, check)
}

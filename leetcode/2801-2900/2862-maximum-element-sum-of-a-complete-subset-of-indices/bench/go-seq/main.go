// LeetCode #2862: Maximum Element-Sum of a Complete Subset of Indices --
// the bench: the ★ arm over 200 arrays of 10^4 values up to 10^9,
// LeetCode's most, all drawn first, then each answered 50 times.
package main

import "fmt"

func maximumSum(nums []int64) int64 {
	n := len(nums)
	var best int64
	for k := 1; k <= n; k++ {
		var sum int64
		for j := 1; k*j*j <= n; j++ {
			sum += nums[k*j*j-1]
		}
		best = max(best, sum)
	}
	return best
}

var seed int64 = 2862

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	const count, rounds, n = 200, 50, 10000
	arrays := make([][]int64, count)
	for c := range arrays {
		arrays[c] = make([]int64, n)
		for i := range arrays[c] {
			arrays[c][i] = wide()%1000000000 + 1
		}
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			best := maximumSum(nums)
			total += best
			check = (check*31 + best%1000000007 + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: best sums total %d, checksum %d\n", count, n, rounds, total, check)
}

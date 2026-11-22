// LeetCode #2873: Maximum Value of an Ordered Triplet I -- the bench, as
// triplet.kara: 100000 arrays of 100 values, each answered 30 times by
// the one-pass arm.
package main

import "fmt"

func maximumTripletValue(nums []int64) int64 {
	var best, top, gap int64
	for _, v := range nums {
		best = max(best, gap*v)
		gap = max(gap, top-v)
		top = max(top, v)
	}
	return best
}

var seed int64 = 2873

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	const count, rounds, n = 100000, 30, 100
	arrays := make([][]int64, count)
	for c := range arrays {
		nums := make([]int64, n)
		for i := range nums {
			nums[i] = wide()%1000000 + 1
		}
		arrays[c] = nums
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			best := maximumTripletValue(nums)
			total += best
			check = (check*31 + best%1000000007 + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: values total %d, checksum %d\n", count, n, rounds, total, check)
}

// LeetCode #2874: Maximum Value of an Ordered Triplet II -- the bench, as
// triplet.kara: 50 arrays of 10^5 values, each answered 20 times by the
// one-pass arm.
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

var seed int64 = 2874

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	const count, rounds, n = 50, 20, 100000
	arrays := make([][]int64, count)
	for c := range arrays {
		nums := make([]int64, n)
		for i := range nums {
			if c%2 == 1 {
				nums[i] = max(1000000-int64(i)*9-wide()%100000, 1)
			} else {
				nums[i] = wide()%1000000 + 1
			}
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

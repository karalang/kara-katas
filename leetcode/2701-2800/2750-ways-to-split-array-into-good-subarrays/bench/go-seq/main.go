// LeetCode #2750: Ways to Split Array Into Good Subarrays -- the bench
// (splits.kara in Go): the product of the distances between neighbouring
// 1s, mod 10^9 + 7.
package main

import "fmt"

const mod int64 = 1000000007

func numberOfGoodSubarraySplits(nums []int64) int64 {
	ways, last := int64(1), int64(-1)
	for i, x := range nums {
		if x == 1 {
			if last >= 0 {
				ways = ways * (int64(i) - last) % mod
			}
			last = int64(i)
		}
	}
	if last < 0 {
		return 0
	}
	return ways
}

var seed int64 = 2750

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds = 50, 20
	arrays := make([][]int64, count)
	for k := range arrays {
		percent := nextRandom()%30 + 1
		nums := make([]int64, 100000)
		for i := range nums {
			if nextRandom()%100 < percent {
				nums[i] = 1
			}
		}
		arrays[k] = nums
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			ways := numberOfGoodSubarraySplits(nums)
			sum += ways
			check = (check*31 + ways + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 100000, %d rounds: ways sum to %d, checksum %d\n", count, rounds, sum, check)
}

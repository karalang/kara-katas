// LeetCode #2835: Minimum Operations to Form Subsequence With Target Sum
// -- the bench, mirrored from ops.kara: counts by bit, low to high.
package main

import (
	"fmt"
	"math/bits"
)

func minOperations(nums []int64, target int64) int64 {
	var sum int64
	for _, x := range nums {
		sum += x
	}
	if sum < target {
		return -1
	}
	count := make([]int64, 32)
	for _, x := range nums {
		count[bits.TrailingZeros64(uint64(x))]++
	}
	var ops int64
	for i := 0; i < 31; i++ {
		if (target>>i)&1 == 1 {
			if count[i] > 0 {
				count[i]--
			} else {
				j := i + 1
				for count[j] == 0 {
					j++
				}
				ops += int64(j - i)
				count[j]--
				for k := i; k < j; k++ {
					count[k]++
				}
			}
		}
		count[i+1] += count[i] / 2
	}
	return ops
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

type kase struct {
	nums   []int64
	target int64
}

func main() {
	const count, rounds, n = 2000, 200, 1000
	seed := int64(2835)
	cases := make([]kase, 0, count)
	for c := 0; c < count; c++ {
		nums := make([]int64, n)
		for i := range nums {
			nums[i] = int64(1) << (nextRandom(&seed)%15 + 16)
		}
		hi := nextRandom(&seed)
		target := (hi*32768+nextRandom(&seed))%2147483647 + 1
		cases = append(cases, kase{nums, target})
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, k := range cases {
			ops := minOperations(k.nums, k.target)
			total += ops
			check = (check*31 + ops + 1 + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: operations total %d, checksum %d\n", count, n, rounds, total, check)
}

// LeetCode #2859: Sum of Values at Indices With K Set Bits -- the
// bench: the ★ arm over 2000 arrays of 1000 values up to 10^5,
// LeetCode's most, with k up to 10, all drawn first, then each answered
// 100 times.
package main

import (
	"fmt"
	"math/bits"
)

func sumIndicesWithKSetBits(nums []int64, k int64) int64 {
	var sum int64
	for i, x := range nums {
		if int64(bits.OnesCount(uint(i))) == k {
			sum += x
		}
	}
	return sum
}

var seed int64 = 2859

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	const count, rounds = 2000, 100
	nums := make([][]int64, count)
	ks := make([]int64, count)
	for c := 0; c < count; c++ {
		ks[c] = nextRandom() % 11
		nums[c] = make([]int64, 1000)
		for i := range nums[c] {
			nums[c][i] = wide()%100000 + 1
		}
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			sum := sumIndicesWithKSetBits(nums[c], ks[c])
			total += sum
			check = (check*31 + sum + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays, %d rounds: sums total %d, checksum %d\n", count, rounds, total, check)
}

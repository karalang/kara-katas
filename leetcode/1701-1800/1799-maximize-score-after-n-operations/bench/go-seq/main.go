// LeetCode #1799: Maximize Score After N Operations -- the bench in Go: the
// ★ arm over 100 random lists of 14 numbers built once, 100 calls.
package main

import (
	"fmt"
	"math/bits"
)

func gcd(a, b int32) int32 {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}

func maxScore(nums []int32) int32 {
	m := int64(len(nums))
	full := int64(1) << m
	best := make([]int32, full)
	for mask := int64(0); mask < full; mask++ {
		taken := int64(bits.OnesCount64(uint64(mask)))
		if taken%2 == 1 {
			continue
		}
		op := int32(taken/2 + 1)
		for i := int64(0); i < m; i++ {
			if mask>>i&1 == 1 {
				continue
			}
			for j := i + 1; j < m; j++ {
				if mask>>j&1 == 1 {
					continue
				}
				next := mask | 1<<i | 1<<j
				best[next] = max(best[next], best[mask]+op*gcd(nums[i], nums[j]))
			}
		}
	}
	return best[full-1]
}

var seed int64 = 1799

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]int32, 100)
	for l := range lists {
		lists[l] = make([]int32, 14)
		for x := range lists[l] {
			lists[l][x] = int32(1 + nextRandom()%1000000)
		}
	}
	var check int64
	for call := int64(0); call < 100; call++ {
		check = (check*31 + int64(maxScore(lists[(check+call)%100]))) % 1000000007
	}
	fmt.Printf("100 calls over 100 lists of 14 numbers: checksum %d\n", check)
}

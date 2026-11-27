// LeetCode #1798: Maximum Number of Consecutive Values You Can Make -- the
// bench in Go: the ★ arm over 200 random lists of 2000 coins built once,
// 20000 calls.
package main

import (
	"fmt"
	"slices"
)

func getMaximumConsecutive(coins []int32) int32 {
	sorted := slices.Clone(coins)
	slices.Sort(sorted)
	var reach int32
	for _, c := range sorted {
		if c > reach+1 {
			break
		}
		reach += c
	}
	return reach + 1
}

var seed int64 = 1798

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]int32, 200)
	for l := range lists {
		lists[l] = make([]int32, 2000)
		for x := range lists[l] {
			lists[l][x] = int32(1 + nextRandom()%200)
		}
	}
	var check int64
	for call := int64(0); call < 20000; call++ {
		check = (check*31 + int64(getMaximumConsecutive(lists[(check+call)%200]))) % 1000000007
	}
	fmt.Printf("20000 calls over 200 lists of 2000 coins: checksum %d\n", check)
}

// LeetCode #1186: Maximum Subarray Sum with One Deletion -- the ★ arm in
// Go: one pass carrying the best sum ending here with nothing deleted
// (`kept`) and with one element deleted (`cut`).
package main

import (
	"fmt"
	"math"
)

func max64(a, b int64) int64 {
	if a > b {
		return a
	}
	return b
}

func maximumSum(arr []int64) int64 {
	kept := arr[0]
	cut := int64(math.MinInt64)
	best := arr[0]
	for _, x := range arr[1:] {
		if cut == math.MinInt64 {
			cut = kept
		} else {
			cut = max64(cut+x, kept)
		}
		kept = max64(kept+x, x)
		best = max64(max64(best, kept), cut)
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1182)
	arrays := [][]int64{}
	for a := 0; a < 10; a++ {
		arr := make([]int64, 100000)
		for i := range arr {
			arr[i] = nextRandom(&seed)%20001 - 10000
		}
		arrays = append(arrays, arr)
	}
	rounds := 100
	check := int64(0)
	for r := 0; r < rounds; r++ {
		for _, arr := range arrays {
			check = (check*131 + maximumSum(arr) + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d rounds of 10 arrays: checksum %d\n", rounds, check)
}

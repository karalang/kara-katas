// LeetCode #1331 bench, Go mirror of the Kāra bench: the ★ arm (the values
// sorted with slices.Sort, their repeats removed with slices.Compact, and
// each value's rank found by binary search) on 20 arrays of 10^5 values,
// the constraints' longest, each from 1 to 10^9 or from a narrower spread
// with many repeats, built once. Then 15 passes, each setting one value of
// every array from the checksum so far, answering it and folding two of
// its ranks plus the pass into the checksum.
package main

import (
	"fmt"
	"slices"
)

func arrayRankTransform(arr []int32) []int32 {
	distinct := slices.Clone(arr)
	slices.Sort(distinct)
	distinct = slices.Compact(distinct)
	ranks := make([]int32, len(arr))
	for i, x := range arr {
		at, _ := slices.BinarySearch(distinct, x)
		ranks[i] = int32(at + 1)
	}
	return ranks
}

var seed int64 = 1331

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 100000
	arrays := make([][]int32, 20)
	for t := range arrays {
		spread := int64(1000)
		if t%2 == 0 {
			spread = 1000000000
		}
		arrays[t] = make([]int32, n)
		for i := range arrays[t] {
			a := nextRandom()
			b := nextRandom()
			arrays[t][i] = int32((a*61036+b)%spread + 1)
		}
	}
	var check int64
	for pass := int64(0); pass < 15; pass++ {
		for t := 0; t < 20; t++ {
			at := check % n
			arrays[t][at] = int32(check/7%1000000000 + 1)
			ranks := arrayRankTransform(arrays[t])
			check = (check*31 + int64(ranks[at]) + int64(ranks[n-1]) + pass) % 1000000007
		}
	}
	fmt.Printf("15 passes over 20 arrays of 10^5: checksum %d\n", check)
}

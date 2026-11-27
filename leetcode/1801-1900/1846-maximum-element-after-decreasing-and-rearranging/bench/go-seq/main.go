// LeetCode #1846: Maximum Element After Decreasing and Rearranging -- the
// bench in Go: the ★ arm over 200 calls on the first 50000 to 99999 of one
// list of 10^5 numbers from 1 to 60000, built once, each run's length drawn
// from the checksum so far. Each call is handed its own copy of its run,
// which the arm sorts.
package main

import (
	"fmt"
	"slices"
)

func maximumElementAfterDecrementingAndRearranging(arr []int64) int64 {
	slices.Sort(arr)
	top := int64(0)
	for _, x := range arr {
		top = min(top+1, x)
	}
	return top
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1846)
	base := make([]int64, 0, 100000)
	for i := 0; i < 100000; i++ {
		hi := nextRandom(&seed)
		base = append(base, 1+(hi*32768+nextRandom(&seed))%60000)
	}
	check := int64(0)
	for call := int64(0); call < 200; call++ {
		n := 50000 + (check+call)%50000
		check = (check*31 + maximumElementAfterDecrementingAndRearranging(slices.Clone(base[:n]))) % 1000000007
	}
	fmt.Printf("200 calls: checksum %d\n", check)
}

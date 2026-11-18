// LeetCode #1200 bench: the ★ arm in Go, over the same 20 arrays of 10^5
// values and 10 rounds as the Kāra bench; each call sorts its own copy
// with `slices.Sort`.
package main

import (
	"fmt"
	"math"
	"slices"
)

func minimumAbsDifference(src []int64) [][2]int64 {
	arr := slices.Clone(src)
	slices.Sort(arr)
	least := int64(math.MaxInt64)
	for i := 1; i < len(arr); i++ {
		least = min(least, arr[i]-arr[i-1])
	}
	var pairs [][2]int64
	for i := 1; i < len(arr); i++ {
		if arr[i]-arr[i-1] == least {
			pairs = append(pairs, [2]int64{arr[i-1], arr[i]})
		}
	}
	return pairs
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	spans := []int64{1000000, 100000, 60000}
	seed := int64(1200)
	arrays := make([][]int64, 0, 20)
	for k := 0; k < 20; k++ {
		span := spans[k%3]
		taken := make([]bool, 2*span+1)
		arr := make([]int64, 0, 100000)
		for len(arr) < 100000 {
			a := nextRandom(&seed)
			b := nextRandom(&seed)
			v := (a*32768+b)%(2*span+1) - span
			if !taken[v+span] {
				taken[v+span] = true
				arr = append(arr, v)
			}
		}
		arrays = append(arrays, arr)
	}
	var check int64
	for r := 0; r < 10; r++ {
		for _, arr := range arrays {
			pairs := minimumAbsDifference(arr)
			check = (check*131 + int64(len(pairs))) % 1000000007
			for _, p := range pairs {
				check = (check*131 + p[0] + p[1] + 2000000) % 1000000007
			}
		}
	}
	fmt.Printf("10 rounds of 20 arrays of 100000 values: checksum %d\n", check)
}

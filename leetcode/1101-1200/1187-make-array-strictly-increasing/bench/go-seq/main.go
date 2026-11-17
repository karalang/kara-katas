// LeetCode #1187: Make Array Strictly Increasing -- the ★ arm in Go: for each
// count k of replacements so far, the least value the prefix can end on,
// over the same pairs as the Kāra bench.
package main

import (
	"fmt"
	"math"
	"sort"
)

func makeArrayIncreasing(arr1, arr2 []int64) int64 {
	sorted := append([]int64(nil), arr2...)
	sort.Slice(sorted, func(i, j int) bool { return sorted[i] < sorted[j] })
	spare := sorted[:0]
	for i, v := range sorted {
		if i == 0 || v != spare[len(spare)-1] {
			spare = append(spare, v)
		}
	}
	n := len(arr1)
	const none = int64(math.MaxInt64)
	end := make([]int64, n+1)
	for k := range end {
		end[k] = none
	}
	end[0] = math.MinInt64
	for _, a := range arr1 {
		next := make([]int64, n+1)
		for k := range next {
			next[k] = none
		}
		for k := 0; k <= n; k++ {
			if end[k] != none && a > end[k] {
				next[k] = a
			}
			if k > 0 && end[k-1] != none {
				bound := end[k-1]
				p := sort.Search(len(spare), func(i int) bool { return spare[i] > bound })
				if p < len(spare) && spare[p] < next[k] {
					next[k] = spare[p]
				}
			}
		}
		end = next
	}
	for k := 0; k <= n; k++ {
		if end[k] != none {
			return int64(k)
		}
	}
	return -1
}

var seed int64 = 1187

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func values(n int, span int64) []int64 {
	out := make([]int64, n)
	for i := range out {
		hi := nextRandom()
		out[i] = (hi*32768 + nextRandom()) % span
	}
	return out
}

func main() {
	var firsts, seconds [][]int64
	firsts = append(firsts, values(2000, 1000000001))
	seconds = append(seconds, values(2000, 1000000001))
	rising := make([]int64, 2000)
	for i := range rising {
		if i%40 == 39 {
			rising[i] = 0
		} else {
			rising[i] = int64(i) * 500000
		}
	}
	firsts = append(firsts, rising)
	seconds = append(seconds, values(2000, 1000000001))
	firsts = append(firsts, values(2000, 4000))
	seconds = append(seconds, values(2000, 4000))
	falling := make([]int64, 2000)
	for i := range falling {
		falling[i] = int64(2000-i) * 1000
	}
	firsts = append(firsts, falling)
	seconds = append(seconds, values(2000, 1000000001))
	rounds := int64(6)
	var check int64
	for round := int64(0); round < rounds; round++ {
		for p := 0; p < 4; p++ {
			ops := makeArrayIncreasing(firsts[p], seconds[p])
			check = (check*131 + ops + 2 + round) % 1000000007
		}
	}
	fmt.Printf("%d rounds of 4 pairs of 2000 values: checksum %d\n", rounds, check)
}

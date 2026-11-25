// LeetCode #1288 bench, Go: the same sort and sweep, workload and
// checksum as remove_covered_intervals.kara.
package main

import (
	"fmt"
	"sort"
)

func removeCoveredIntervals(intervals [][]int32) int32 {
	order := make([][]int32, len(intervals))
	for i, iv := range intervals {
		order[i] = append([]int32(nil), iv...)
	}
	sort.SliceStable(order, func(i, j int) bool {
		if order[i][0] != order[j][0] {
			return order[i][0] < order[j][0]
		}
		return order[i][1] > order[j][1]
	})
	var kept, reach int32
	for _, iv := range order {
		if iv[1] > reach {
			kept++
			reach = iv[1]
		}
	}
	return kept
}

func main() {
	var seed int64 = 1288
	pool := make([][]int32, 0, 100000)
	for i := 0; i < 100000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		start := seed % 100000
		seed = (seed*1103515245 + 12345) % 2147483648
		end := start + 1 + seed%(100000-start)
		pool = append(pool, []int32{int32(start), int32(end)})
	}
	var check int64
	for r := int64(0); r < 3000; r++ {
		at := (check + r*7919) % 99001
		window := make([][]int32, 1000)
		for i := range window {
			window[i] = append([]int32(nil), pool[at+int64(i)]...)
		}
		check = (check*131 + int64(removeCoveredIntervals(window))) % 1000000007
	}
	fmt.Printf("3000 windows of 1000 intervals: checksum %d\n", check)
}

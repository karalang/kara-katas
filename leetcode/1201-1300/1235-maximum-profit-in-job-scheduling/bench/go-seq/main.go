// LeetCode #1235 bench: the ★ arm in Go, over the same 20 sets of 50000
// jobs and 10 passes as the Kāra bench.
package main

import (
	"fmt"
	"sort"
)

func jobScheduling(start, end, profit []int64) int64 {
	n := len(start)
	order := make([]int, n)
	for i := range order {
		order[i] = i
	}
	sort.SliceStable(order, func(a, b int) bool { return end[order[a]] < end[order[b]] })
	ends := make([]int64, n)
	for k, i := range order {
		ends[k] = end[i]
	}
	best := make([]int64, n+1)
	for k := 0; k < n; k++ {
		job := order[k]
		before := sort.Search(n, func(m int) bool { return ends[m] > start[job] })
		best[k+1] = max(best[k], best[before]+profit[job])
	}
	return best[n]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1235)
	type set struct{ start, end, profit []int64 }
	var sets []set
	for t := int64(0); t < 20; t++ {
		long := 1000000 * (t%4 + 1)
		var s set
		for i := 0; i < 50000; i++ {
			a := nextRandom(&seed) * 32768
			st := (a+nextRandom(&seed))%999000000 + 1
			s.start = append(s.start, st)
			b := nextRandom(&seed) * 32768
			s.end = append(s.end, st+(b+nextRandom(&seed))%long+1)
			s.profit = append(s.profit, nextRandom(&seed)%10000+1)
		}
		sets = append(sets, s)
	}
	var check int64
	for pass := 0; pass < 10; pass++ {
		for _, s := range sets {
			check = (check*131 + jobScheduling(s.start, s.end, s.profit)) % 1000000007
		}
	}
	fmt.Printf("20 sets of 50000 jobs, 10 passes: checksum %d\n", check)
}

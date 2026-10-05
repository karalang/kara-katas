// Benchmark workload for LeetCode #349 — Go mirror of intersection.kara.
package main

import (
	"fmt"
	"sort"
)

const (
	POOL  = 1000000
	LEN   = 1000
	PAIRS = 20000
)

func intersection(a, b []int64) []int64 {
	seen := map[int64]struct{}{}
	for _, x := range a {
		seen[x] = struct{}{}
	}
	out := []int64{}
	for _, y := range b {
		if _, ok := seen[y]; ok {
			delete(seen, y)
			out = append(out, y)
		}
	}
	sort.Slice(out, func(i, j int) bool { return out[i] < out[j] })
	return out
}

func main() {
	pool := make([]int64, 0, POOL)
	x := int64(349)
	for k := 0; k < POOL; k++ {
		x = (x*1103515245 + 12345) % 2147483648
		pool = append(pool, x/16%1001)
	}

	sink := int64(0)
	for p := 0; p < PAIRS; p++ {
		x = (x*1103515245 + 12345) % 2147483648
		i := x / 16 % (POOL - LEN)
		x = (x*1103515245 + 12345) % 2147483648
		j := x / 16 % (POOL - LEN)
		a := append([]int64(nil), pool[i:i+LEN]...)
		b := append([]int64(nil), pool[j:j+LEN]...)
		r := intersection(a, b)
		s := int64(0)
		for _, v := range r {
			s += v
		}
		sink = (sink*31 + int64(len(r))*1000003 + s) % 1000000007
	}
	fmt.Printf("sink %d\n", sink)
}

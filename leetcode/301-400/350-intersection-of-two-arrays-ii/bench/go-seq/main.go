// Benchmark workload for LeetCode #350 — Go mirror of intersect.kara.
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

func intersect(a, b []int64) []int64 {
	counts := map[int64]int64{}
	for _, x := range a {
		counts[x]++
	}
	out := []int64{}
	for _, y := range b {
		left := counts[y]
		if left > 0 {
			counts[y] = left - 1
			out = append(out, y)
		}
	}
	sort.Slice(out, func(i, j int) bool { return out[i] < out[j] })
	return out
}

func main() {
	pool := make([]int64, 0, POOL)
	x := int64(350)
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
		r := intersect(a, b)
		s := int64(0)
		for _, v := range r {
			s += v
		}
		sink = (sink*31 + int64(len(r))*1000003 + s) % 1000000007
	}
	fmt.Printf("sink %d\n", sink)
}

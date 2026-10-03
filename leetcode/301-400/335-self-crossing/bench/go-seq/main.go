// Benchmark workload for LeetCode #335 — Go mirror of self_crossing.kara.
package main

import "fmt"

const (
	moves   = 1000000
	punches = 100
	modulus = 1073741789
)

func isSelfCrossing(d []int64) bool {
	n := len(d)
	for i := 3; i < n; i++ {
		if d[i] >= d[i-2] && d[i-1] <= d[i-3] {
			return true
		}
		if i >= 4 && d[i-1] == d[i-3] && d[i]+d[i-4] >= d[i-2] {
			return true
		}
		if i >= 5 &&
			d[i-2] >= d[i-4] &&
			d[i]+d[i-4] >= d[i-2] &&
			d[i-1] <= d[i-3] &&
			d[i-1]+d[i-5] >= d[i-3] {
			return true
		}
	}
	return false
}

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	hi := next(seed)
	return hi*32768 + next(seed)
}

func main() {
	seed := int64(335)
	d := make([]int64, 0, moves)
	for i := 0; i < moves; i++ {
		twoBack := int64(0)
		if i >= 2 {
			twoBack = d[i-2]
		}
		d = append(d, twoBack+1+next(&seed)%3)
	}
	sink := int64(0)
	for p := 0; p < punches; p++ {
		at := 2 + wide(&seed)%(moves-2)
		old := d[at]
		if p%2 == 0 {
			d[at] = 1
		}
		answer := int64(0)
		if isSelfCrossing(d) {
			answer = 1
		}
		d[at] = old
		sink = (sink*1000003 + answer*2000003 + at) % modulus
	}
	fmt.Println(sink)
}

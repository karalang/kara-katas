// Benchmark mirror of rangesum.kara — LeetCode #303, O(1) prefix-sum query.
// Same LCG, same query list, same sink.
package main

import "fmt"

const (
	n        = 65536
	nqueries = 200000
	passes   = 1800
)

func main() {
	state := int64(20303)

	prefix := make([]int64, n+1)
	for i := 0; i < n; i++ {
		state = (state*1103515245 + 12345) & 0x7fffffff
		v := (state/65536)%2001 - 1000
		prefix[i+1] = prefix[i] + v
	}

	qs := make([]int64, nqueries*2)
	for q := 0; q < nqueries; q++ {
		state = (state*1103515245 + 12345) & 0x7fffffff
		x := (state / 65536) % n
		state = (state*1103515245 + 12345) & 0x7fffffff
		y := (state / 65536) % n
		if x <= y {
			qs[q*2], qs[q*2+1] = x, y
		} else {
			qs[q*2], qs[q*2+1] = y, x
		}
	}

	var checksum int64
	for p := 0; p < passes; p++ {
		for k := 0; k < nqueries; k++ {
			v := prefix[qs[k*2+1]+1] - prefix[qs[k*2]]
			checksum = (checksum + v) & 0x3FFFFFFF
		}
	}

	fmt.Printf("checksum %d\n", checksum)
}

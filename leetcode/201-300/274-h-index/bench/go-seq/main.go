// Benchmark harness for LeetCode #274 — H-Index.
// Mirrors h_index.kara algorithm-for-algorithm; the sort is each language's
// stdlib sort on identical data (see ../README.md § Benchmarks).

package main

import (
	"fmt"
	"slices"
)

func hIndex(cit []int64) int64 {
	v := make([]int64, 0, len(cit))
	for i := 0; i < len(cit); i++ {
		v = append(v, cit[i])
	}
	slices.Sort(v)
	n := int64(len(v))
	for j := int64(0); j < n; j++ {
		if v[j] >= n-j {
			return n - j
		}
	}
	return 0
}

func main() {
	const np int64 = 4
	const n int64 = 60000
	const iters int64 = 600

	arrays := make([][]int64, 0, np)
	for p := int64(0); p < np; p++ {
		arr := make([]int64, 0, n)
		x := p + 1
		for t := int64(0); t < n; t++ {
			x = (x*1103515245 + 12345) % 2147483648
			r := (x / 65536) % 32768
			switch {
			case p == 0:
				arr = append(arr, r%30000)
			case p == 1:
				arr = append(arr, r%40)
			case p == 2:
				arr = append(arr, (r%7)*3000)
			default:
				arr = append(arr, t+(r%5))
			}
		}
		arrays = append(arrays, arr)
	}

	var sink int64 = 0
	for it := int64(0); it < iters; it++ {
		idx := (it * 3) % np
		sink = (sink*31 + hIndex(arrays[idx])) % 1000000007
	}
	fmt.Println(sink)
}

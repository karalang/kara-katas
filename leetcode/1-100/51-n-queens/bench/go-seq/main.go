// Bench mirror of nqueens_bench.kara — bitmask solution-counting backtracker,
// weighted-checksum int64 sink, swept over n = 8..13. go build.
// See ../../README.md § Benchmarks.
package main

import "fmt"

func count(n, row, cols, diag1, diag2, partial int64, acc, sink *int64) {
	if row == n {
		*acc++
		*sink += partial
		return
	}
	for c := int64(0); c < n; c++ {
		bitC := int64(1) << c
		bitD1 := int64(1) << (row + c)
		bitD2 := int64(1) << (row - c + (n - 1))
		if (cols&bitC) == 0 && (diag1&bitD1) == 0 && (diag2&bitD2) == 0 {
			count(n, row+1, cols|bitC, diag1|bitD1, diag2|bitD2, partial+c*(row+1), acc, sink)
		}
	}
}

func main() {
	var nLo, nHi int64 = 8, 13
	var total int64 = 0
	for n := nLo; n <= nHi; n++ {
		var acc, sink int64 = 0, 0
		count(n, 0, 0, 0, 0, 0, &acc, &sink)
		total += acc*100003 + sink
	}
	fmt.Println(total)
}

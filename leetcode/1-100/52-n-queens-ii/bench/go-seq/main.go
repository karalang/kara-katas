// Bench mirror of nqueens2_bench.kara — return-value counting backtracker,
// weighted-checksum int64 sink, swept over n = 9..13. go build.
// See ../../README.md § Benchmarks.
package main

import "fmt"

func search(n, row, cols, diag1, diag2, partial int64) int64 {
	if row == n {
		return 1 + partial
	}
	var acc int64 = 0
	for c := int64(0); c < n; c++ {
		bitC := int64(1) << c
		bitD1 := int64(1) << (row + c)
		bitD2 := int64(1) << (row - c + (n - 1))
		if (cols&bitC) == 0 && (diag1&bitD1) == 0 && (diag2&bitD2) == 0 {
			acc += search(n, row+1, cols|bitC, diag1|bitD1, diag2|bitD2, partial+c*(row+1))
		}
	}
	return acc
}

func main() {
	var nLo, nHi int64 = 9, 13
	var total int64 = 0
	for n := nLo; n <= nHi; n++ {
		total += search(n, 0, 0, 0, 0, 0)
	}
	fmt.Println(total)
}

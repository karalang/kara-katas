// Benchmark mirror — LeetCode 304, Range Sum Query 2D (Immutable).
// Same algorithm, same flat prefix layout, same LCG, same masked sink as
// rangesum2d.kara. See ../../README.md § Benchmarks.
package main

import "fmt"

func main() {
	const n int64 = 256
	const stride int64 = n + 1
	const queries int64 = 100000
	const passes int64 = 1800
	var state int64 = 20304

	m := make([]int64, n*n)
	for i := int64(0); i < n*n; i++ {
		state = (state*1103515245 + 12345) % 2147483648
		m[i] = state%21 - 10
	}

	pre := make([]int64, (n+1)*stride)
	for r := int64(0); r < n; r++ {
		for c := int64(0); c < n; c++ {
			pre[(r+1)*stride+(c+1)] = pre[r*stride+(c+1)] +
				pre[(r+1)*stride+c] -
				pre[r*stride+c] +
				m[r*n+c]
		}
	}

	qr1 := make([]int64, queries)
	qc1 := make([]int64, queries)
	qr2 := make([]int64, queries)
	qc2 := make([]int64, queries)
	for q := int64(0); q < queries; q++ {
		state = (state*1103515245 + 12345) % 2147483648
		a := state % n
		state = (state*1103515245 + 12345) % 2147483648
		b := state % n
		state = (state*1103515245 + 12345) % 2147483648
		c := state % n
		state = (state*1103515245 + 12345) % 2147483648
		d := state % n
		if a <= b {
			qr1[q], qr2[q] = a, b
		} else {
			qr1[q], qr2[q] = b, a
		}
		if c <= d {
			qc1[q], qc2[q] = c, d
		} else {
			qc1[q], qc2[q] = d, c
		}
	}

	var checksum int64
	for p := int64(0); p < passes; p++ {
		for k := int64(0); k < queries; k++ {
			r1, c1, r2, c2 := qr1[k], qc1[k], qr2[k], qc2[k]
			v := pre[(r2+1)*stride+(c2+1)] -
				pre[r1*stride+(c2+1)] -
				pre[(r2+1)*stride+c1] +
				pre[r1*stride+c1]
			checksum = (checksum + v) & 0x3FFFFFFF
		}
	}

	fmt.Printf("checksum %d\n", checksum)
}

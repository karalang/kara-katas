// Benchmark mirror — LeetCode 311, Sparse Matrix Multiplication.
// Same flat row-major layout, same LCG, same zero-skipping multiply, same
// per-pass perturbation and masked sink as spmm.kara. See ../../README.md.
package main

import "fmt"

func main() {
	const n int64 = 320
	const passes int64 = 620
	cells := n * n
	a := make([]int64, cells)
	b := make([]int64, cells)
	c := make([]int64, cells)
	state := int64(20311)
	for i := int64(0); i < cells; i++ {
		state = (state*1103515245 + 12345) % 2147483648
		if state%100 < 4 {
			state = (state*1103515245 + 12345) % 2147483648
			a[i] = state%9 - 4
		} else {
			a[i] = 0
		}
		state = (state*1103515245 + 12345) % 2147483648
		if state%100 < 4 {
			state = (state*1103515245 + 12345) % 2147483648
			b[i] = state%9 - 4
		} else {
			b[i] = 0
		}
	}

	var checksum int64
	for p := int64(0); p < passes; p++ {
		slot := (p * 7919) % cells
		a[slot] = a[slot] + (checksum & 1)
		for i := int64(0); i < cells; i++ { c[i] = 0 }
		for r := int64(0); r < n; r++ {
			arow := r * n
			for k := int64(0); k < n; k++ {
				av := a[arow+k]
				if av != 0 {
					brow := k * n
					for j := int64(0); j < n; j++ { c[arow+j] += av * b[brow+j] }
				}
			}
		}
		var acc int64
		for t := int64(0); t < cells; t++ { acc = (acc + c[t]) & 0x3FFFFFFF }
		checksum = (checksum + acc) & 0x3FFFFFFF
	}
	fmt.Printf("checksum %d\n", checksum)
}

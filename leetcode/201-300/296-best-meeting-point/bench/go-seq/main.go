// Benchmark mirror of meetpoint.kara — LeetCode #296, separable medians.
// Same two scans (row-major then column-major), same reused scratch, same sink.
package main

import "fmt"

const (
	ncases = 400
	dim    = 128
	passes = 30
	cells  = dim * dim
	mod    = int64(1000000007)
)

func main() {
	corpus := make([]byte, ncases*cells)
	state := int64(24601)
	for n := range corpus {
		state = (state*1103515245 + 12345) & 0x7fffffff
		if (state/65536)%100 < 10 {
			corpus[n] = 1
		}
	}

	rows := make([]int64, cells)
	cols := make([]int64, cells)
	var checksum int64

	for p := 0; p < passes; p++ {
		for ci := 0; ci < ncases; ci++ {
			base := ci * cells

			k := 0
			for r := 0; r < dim; r++ {
				for c := 0; c < dim; c++ {
					if corpus[base+r*dim+c] == 1 {
						rows[k] = int64(r)
						k++
					}
				}
			}

			k2 := 0
			for c := 0; c < dim; c++ {
				for r := 0; r < dim; r++ {
					if corpus[base+r*dim+c] == 1 {
						cols[k2] = int64(c)
						k2++
					}
				}
			}

			var total int64
			if k > 0 {
				mr := rows[k/2]
				mc := cols[k/2]
				for i := 0; i < k; i++ {
					dr := rows[i] - mr
					if dr < 0 {
						dr = -dr
					}
					dc := cols[i] - mc
					if dc < 0 {
						dc = -dc
					}
					total += dr + dc
				}
			}
			checksum = (checksum + total) % mod
		}
	}

	fmt.Printf("checksum %d\n", checksum)
}

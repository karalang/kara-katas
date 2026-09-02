// Benchmark mirror — LeetCode 305, Number of Islands II.
// Same algorithm, same Fisher-Yates over the same LCG, same masked sink as
// islands2.kara. See ../../README.md § Benchmarks.
package main

import "fmt"

func main() {
	const n int64 = 256
	const cells int64 = n * n
	const passes int64 = 160

	order := make([]int64, cells)
	for i := int64(0); i < cells; i++ {
		order[i] = i
	}
	state := int64(20305)
	for i := cells - 1; i > 0; i-- {
		state = (state*1103515245 + 12345) % 2147483648
		j := state % (i + 1)
		order[i], order[j] = order[j], order[i]
	}

	parent := make([]int64, cells)
	rank := make([]int64, cells)
	var checksum int64

	for p := int64(0); p < passes; p++ {
		for k := int64(0); k < cells; k++ {
			parent[k] = -1
			rank[k] = 0
		}
		var count int64
		for q := int64(0); q < cells; q++ {
			idx := order[q]
			r := idx / n
			c := idx % n
			parent[idx] = idx
			count++
			for d := int64(0); d < 4; d++ {
				nb := int64(-1)
				if d == 0 && r > 0 {
					nb = idx - n
				}
				if d == 1 && r < n-1 {
					nb = idx + n
				}
				if d == 2 && c > 0 {
					nb = idx - 1
				}
				if d == 3 && c < n-1 {
					nb = idx + 1
				}
				if nb >= 0 && parent[nb] >= 0 {
					ra := idx
					for parent[ra] != ra {
						ra = parent[ra]
					}
					cur := idx
					for parent[cur] != ra {
						nx := parent[cur]
						parent[cur] = ra
						cur = nx
					}
					rb := nb
					for parent[rb] != rb {
						rb = parent[rb]
					}
					cur = nb
					for parent[cur] != rb {
						nx := parent[cur]
						parent[cur] = rb
						cur = nx
					}
					if ra != rb {
						if rank[ra] < rank[rb] {
							parent[ra] = rb
						} else if rank[ra] > rank[rb] {
							parent[rb] = ra
						} else {
							parent[rb] = ra
							rank[ra]++
						}
						count--
					}
				}
			}
			checksum = (checksum + count) & 0x3FFFFFFF
		}
	}
	fmt.Printf("checksum %d\n", checksum)
}

// Benchmark mirror — LeetCode 307, Range Sum Query (Mutable).
// Same Fenwick tree, same LCG-generated operation script, same masked sink as
// fenwick.kara. See ../../README.md § Benchmarks.
package main

import "fmt"

func main() {
	const n int64 = 65536
	const ops int64 = 200000
	const passes int64 = 110

	tree := make([]int64, n+1)
	data := make([]int64, n)
	kind := make([]int64, ops)
	opa := make([]int64, ops)
	opb := make([]int64, ops)

	state := int64(20307)
	for k := int64(0); k < ops; k++ {
		state = (state*1103515245 + 12345) % 2147483648
		t := state % 2
		state = (state*1103515245 + 12345) % 2147483648
		x := state % n
		state = (state*1103515245 + 12345) % 2147483648
		y := state % n
		kind[k] = t
		if t == 0 {
			opa[k], opb[k] = x, y%2001-1000
		} else if x <= y {
			opa[k], opb[k] = x, y
		} else {
			opa[k], opb[k] = y, x
		}
	}

	var checksum int64
	for p := int64(0); p < passes; p++ {
		for k := int64(0); k < ops; k++ {
			if kind[k] == 0 {
				i := opa[k]
				delta := opb[k] - data[i]
				data[i] = opb[k]
				for x := i + 1; x <= n; x += x & -x {
					tree[x] += delta
				}
			} else {
				var total int64
				for hi := opb[k] + 1; hi > 0; hi -= hi & -hi {
					total += tree[hi]
				}
				for lo := opa[k]; lo > 0; lo -= lo & -lo {
					total -= tree[lo]
				}
				checksum = (checksum + total) & 0x3FFFFFFF
			}
		}
	}
	fmt.Printf("checksum %d\n", checksum)
}
